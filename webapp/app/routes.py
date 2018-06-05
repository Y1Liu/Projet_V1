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
from flask import render_template, flash, redirect, Markup, request, url_for, session
from app import app
from app.forms import TrajectForm
from werkzeug.contrib.cache import SimpleCache
import win32api
import cgi
import json


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
	#user = {'username': 'Arnaud'}
	return render_template('index.html', title='Home')

#Fonction créant la page du formulaire de renseignements
#Renvoie les choix de l'utilisateur sous forme de liste après soumission du formulaire
#Utilise la classe cached pour garder les données en cache
@app.route('/form', methods=['GET', 'POST'])
@cached()
def form():
	form = TrajectForm()
	Result=[]
	#escales=[]
	#if form.addEscales.data:
	#	try:
	#		form.choix_escales.append_entry()
	#	except AssertionError:
	#		win32api.MessageBox(0, 'Vous ne pouvez pas ajouter plus de 3 escales', 'Nombre max d\'escales atteinte')
	
	#elif form.deleteEscales.data:
	#	try:
	#		form.choix_escales.pop_entry()
	#	except IndexError:
	#		win32api.MessageBox(0, 'Vous n\'avez plus d\'escale à supprimer', 'Plus d\'escale')

	if form.validate_on_submit():
		Result.append(form.depart.data)
		depart=form.depart.data

		#Result.append(form.start_date_time.data.strftime('%d/%m/%Y %H:%M'))
		
		Result.append(form.arrivee.data)
		arrivee=form.arrivee.data    
		
		Result.append(form.choix_escales.data)
		#flash(form.choix_escales[1]['escales'].data)
		for i in range(0,len(form.choix_escales.data)):
			try:
				escales.append(form.choix_escales[i]['escales'].data)
			except IndexError:
				escales=escales
		escales=form.choix_escales.data
		#flash(escales)
		#Result.append(form.mode.data)
		
		#Result.append(form.pause_voyage.data)
		
		#Result.append(form.tps_repas.data)
		
		#Result.append(form.tags.data)
		
		session["depart"]=depart
		session["arrivee"]=arrivee
		session["escales"]=escales    
		#flash(Result)
		return redirect('/map')
	return render_template('form2.html', title='Formulaire', form=form)


@app.route('/test', methods=['GET','POST'])
def test():
	if request.method == 'POST':
		data = request.get_json()
		with open('forms.json', 'w') as json_file:
			json.dump(data, json_file, indent=4)
	return render_template('test.html', title='test')
		   

@app.route('/map')
def map():
	depart=session.get("depart",None)
	arrivee=session.get("arrivee", None)
	escales=session.get("escales", None)
	
	return render_template('map.html', title='Map', depart=depart, arrivee=arrivee, escales=escales)


