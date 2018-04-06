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
from flask_caching import Cache
from config import Config
#from app.cache import cache
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate


###############################################################################
#Initialisation de l'application
###############################################################################
app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
#db = SQLAlchemy(app)
#migrate = Migrate
#app.config.from_object(cache)
#cache.init_app(app)

from app import routes