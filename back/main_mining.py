#!/usr/bin/env python
# coding: utf-8 

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
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import place as p
import computing as cp
###############################################################################


###############################################################################
#MAIN
###############################################################################
if __name__ == '__main__':
    #db.placesToCsv()
    #dm.getTypes()
    #dm.placeTags("../data/tags.csv", "../data/placeTags.csv")
    #dm.paramsToCsv("../data/cities.csv", "../data/params_final.csv")
    #dm.clearParams()
    cp.placesSimilarities()
    result=cp.getSimilarity('4cd5555fa5b34688a1248d50','4adcda10f964a520af3521e3')
    print(result)
    #cp.computeRecommandation(["Rock","Art","Museum"], spark)
###############################################################################