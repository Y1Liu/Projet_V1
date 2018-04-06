#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#Fichier contenant les fonctions permettant d'accéder à chaque page de l'application
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask import render_template, flash, redirect, Markup
from app import app
from app.forms import TrajectForm
import sys
from app.cache import cache


###############################################################################
#FONCTIONS
###############################################################################
#Fonction créant une page d'accueil
@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Arnaud'}
	return render_template('index.html', title='Home', user=user)

#Fonction créant la page du formulaire de renseignements
#Renvoie les choix de l'utilisateur après soumission du formulaire
#Données en cache pendant 300 secondes
@app.route('/form', methods=['GET', 'POST'])
@cache.cached(timeout=300)
#@cache.cached(300, key_prefix='form', unless='only_cache_get')
def form():
	form = TrajectForm()
	if form.validate_on_submit():
		reload(sys)
		sys.setdefaultencoding('utf8')
		flash(Markup('Ville de départ : <b>{}</b>'.format(form.depart.data)))
		flash(Markup('Ville d arrivee : <b>{}</b>'.format(form.arrivee.data)))
		flash(Markup('Moyen de transport : <b>{}</b>'.format(form.mode.data)))
		flash(Markup('Temps maximal de trajet : <b>{}</b>'.format(form.pause_voyage.data)))
		flash(Markup('Durée maximale du repas : <b>{}</b>'.format(form.tps_repas.data)))
		flash(Markup('Tags : <b>{}</b>'.format(form.tags.data)))
		return redirect('/form')
	return render_template('forms.html', title='Formulaire', form=form)


@app.route('/response')
def response():
	return render_template('response.html', title='response')


