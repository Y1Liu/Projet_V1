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
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
"""
    OUT :   
        ________
        tags(str)
        ________  
"""
#Fonction permettant de mettre la table TYPE au format de DataFrame
def types_toDf():
    results=pd.read_csv('../../data/tags.csv', names=['name'])
    return results


"""
    OUT :   
        __________________________________________
        City_id | name(str)| lat(float)|lng(float)
        ________|__________|___________|__________
"""
#Fonction permettant de mettre la table CITY au format de DataFrame
def cities_toDf():
    results=pd.read_csv('../../data/cities.csv', names=['id', 'name', 'lat', 'lng'], encoding='latin-1')
    return results


"""
    OUT :     
        _______________________________________________________
        id | name | photo | type | lat | lng | visits | city_id
        _______________________________________________________
"""
#Fonction permettant de mettre la table PLACE au format de DataFrame
def places_toDf():
    results=pd.read_csv('../../data/all_places.csv')
    results
    return results


"""
    OUT :    
        _______________________________________________________________________
        mode | time | distance | heuristique | id city départ | id city arrivée
        _____|______|__________|_____________|________________|________________
"""
#Fonction permettant de mettre la table PARAMS au format de DataFrame
def params_toDf(mode):
    results=pd.read_csv('../../data/params.csv', names=['mode', 'time', 'distance', 'heuristic', 'cityDep_id', 'cityArr_id'])
    results=results.loc[results['mode']==mode]
    results=results.iloc[:, 1:]
    return results


"""
    OUT :     
        _____________________________________
        id_tag1 | id_tag2 | similarity(float)
        ________|_________|__________________
"""
#Fonction permettant de mettre la table SIMILARITY au format de DataFrame
def similarities_toDf():
    results=pd.read_csv('../../data/similaritiesTags.csv', names=['type_id1', 'type_id2', 'similarity'])
    return results


"""
    OUT :    
        _________________
        place_id | id_tag
        _________|_______
"""
#Fonction permettant de mettre la table PLACETYPE au format de DataFrame
def placeTypes_toDf():
    results=pd.read_csv('../../data/placeTags.csv', names=['place_id', 'word'])
    return results
###############################################################################