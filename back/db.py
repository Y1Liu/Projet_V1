###############################################################################
#Fichier base de données
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#10/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import pypyodbc
import pandas as pd
###############################################################################


###############################################################################
#FONCTION
###############################################################################
#Initialisation de la base de données
#Retourne le contexte
def init_db():
    cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
                            "Server=10.2.38.20;"
                            "Database=Planner;"
                            "uid=;pwd=")
    return cnxn


#Permet de réaliser une commande sql
def command(db_cmd):
    context=init_db()
    handler=context.cursor()
    res=handler.execute(db_cmd)


#Insertion des données dans la base pour le trajet témoin
def insertion():
    #Insertion des latitudes-longitudes
###############################################################################
