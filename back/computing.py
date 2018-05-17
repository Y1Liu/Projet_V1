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
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import IntegerType
import pyspark
###############################################################################


###############################################################################
#Création du spark context
###############################################################################
sc = pyspark.SparkContext.getOrCreate()
conf = pyspark.SparkConf()
conf.setAppName('SmartPlanner')
conf.setMaster('spark://10.2.68.52:7077')
conf.set('spark.executor.memory', '8g')
conf.set('spark.executor.cores', '3')
conf.set('spark.cores.max', '9')
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
#df_types=spark.createDataFrame(df_types)
#Récupération de la matrice de similarité sous forme de dataframe
df_similarities=dtf.similaritiesToDf()
#Spark DataFrame
#df_similarities=spark.createDataFrame(df_similarities)
#Récupération de la matrice de placeTypes sous forme de dataframe
df_placeTypes=dtf.placeTypesToDf()
#Spark DataFrame
#df_placeTypes=spark.createDataFrame(df_placeTypes)
#Récupération de la matrice de placesSimilarity sous forme de dataframe
#Spark DataFrame
placesSimilarities=spark.read.format('csv').option('header', 'true').load('../data/placesSimilarities.csv')
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
    words1=df_placeTypes[df_placeTypes.place_id==id_place1]['word']
    words2=df_placeTypes[df_placeTypes.place_id==id_place2]['word']
    #Récupération du nombre de tag par id 
    nb1=len(words1)
    nb2=len(words2)
    #print(words1)
    #print(words2)
    nb_ind=nb1+nb2
    for i in range(0,nb1):
        for j in range(0, nb2):
            result=df_similarities[((df_similarities.type_id1==words1.iloc[i]) & (df_similarities.type_id2==words2.iloc[j]))^((df_similarities.type_id1==words2.iloc[j]) & (df_similarities.type_id2==words1.iloc[i]))]['similarity']
            if(words1.iloc[i]!=words2.iloc[j]):
                score=score+result.iloc[0]
            else:
                score=score+1
            #print(score)
    return score/nb_ind


#Fonction créant la matrice de similarité entre les évenements
def placesSimilarities():
    #Création de la DataFrame carrée avec des similarités de 0
    temp=df_placeTypes['place_id'].unique()
    print(len(temp))
    df_sim=pd.DataFrame(np.zeros((len(temp),len(temp))), columns=list(temp), index=list(temp))
    #Boucle peuplant la matrice avec les similarités calculées
    for i in range(1, len(temp)):
        for j in range(1, len(temp)):
            #évite de recommander le même point d'intéret
            if(i!=j):
                print(temp[i]+", "+temp[j]+" : "+str(getSimilarity(temp[i], temp[j])))
                df_sim.loc[[temp[i]],[temp[j]]]=getSimilarity(temp[i], temp[j])
    return(df_sim)


#Fonction permettant de lire les Tags données par l'utilisateur 
#Retourne la liste des meilleurs events pour chaque tag
def computeRecommandation(tab_tags):
    #Passage en SparkDataframes
    #Nombre de tags saisis par l'utilisateur
    user_tags=[]
    nSize=len(tab_tags)
    #CONSTRUCTION DE LA MATRICE DE SIMILARITE ENTRE LES EVENEMENTS
    #Récupération des id de tags choisis par l'utilisateur
    for i in range(0, nSize):
        user_tags.append(int(df_types.index[df_types.name==tab_tags[i]].get_values()[0]))
    return 0
###############################################################################