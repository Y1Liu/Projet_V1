from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField, SelectField, BooleanField
from wtforms_components import TimeField, DateField
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mongoengine import MongoEngine, Document
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import DataRequired
from tags import Tags, TAGS


###############################################################################
#CLASSE Formulaire de renseingment
###############################################################################
class GeneralForm(FlaskForm):
    add_dep=StringField('Adresse de départ :', validators=[DataRequired()])
    dep_home=BooleanField('Partir de votre domicile')
    add_arr=StringField('Adresse d\'arrivée :', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', choices=Tags(TAGS))
    locomotion=RadioField('Locomotion :', choices=[('driving','Voiture'),('transit','Transports en commun'),('walking','A pied')])
    optimisation=RadioField('Optimisation :', choices=[('distance','Distance'),('time','Temps'),('affinity','Affinités')])
    h_dep=TimeField('Heure de départ :')
    j_dep=DateField('Jour de départ :')
    h_arr=TimeField('Heure d\'arrivée :')
    j_arr=DateField('Jour d\'arrivée :')
    max_escales=SelectField('Nombre d\'escales souhaité :', choices=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)])
    escales=TextField('Escales :')
    t_max=RadioField('Durée maximale sans pause :', choices=[(0,'Sans pause'),(3600,'1h00'),(7200,'2h00'),(10800,'3h00')])
    d_max=RadioField('Distance maximale sans pause:', choices=[(0,'Sans pause'),(100000,'100km'),(20000,'200km'),(300000,'300km')])
    submit=SubmitField('Valider')
###############################################################################    