#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les données de la BDD au format DF
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#02/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import pandas as pd
import db
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant de mettre la table TYPE au format de DataFrame
def types_toDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT type.id, type.name FROM type', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table CITY au format de DataFrame
def cities_toDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT city.id, city.name, city.lat, city.lng FROM city', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PLACE au format de DataFrame
def places_toDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT place.id, place.name, place.photo, place.type, place.visits, place.lat, place.lng, place.city_id FROM place', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PARAMS au format de DataFrame
def params_toDf(mode):
    connexion=db.init_db()
    qr="SELECT param.id,param.time, param.distance, param.heuristic, param.cityDep_id, param.cityArr_id FROM param WHERE param.mode LIKE " + mode
    results=pd.read_sql(qr, connexion, index_col='id')
    return results


#Fonction permettant de mettre la table SIMILARITY au format de DataFrame
def similarities_toDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT similarity.id, similarity.type_id1, similarity.type_id2, similarity.similarity FROM similarity', connexion, index_col='id')
    return results


#Fonction permettant de mettre la table PLACETYPE au format de DataFrame
def placeTypes_toDf():
    connexion=db.init_db()
    results=pd.read_sql('SELECT placeTypes.place_id, placeTypes.word FROM placeTypes', connexion)
    return results
###############################################################################