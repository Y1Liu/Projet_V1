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
    
    #Récupération de toutes les places et instanciation de objets
    temp = dm.getPlacesGps('../data/cities.csv', '../data/data_place.json')
    
###############################################################################
