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
from flask import Flask, render_template, flash, redirect, Markup, request, url_for, session
from werkzeug.contrib.cache import SimpleCache
import computing as cp
###############################################################################


###############################################################################
#CONSTANTES
###############################################################################
CACHE_TIMEOUT = 60 #Définit le timeout du cache à 60 secondes
cache = SimpleCache()
spark=cp.getsparkContext()
print("SPARK CONTEXT DONE")
tags_user=[]
datas=cp.initMatrix(spark)
print("GET MATRIX DONE")
app = Flask(__name__)
###############################################################################


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
@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        #data = request.get_json()
        #tags = data['tags_users']
        tags_user = ['Art', 'Rock']
    tags_user = ['Art', 'Rock']
    test=cp.getWay(tags_user, cp.getClassement(datas[2], tags_user, spark, datas[1], datas[3], datas[0])[0].toPandas(), 2, datas[0])
    return render_template('test.html', title='test', test=test)
		   

@app.route('/map')
def map():
	depart=session.get("depart",None)
	arrivee=session.get("arrivee", None)
	escales=session.get("escales", None)
	return render_template('map.html', title='Map', depart=depart, arrivee=arrivee, escales=escales)
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == '__main__':
    app.run(debug=False)
###############################################################################

