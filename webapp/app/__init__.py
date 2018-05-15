###############################################################################
#Fichier permettant l'initialisation de l'application
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#06/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from flask import Flask
from config import Config

from flask_bootstrap import Bootstrap

###############################################################################
#Initialisation de l'application
###############################################################################
#Creation de l'instance de l'appplication dans une variable globale
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


from app import routes