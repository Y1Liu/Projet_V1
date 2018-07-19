#!/usr/bin/env python
# coding: utf-8


###############################################################################
#Fichier contenant les fonction de planification
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#juin 2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField, SelectField
from wtforms_components import TimeField
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mongoengine import MongoEngine, Document
import pymongo as pm
from registerform import RegisterForm
from loginform import LoginForm
from logoutform import LogoutForm
from modifform import ModifForm
from modifacceptedform import ModifAcceptedForm
from generalform import GeneralForm
from tags import Tags
import computing as cp
import plan as pl
import hashlib
from graphnode import *
import numpy as np
###############################################################################


###############################################################################
# App config.
###############################################################################
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
bootstrap = Bootstrap(app)
datas=cp.init_matrix()
SESSION_TYPE = "mongodb"
#Session(app)
mongo = pm.MongoClient()
###############################################################################


###############################################################################
#DATABASE
###############################################################################
client=pm.MongoClient('mongodb://root:root_06@ds263660.mlab.com:63660/smartplanner_users')
db=client.get_database()
users=db['users']
###############################################################################


############################################################################### 
#ROUTES
###############################################################################
#Page de login
"""
    IN : 
        login_form : formulaire de login   
    OUT : 
        1) template 'login.html'
        2) Après validation du formulaire :
            - si utilisateur dans la BDD : -> redirection vers route 'form' + cryptage du mot de passe
            - sinon -> redirection vers route 'login'
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form=LoginForm(request.form)
    if login_form.validate_on_submit():
        pw=request.form['login_password'].encode('utf-8')
        hashpass=hashlib.md5(pw)
        pwd=hashpass.hexdigest()
        user=users.find({'email':request.form['login_email'], 'password':pwd}).count()
        if user==1:
            session['email']=request.form['login_email']
            return redirect(url_for('form'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)


#Page d'inscription
"""
    IN : 
        register_form : formulaire d'inscription
 
    OUT : 
        1) template 'register.html'
        2) après validation du formulaire -> redirection vers route 'form' + cryptage du mot de passe
"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form)  
    if register_form.validate_on_submit():
        pw=request.form['register_password'].encode('utf-8')
        hashpass=hashlib.md5(pw)
        pwd=hashpass.hexdigest()
        users.insert({'email': request.form['register_email'], 'password':pwd, 'nom':request.form['register_nom'], 'prenom':request.form['register_prenom'], 'rue':request.form['register_rue'], 'cp':request.form['register_cp'], 'ville':request.form['register_ville'], 'tags':register_form.register_tags.data})
        session['email'] = request.form['register_email']
        return redirect(url_for('form'))
    return render_template('register.html', register_form=register_form)


#Page d'accueil
"""
    IN :  
    OUT : template 'index.html'  
"""
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', Title="Accueil")


#Page de profil
"""
    IN : 
        modif_accepted_form : formulaire de modification des informations utilisateur
        logout_form & modif_form : header    
    OUT : 
        1) template 'profile.html'
        2) Après validation de modif_accepted_form -> redirection vers route 'index'
        3) Après validation de logout_form -> deconnexion et redirection vers route 'login'
        4) Après validation de modif_form -> redirection vers route 'profile'
"""
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    logout_form=LogoutForm(request.form)
    modif_form=ModifForm(request.form)
    modif_accepted_form=ModifAcceptedForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        session['email']=None
        return redirect(url_for('login'))
    if modif_accepted_form.register_submit.data and modif_accepted_form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('profile.html', logout_form=logout_form, modif_form=modif_form, session_email=session['email'], modif_accepted_form=modif_accepted_form)    


#Page de formulaire
"""
    IN : 
        form : formulaire de renseignement     
    OUT : 
        template 'form.html'
        si optimisation en distance/temps : get_path = tableau avec les noms et scores de chaque étape
        si optimisation en affinités : get_way = liste d'étapes [["ville1", "score1"], ["ville2", "score2"], ...] 
"""
@app.route('/form', methods=['GET','POST'])
def form():
    logout_form=LogoutForm(request.form)
    modif_form=ModifForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        session['email']=None
        return redirect(url_for('index'))

    form = GeneralForm(request.form)
    test=[]
    tags=['Hall', 'Museum']
    start=Node(1000, 0, None, 0, 0)
    target=Node(10000, 0, None, 0, 0)
    if request.method == 'POST':
        add_dep=request.form.get('add_dep')
        session["add_dep"]=add_dep   
        add_arr=request.form.get('add_arr')
        session["add_arr"]=add_arr
        escales=[form.escales.data]
        tags=form.tags.data
        session["tags"]=tags
        max_escales=int(request.form.get('max_escales'))
        optimisation=request.form.get('optimisation')
        mode=request.form.get('locomotion')
        h_dep=request.form.get('h_dep')
        session["h_dep"]=h_dep
        j_dep=request.form.get('j_dep')
        session["j_dep"]=j_dep
        h_arr=request.form.get('h_arr')
        session["h_arr"]=h_arr
        j_arr=request.form.get('j_arr')
        session["j_arr"]=j_arr
        t_max=int(request.form.get('t_max'))
        d_max=int(request.form.get('d_max'))
        overallScore = cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0]
        dtfr=cp.get_graph_matrix(add_dep, add_arr, escales, mode, overallScore)
        if (optimisation == 'distance'):
            df_filtered = dtfr.loc[(dtfr['distance'] < d_max) & (dtfr['distance'] > 50000)]
        elif (optimisation == 'time'):
            df_filtered = dtfr.loc[dtfr['time'] < t_max]
        elif (optimisation == 'affinity'):
            df_filtered = dtfr.loc[(dtfr['distance']<d_max) & (dtfr['distance'] > 50000)]
        test=pl.get_path(start, target, dtfr, overallScore, optimisation, df_filtered, datas[0], add_dep, add_arr, escales)
        session["test"]=test[0]
        return redirect('/map')
    else:
        tags=session.get("tags", None)
        test=session.get("test", None)
    return render_template('form.html', title='Formulaire', form=form, logout_form=logout_form, modif_form=modif_form, session_email=session['email'])


#Page d'affichage de la carte
"""
    IN : 
        depart : Ville de départ enregistrée depuis la requête utilisateur
        j_dep : Jour de départ
        h_dep: Heure de départ
        arrivee : Ville d'arrivée enregistrée depuis la requête utilisateur
        tags : Tags fournis par l'utilisateur
        test = trajet fourni par l'algorithme
    OUT :   
        template 'map.html' avec la carte complétée
"""
@app.route('/map', methods=['GET','POST'])
def map():
    depart=session.get("add_dep", None)
    j_dep=session.get("j_dep", None)
    h_dep=session.get("h_dep", None)
    arrivee=session.get("add_arr", None)
    tags=session.get("tags", None)
    test=session.get("test", None)
    logout_form = LogoutForm(request.form)
    modif_form = ModifForm(request.form)
    modif_accepted_form = ModifAcceptedForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        session['email'] = None
        return redirect(url_for('login'))
    return render_template('map.html', title='Map', depart=depart, j_dep=j_dep, h_dep=h_dep, arrivee=arrivee, tags=tags, test=test, logout_form=logout_form, modif_form=modif_form, session_email=session['email'], modif_accepted_form=modif_accepted_form)
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == "__main__":
    app.run(debug="true")
###############################################################################
