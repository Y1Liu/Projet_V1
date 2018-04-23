#!/usr/bin/env python
# coding: utf-8 

###############################################################################
#Fichier contenant les fonctions permettant de créer la base de données de tags et similarités entre mots
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#05/04/2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
from nltk.corpus import wordnet
import numpy as np
import csv
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#prends deux mots en arguments et renvoie la mesure de similarité
def getSimilarity(str1, str2):
    word1=wordnet.synsets(str1, 'n')[0]
    word2=wordnet.synsets(str2, 'n')[0]
    s=word1.wup_similarity(word2)
    return(s)


#prends la liste de tag et renvoie une matrice de similarité
def csvToSimilarities(path_file, return_file):
    with open(path_file, 'r') as csvfile:
        tags=csv.reader(csvfile)
        l=list(map(tuple,tags))
        nSize=len(l)
        t=np.zeros((nSize-1, nSize-1),dtype='float')
        for i in range (0,nSize-1):
            for j in range (0,nSize-1):
                t[i][j]=getSimilarity(''.join(l[i]),''.join(l[j]))
    #Création d'un csv avec toutes les similarités associées. 
    #Indice du mot 1 | Indice du mot2 | Similarité
    with open(return_file, 'w') as csvfile:
        wr = csv.writer(csvfile)
        for i in range (0,nSize-1):
            for j in range (0,nSize-1):
                if(i<=j):
                    wr.writerow([str(i) ,str(j), str(t[i][j])])


csvToSimilarities("../data/tags.csv", "../data/similarities.csv")
###############################################################################
