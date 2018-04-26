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
import csv
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#prends deux mots en arguments et renvoie la mesure de similarité
def getSimilarity(str1, str2):
    word1=wordnet.synsets(str1)[0]
    word2=wordnet.synsets(str2)[0]
    s=word1.wup_similarity(word2)
    return(s)


#Création du csv contenant les similarités entre les mots contenus dans les tags
#Csv à importer dans la base de données
def similaritiesToCsv(path_file, return_file):
    #Récupération du fichier des villes
    with open(path_file, 'r') as csv_file:
        rd=csv.reader(csv_file)
        tags=list(rd)
    nSize=len(tags)
    print(nSize)
    #écriture dans le fichier contenant ID_tag1 | ID_Tag2 | Similarity
    with open(return_file, 'w') as csv_file:
        wr=csv.writer(csv_file)
        for i in range(0,nSize):
            for j in range(0,nSize):
                if(i <= j):
                    wr.writerow([i, j, getSimilarity(str(tags[i]), str(tags[j]))])
   
    
similaritiesToCsv('../data/tags.csv','../data/similaritiesTags.csv')
###############################################################################
