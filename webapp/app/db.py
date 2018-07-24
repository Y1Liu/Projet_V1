#!/usr/bin/env python
# coding: utf-8
###############################################################################
#Initialisation de l'application app - base de données MONGODB
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#10/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from routes import app
import configparser
from flask_mongoengine import MongoEngine
###############################################################################


###############################################################################
#CONNEXION BDD
###############################################################################
cfg = configparser.ConfigParser()
cfg.read('conf.cfg')
user = cfg.get('DB', 'user')
password = cfg.get('DB', 'password')
app.config['MONGODB_SETTINGS'] = {'db': 'smartplanner_users', 'host': 'mongodb://'+user+':'+password+'@ds263660.mlab.com:63660/smartplanner_users'}
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
###############################################################################


###############################################################################
#DATABASE
###############################################################################
db=MongoEngine(app)
###############################################################################



