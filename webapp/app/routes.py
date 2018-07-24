#!/usr/bin/env python
# coding: utf-8


###############################################################################
# Fichier contenant les fonction de planification
# Par Arnaud Duhamel et Robin Cavalieri
# Planificateur intelligent
# SOLUTEC Paris
# juin 2018
###############################################################################


###############################################################################
# LIBRAIRIES
###############################################################################
from flask import Flask, render_template, flash, request, redirect, url_for, session
from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField, \
    SelectField
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
import schedule as sc
import hashlib
from graphnode import *
import configparser
import numpy as np

###############################################################################


###############################################################################
# App config.
###############################################################################
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
cfg = configparser.ConfigParser()
cfg.read('conf.cfg')
user = cfg.get('DB', 'user')
password = cfg.get('DB', 'password')
app.config['MONGODB_SETTINGS'] = {'db': 'smartplanner_users',
                                  'host': 'mongodb://' + user + ':' + password + '@ds263660.mlab.com:63660/smartplanner_users'}
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
datas = cp.init_matrix()
SESSION_TYPE = "mongodb"
# Session(app)
mongo = pm.MongoClient()
###############################################################################


###############################################################################
# DATABASE
###############################################################################
db = MongoEngine(app)


###############################################################################
class User(UserMixin, db.Document):
    # CONSTRUCTEUR DE User
    """
    def __init__(self, email, password, nom, prenom, rue, cp, ville, tags):
    """
    email = db.EmailField(max_length=30)
    password = db.StringField(max_length=100)
    nom = db.StringField(max_length=30)
    prenom = db.StringField(max_length=30)
    rue = db.StringField(max_length=30)
    cp = db.StringField(max_length=30)
    ville = db.StringField(max_length=30)
    tags = db.ListField(max_length=30)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


###############################################################################
# ROUTES
###############################################################################
# Page de login
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
    if current_user.is_authenticated == True:
        return redirect(url_for('form'))
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate():
            check_user = User.objects(email=login_form.login_email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], login_form.login_password.data):
                    login_user(check_user)
                    return redirect(url_for('form'))
                else:
                    error = "e-mail ou mot de passe invalide"
                    return render_template('login.html', error=error, login_form=login_form)
    return render_template('login.html', login_form=login_form)


# Page d'inscription
"""
    IN : 
        register_form : formulaire d'inscription

    OUT : 
        1) template 'register.html'
        2) après validation du formulaire -> redirection vers route 'form' + cryptage du mot de passe
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate():
            existing_user = User.objects(email=register_form.register_email.data).first()
            if existing_user is None:
                pwd = generate_password_hash(register_form.register_password.data, method='sha256')
                new = User(email=request.form['register_email'],
                           password=pwd,
                           nom=request.form['register_nom'],
                           prenom=request.form['register_prenom'],
                           rue=request.form['register_rue'],
                           cp=request.form['register_cp'],
                           ville=request.form['register_ville'],
                           tags=register_form.register_tags.data).save()
                login_user(new)
                return redirect(url_for('form'))
            else:
                error = "Compte existant"
                return render_template('register.html', error=error, register_form=register_form)
    return render_template('register.html', register_form=register_form)


# Page de profil
"""
    IN : 
        modif_accepted_form : formulaire de modification des informations utilisateur
        logout_form & modif_form : header    
    OUT : 
        1) template 'profile.html'
        2) Après validation de modif_accepted_form -> redirection vers route 'login'
        3) Après validation de logout_form -> deconnexion et redirection vers route 'login'
        4) Après validation de modif_form -> redirection vers route 'profile'
"""


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    logout_form = LogoutForm(request.form)
    modif_form = ModifForm(request.form)
    modif_accepted_form = ModifAcceptedForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        logout_user()
        return redirect(url_for('login'))
    if modif_accepted_form.register_submit.data and modif_accepted_form.validate_on_submit():
        return redirect(url_for('profile'))
    return render_template('profile.html', logout_form=logout_form, modif_form=modif_form, session_email=current_user.email, modif_accepted_form=modif_accepted_form)


# Page de formulaire
"""
    IN : 
        form : formulaire de renseignement     
    OUT : 
        template 'form.html'
        si optimisation en distance/temps : get_path = tableau avec les noms et scores de chaque étape
        si optimisation en affinités : get_way = liste d'étapes [["ville1", "score1"], ["ville2", "score2"], ...] 
"""


@app.route('/form', methods=['GET', 'POST'])
@login_required
def form():
    logout_form = LogoutForm(request.form)
    modif_form = ModifForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        logout_user()
        return redirect(url_for('login'))

    form = GeneralForm(request.form)
    test = []
    tags = ['Hall', 'Museum']
    start = Node(1000, 0, None, 0, 0)
    target = Node(10000, 0, None, 0, 0)
    if request.method == 'POST':
        add_dep = request.form.get('add_dep')
        session["add_dep"] = add_dep
        add_arr = request.form.get('add_arr')
        session["add_arr"] = add_arr
        escales = [form.escales.data]
        tags = form.tags.data
        session["tags"] = tags
        max_escales = int(request.form.get('max_escales'))
        optimisation = request.form.get('optimisation')
        mode = request.form.get('locomotion')
        h_dep = request.form.get('h_dep')
        session["h_dep"] = h_dep
        j_dep = request.form.get('j_dep')
        session["j_dep"] = j_dep
        h_arr = request.form.get('h_arr')
        session["h_arr"] = h_arr
        j_arr = request.form.get('j_arr')
        session["j_arr"] = j_arr
        t_max = int(request.form.get('t_max'))
        d_max = int(request.form.get('d_max'))
        overallScore = cp.get_classement(datas[2], tags, datas[1], datas[3], datas[0])[0]
        dtfr = cp.get_graph_matrix(add_dep, add_arr, escales, mode, overallScore)
        if (optimisation == 'distance'):
            df_filtered = dtfr.loc[(dtfr['distance'] < d_max) & (dtfr['distance'] > 50000)]
        elif (optimisation == 'time'):
            df_filtered = dtfr.loc[dtfr['time'] < t_max]
        elif (optimisation == 'affinity'):
            df_filtered = dtfr.loc[(dtfr['distance'] < d_max) & (dtfr['distance'] > 50000)]
        test = pl.get_path(start, target, dtfr, overallScore, optimisation, df_filtered, datas[0], add_dep, add_arr, escales)
        session["test"] = test[0]
        time = sc.schedule_str(h_dep, h_arr, dtfr, test[1])
        session["time"] = time
        return redirect('/map')
    else:
        tags = session.get("tags", None)
        test = session.get("test", None)
    return render_template('form.html', title='Formulaire', form=form, logout_form=logout_form, modif_form=modif_form, session_email=current_user.email)


# Page d'affichage de la carte
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


@app.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    depart = session.get("add_dep", None)
    j_dep = session.get("j_dep", None)
    h_dep = session.get("h_dep", None)
    arrivee = session.get("add_arr", None)
    tags = session.get("tags", None)
    test = session.get("test", None)
    time = session.get("time", None)
    logout_form = LogoutForm(request.form)
    modif_form = ModifForm(request.form)
    modif_accepted_form = ModifAcceptedForm(request.form)
    if modif_form.modif_submit.data and modif_form.validate_on_submit():
        return redirect(url_for('profile'))
    if logout_form.logout_submit.data and logout_form.validate_on_submit():
        logout_user()
        return redirect(url_for('login'))
    return render_template('map.html', title='Map', depart=depart, j_dep=j_dep, h_dep=h_dep, arrivee=arrivee, tags=tags, test=test, time=time, logout_form=logout_form, modif_form=modif_form, session_email=current_user.email, modif_accepted_form=modif_accepted_form)


###############################################################################


###############################################################################
# MAIN
###############################################################################
if __name__ == "__main__":
    app.run(debug="true")
###############################################################################
