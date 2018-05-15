#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#Fichier contenant les fonctionsde création de chaque page de l'application
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask import render_template, flash, redirect, Markup, request
from app import app
from app.forms import TrajectForm
from werkzeug.contrib.cache import SimpleCache


###############################################################################
#CONSTANTES
###############################################################################
CACHE_TIMEOUT = 60 #Définit le timeout du cache à 60 secondes
cache = SimpleCache()

###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant la mise en cache des données
#Permet de mettre en cache des objets individuels comme le résultat d'une requête
class cached(object):

	def __init__(self, timeout=None):
		self.timeout = timeout or CACHE_TIMEOUT

	def __call__(self, f):
		def decorator(*args, **kwargs):
			response = cache.get(request.path)
			if response is None:
				response = f(*args, **kwargs)
				cache.set(request.path, response, self.timeout)
				cache.clear()
			return response
		return decorator

#Fonction créant une page d'accueil
@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Arnaud'}
	return render_template('index.html', title='Home', user=user)

#Fonction créant la page du formulaire de renseignements
#Renvoie les choix de l'utilisateur sous forme de liste après soumission du formulaire
#Utilise la classe cached pour garder les données en cache
@app.route('/form', methods=['GET', 'POST'])
@cached()
def form():
	form = TrajectForm()
	Result=[]
	if form.validate_on_submit():
		Result.append(form.depart.data)
		Result.append(form.start_date_time.data.strftime('%d/%m/%Y %H:%M'))
		#Result.append(form.start_time.data)
		Result.append(form.arrivee.data)
		Result.append(form.choix_escales.data)
		Result.append(form.mode.data)
		Result.append(form.pause_voyage.data)
		Result.append(form.tps_repas.data)
		Result.append(form.tags.data)
		flash(Result)
		return redirect('/map')
	return render_template('forms.html', title='Formulaire', form=form)


@app.route('/response')
def response():
	return render_template('response.html', title='response')


@app.route('/loading')
def loading():
    return render_template('loading.html', title='loading')
           

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


