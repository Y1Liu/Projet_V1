#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#Fichier contenant la fonction créant le formulaire de renseignements
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired
from .tags import *


###############################################################################
#Fonction créant le formulaire
###############################################################################
class TrajectForm(FlaskForm):
	depart = StringField('Adresse de depart', validators=[DataRequired()])
	arrivee = StringField('Adresse d arrivee', validators=[DataRequired()])
	escales = BooleanField('Ajouter des escales ?')
	choix_escales = StringField('')
	mode = SelectField('Moyen de transport', choices=[('Voiture', 'Voiture'), ('Train', 'Train')])
	pause_voyage = SelectField('Duree maximale d un trajet avant une pause', choices=[('1h', '1h'),('2h', '2h'),('3h', '3h'),('4h', '4h'),('5h', '5h'),('6h', '6h'),])
	tps_repas = SelectField('Duree maximale du repas', choices=[('30min', '30min'),('1h', '1h'),('2h', '2h')])
	tags = SelectMultipleField('Tags', choices=Tags(TAGS))
	submit = SubmitField('Valider')




#open(PATH_FILE, 'r') as csv_file:
#	csv_file.reader()