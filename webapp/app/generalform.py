from wtforms import TextField, TextAreaField, validators, StringField, SubmitField, RadioField, SelectMultipleField, SelectField
from wtforms_components import TimeField
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
class GeneralForm(FlaskForm):
    add_dep=StringField('Adresse de départ :', validators=[DataRequired()])
    add_arr=StringField('Adresse d\'arrivée :', validators=[DataRequired()])
    #tags=StringField('Tags :', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', choices=Tags(TAGS))
    locomotion=RadioField('Locomotion :', choices=[('driving','Voiture'),('transit','Transports en commun'),('walking','A pied')])
    optimisation=RadioField('Optimisation :', choices=[('distance','Distance'),('time','Temps'),('affinity','Affinités')])
    h_dep=TimeField('Heure de départ :')
    j_dep=TimeField('Jour de départ :')
    h_arr=TimeField('Heure d\'arrivée :')
    j_arr=TimeField('Jour d\'arrivée :')
    max_escales=SelectField('Nombre maximal d\'escales :', choices=[(0,0),(1,1),(2,2),(3,3),(4,4),(5,5)])
    escales=TextField('Escales :')
    t_max=RadioField('Durée maximale sans pause :', choices=[(0,'Sans pause'),(3600,'1h00'),(7200,'2h00'),(10800,'3h00')])
    d_max=RadioField('Distance maximale sans pause:', choices=[(0,'Sans pause'),(100000,'100km'),(20000,'200km'),(300000,'300km')])
    t_repas=RadioField('Durée maximale du repas :', choices=[(900,'15 min'),(1800,'30 min'),(3600,'1h00')])
    submit=SubmitField('Valider')
###############################################################################    