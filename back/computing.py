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
import time
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
    
    
t1=time.time()
test=computeDepArr(dtf.paramsToDf("'driving'"), "Aumetz, France", "Limoges, France", ["Censier Daubenton, Paris"], "driving")
t2=time.time()-t1
print(t2)
###############################################################################
