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
#from werkzeug.contrib.cache import SimpleCache
import computing as cp
import plan as pl
from node import *
import sys
import json
from time import sleep
import sys
###############################################################################


###############################################################################
#CONSTANTES
###############################################################################
#CACHE_TIMEOUT = 60 #Définit le timeout du cache à 60 secondes
#cache = SimpleCache()
tags_user=[]
datas=cp.init_matrix()
app = Flask(__name__)
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant la mise en cache des données
#Permet de mettre en cache des objets individuels comme le résultat d'une requête
"""class cached(object):

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
"""


#Fonction créant la page du formulaire de renseignements
#Renvoie les choix de l'utilisateur sous forme de liste après soumission du formulaire
#Utilise la classe cached pour garder les données en cache
@app.route('/', methods=['GET','POST'])
def index():
    #Hif(request.method == 'POST'):
     #   data = request.get_json()
     #   #test=[['Paris',1]]
     #   tags = data['tags_users']
     #   tags_user=list(tags)
     #   with open('test1.json', 'w') as json_file:
     #       json.dump(data, json_file, indent=4)
     #   test=cp.get_way(tags_user, cp.get_classement(datas[2], tags_user, datas[1], datas[3], datas[0])[0], 1, datas[0])
        #session["test"]=test
    #else:
    #    tags_user = ['Art']
    #    with open('test1.json', 'w') as json_file :
    #        json.dump(tags_user, json_file, indent=4)
    #    test=cp.get_way(tags_user, cp.get_classement(datas[2], tags_user, datas[1], datas[3], datas[0])[0], 1, datas[0])

        #tags_user=tags_user
        #test=cp.get_way(tags_user, cp.get_classement(datas[2], tags_user, datas[1], datas[3], datas[0])[0], 1, datas[0])

    start=Node(56, 0, None, 0, 0)
    target=Node(2, 0, None, 0, 0)
    if request.method == 'POST':
        data = request.get_json()
        tags = data['tags_users']
        tags_user=list(tags)
        optimisation = data['optimisation']
        dep = data['depart']
        arr = data['arrivee']
        mode = data['transport']
        pause = data['tps_max']
        overallScore = cp.get_classement(datas[2], tags_user, datas[1], datas[3], datas[0])[0]
        df=cp.get_graph_matrix(dep, arr, [], mode, overallScore)
        df_filtered = df.loc[df['time']<=pause]
        
        #if (optimisation == 'distance' or optimisation == 'time'):
     #   test=[['Marseille',0]]
        #test=pl.get_path(start, target, df, overallScore, optimisation, df_filtered, datas[0])
            
    else:
        tags_user=['Art']
        optimisation='distance'
        dep='Lille'
        arr='Marseille'
        mode='driving'
        overallScore=5
        pause=7200
        df=cp.get_graph_matrix(dep, arr, [], mode, overallScore)
        df_filtered = df.loc[df['time']<=pause]
        #test=pl.get_path(start, target, df, overallScore, optimisation, df_filtered, datas[0])
        #    test=[['Lyon',0]]
    test=cp.get_way(tags_user, cp.get_classement(datas[2], tags_user, datas[1], datas[3], datas[0])[0], 1, datas[0])
    return render_template('index.html', title='test', test=test)
		   

#@app.route('/map')
#def map():
	#test=session.get("test",None)
	#return render_template('map.html', title='Map', test=test)
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == '__main__':
    app.run(debug="true")
###############################################################################

