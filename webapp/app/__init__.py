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
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate


###############################################################################
#Initialisation de l'application
###############################################################################
#Creation de l'instance de l'appplication dans une variable globale
app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)
#migrate = Migrate


from app import routes