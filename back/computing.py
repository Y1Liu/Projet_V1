#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction permettant de réaliser les calculs de trajet
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/01/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import data_mining as dm
import dataframes as dtf
import pandas as pd
import numpy as np
from pyspark.sql.session import SparkSession
import pyspark
###############################################################################


###############################################################################
#Création du spark context
###############################################################################
sc = pyspark.SparkContext.getOrCreate()
conf = pyspark.SparkConf()
conf.setAppName("SmartPlanner")
conf.setMaster('spark://10.2.68.52:7077')
conf.set('spark.executor.memory', '8g')
conf.set('spark.executor.cores', '3')
conf.set('spark.cores.max', '20')
conf.set('spark.logConf', True)
sc.stop()
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)
###############################################################################


###############################################################################
#IMPORT DES MATRICES DE DONNEES SOUS FORME DE DataFrames
###############################################################################
#Récupération de la matrice de types sous forme de dataframe
df_types=dtf.typesToDf()
#Spark DataFrame
df_types=spark.createDataFrame(df_types)
#Récupération de la matrice de similarité sous forme de dataframe
df_similarities=dtf.similaritiesToDf()
#Spark DataFrame
df_similarities=spark.createDataFrame(df_similarities)
#Récupération de la matrice de placeTypes sous forme de dataframe
df_placeTypes=dtf.placeTypesToDf()
#Spark DataFrame
df_placeTypes=spark.createDataFrame(df_placeTypes)
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Fonction permettant de retourner une Dataframe avec les distances, temps entre les villes avec le lieu de départ et d'arrivée de l'utilisateur
def computeDepArr(df, addDep, addArr, wayPoints, mode): 
    #Récupération des coordonnées depuis les adresses fournies
    coordDep=dm.getGps(addDep)
    coordArr=dm.getGps(addArr)
    rows=[]
    temp=len(wayPoints)
    #Récupération de la dataframe contenant les villes
    cities=dtf.citiesToDf()
    nSize=len(cities)
    #Appel de la fonction permettant de calculer la distance d'un point à tous les autres
    for i in range(0,nSize):
        #Obtention des paramètres depuis le lieu de départ 
        distDuree=dm.getDistance_Duree(coordDep[0], coordDep[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
        rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, i])
        #Obtention des paramètres depuis le lieu d'arrivée 
        distDuree=dm.getDistance_Duree(coordArr[0], coordArr[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
        rows.append([distDuree[1], distDuree[2], distDuree[3], 10000, i])
        if(temp>0):
            print("Waypoints with cities")
            #Obtention des paramètres depuis les Waypoints
            for j in range(0,temp):
                coordWayp=dm.getGps(wayPoints[j])
                #Pour toutes les villes
                distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], str(cities.iloc[i][1]), str(cities.iloc[i][2]), mode)
                rows.append([distDuree[1], distDuree[2], distDuree[3], 100000+j, i])
    if(temp>0):
        print("Waypoints with start and arrival")
        #Obtention des paramètres depuis les Waypoints
        for j in range(0,temp):
            #Depuis le départ
            distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], coordDep[0], coordDep[1], mode)
            rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, 100000+j])
            #Depuis l'arrivée
            distDuree=dm.getDistance_Duree(coordWayp[0], coordWayp[1], coordArr[0], coordArr[1], mode)
            rows.append([distDuree[1], distDuree[2], distDuree[3], 10000, 100000+j])
    print("Start - Arrival")
    #Calcul des paramètres entre le départ et l'arrivée
    distDuree=dm.getDistance_Duree(coordDep[0], coordDep[1], coordArr[0], coordArr[1], mode)
    rows.append([distDuree[1], distDuree[2], distDuree[3], 1000, 10000])
    df1=pd.DataFrame(rows)
    #Retourne la nouvelle DataFrame
    return(df1)


#Fonction permettant de mesurer la similarité entre 2 places
def getSimilarity(id_place1, id_place2):
    score=0.0
    #Récupération des tag_id de chaque place
    words1=df_placeTypes.filter(df_placeTypes["place_id"]==id_place1).select("word")
    words1.show()
    words2=df_placeTypes.filter(df_placeTypes["place_id"]==id_place2).select("word")
    words2.show()
    #Récupération du nombre de tag par id 
    nb_ind=words1.count()+words2.count()
    print(nb_ind)
    #Calcul des similarités croisées 
    for row1 in words1:
        for row2 in words2:
            #result=spark.sql("SELECT similarity FROM similarity WHERE type_id1='"+row1+"' AND type_id2='"+row2+"' OR type_id1='"+row2+"' AND type_id2='"+row1)
            result=df_similarities.filter((df_similarities["type_id1"]==row1 & df_similarities["type_id2"]==row2) | (df_similarities["type_id2"]==row1 & df_similarities["type_id1"]==row2))
            score=score+result["similarity"]
    return score/nb_ind


#Fonction créant la matrice de similarité entre les évenements
def placesSimilarities():
    #Création de la DataFrame carrée avec des similarités de 0
    temp=df_placeTypes.toPandas()['place_id'].unique()
    print(len(temp))
    df_sim=pd.DataFrame(np.zeros((len(temp),len(temp))), columns=list(temp), index=list(temp))
    #Boucle peuplant la matrice avec les similarités calculées
    

#Fonction permettant de lire les Tags données par l'utilisateur 
#Retourne la liste des villes triées selon les gôuts de l'utilisateur 
def computeRecommandation(tab_tags):
    #Nombre de tags saisis par l'utilisateur
    #CONSTRUCTION DE LA MATRICE DE SIMILARITE ENTRE LES EVENEMENTS
    #Récupération de toutes les place_id
    temp=df_placeTypes.toPandas()['place_id'].unique()
    nPlaces=len(temp)
###############################################################################