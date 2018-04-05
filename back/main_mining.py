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
from pyspark import *
from pyspark.sql.session import SparkSession
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == '__main__':

    #Création du spark context
    conf = pyspark.SparkConf().setAll([('spark.executor.memory', '2g'), ('spark.executor.cores', '4'),("spark.cores.max", "8"), ('spark.driver.memory','4g')])
    sc = pyspark.SparkContext.getOrCreate()
    sc.stop()
    sc = pyspark.SparkContext(master='local[*]', appName='SchedulerJob',conf=conf)
    spark = SparkSession(sc)
    #Récupération date
    [date_today, end_time] = dm.getDate()
    t1=time.time()
    #Récupérations des lieux autour
    #dm.getPlaces("/home/pmaksud/Projet/data/data_places.json", str(43.29609079999999), str(5.3698543))
    #Test récupération des données GPS : FONCTIONNE
    temp = dm.getGps("86 boulevard Haussmann, Paris\n")
    #Test de la récupération de route
    #t_waypoints = dm.np.array([[48.856614,2.3522219000000177],[48.390394,-4.486076]])
    t_waypoints = dm.np.array([])
    link=dm.getTrace("../data/data_route.json", str(49.357571), str(6.168426), str(43.300000), str(5.400000), t_waypoints)
    t2=time.time()
    #print("Temps de reception des données via API : ", t2-t1, " s")
    #Test de la récupération du trajet sous forme de tableau de coordonnées GPS
    dm.getTraceGps("../data/data_route.json", link, "../data/GPScoords.csv")
    dm.getPlaces(str(49.357571), str(6.168426))
    dm.getPlaceFromId("4c5c6cd16ebe2d7f060bd02e","/home/pmaksud/Projet/data/data_place.json")
    #Test de la récupération de tous les lieux autour du trajet et affichage
    test_places=dm.getPlacesGps("../data/GPScoords.csv")
    for Place in test_places:
            Place.displayPlace()
###############################################################################
