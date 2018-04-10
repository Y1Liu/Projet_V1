###############################################################################
#Fichier base de données
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#10/04/2018
#Les fonctions d'insertion dans la BDD sont encascadées selon les dépendances 
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
    connexion = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
        "Server=10.2.38.20;"
        "Database=Planner;"
        "uid=;pwd=")
    return connexion


#Permet de réaliser une commande sql
def command(db_cmd):
    context=init_db()
    handler=context.cursor()
    res=handler.execute(db_cmd)


#Insertion des parametres dans la BDD : time | distance | heuristic | position_id(FK)
def insert_param(lat, lng, position_id):
    command("INSERT INTO param (time, distance, heuristic) VALUES ("+lat+","+lng+","+position_id+")")


#Insertion des position dans la BDD : lat | lng | trajet_id(FK)
def insert_positions(coords_car, coords_foot, coords_transit, coords_car_, coords_foot_, coords_transit_):
    nSize=len(coords_car)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_car[0][0]+","+coords_car[0][1]+",1)")
        insert_param(coords_car[0][0], coords_car[0][1], 1)
    nSize=len(coords_foot)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_foot[0][0]+","+coords_foot[0][1]+",2)")
        insert_param(coords_foot[0][0], coords_foot[0][1], 2)
    nSize=len(coords_transit)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_transit[0][0]+","+coords_transit[0][1]+",3)")
        insert_param(coords_transit[0][0], coords_transit[0][1], 3)
    nSize=len(coords_car_)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_car_[0][0]+","+coords_car_[0][1]+",4)")
        insert_param(coords_car_[0][0], coords_car_[0][1], 4)
    nSize=len(coords_foot_)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_foot_[0][0]+","+coords_foot_[0][1]+",5)")
        insert_param(coords_foot_[0][0], coords_foot_[0][1], 5)
    nSize=len(coords_transit_)
    for i in range (0,nSize):
        command("INSERT INTO position (lat,lng,trajet_id) VALUES ("+coords_transit_[0][0]+","+coords_transit_[0][1]+",6)")
        insert_param(coords_transit_[0][0], coords_transit_[0][1], 6)
###############################################################################
