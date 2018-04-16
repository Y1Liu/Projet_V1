#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#Fichier appelant les fonctions permettant la récupération des données au format JSON
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#15/03/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import data_mining as dm
import random
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import pyspark
import os
import time
import place as p
import db
from pyspark import *
from pyspark.sql.session import SparkSession
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == '__main__':

    #Création du spark context
    #conf = pyspark.SparkConf().setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '4'),("spark.cores.max", "8"), ('spark.driver.memory','4g')])
    #sc = pyspark.SparkContext.getOrCreate()
    #sc.stop()
    #sc = pyspark.SparkContext(master='local[*]', appName='SchedulerJob',conf=conf)
    #spark = SparkSession(sc)
    
    #Définition des adresses du trajet témoin
    adresse_dep="Lille, France"
    adresse_arr="Paris, France"
    waypoint="Amiens, France"
    
    #récupération des lat lng
    latDep=dm.getGps(adresse_dep)[0,0]
    lngDep=dm.getGps(adresse_dep)[0,1]
    latWayp=dm.getGps(adresse_arr)[0,0]
    lngWayp=dm.getGps(adresse_arr)[0,1]
    latArr=dm.getGps(waypoint)[0,0]
    lngArr=dm.getGps(waypoint)[0,1]

    #Création des fichiers de données coordonnées 
    temp=dm.getTrace("../data/dataroute_car.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "driving")
    dm.getTraceGps("../data/GPS_car.csv", temp)
    temp=dm.getTrace("../data/dataroute_foot.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "walking")
    dm.getTraceGps("../data/GPS_foot.csv", temp) 
    temp=dm.getTrace("../data/dataroute_transit.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "transit")
    dm.getTraceGps("../data/GPS_transit.csv", temp)   
    temp=dm.getTrace("../data/dataroute_car_.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "driving")
    dm.getTraceGps("../data/GPS_car_.csv", temp)   
    temp=dm.getTrace("../data/dataroute_foot_.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "walking")
    dm.getTraceGps("../data/GPS_foot_.csv", temp)  
    temp=dm.getTrace("../data/dataroute_transit_.json", latDep, lngDep, latArr, lngArr, [latWayp, lngWayp], "transit")
    dm.getTraceGps("../data/GPS_transit_.csv", temp)
###############################################################################
