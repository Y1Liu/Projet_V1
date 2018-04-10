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
from collections import OrderedDict
import numpy as np
from graphdb import GraphDB
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


#Creation du fichier csv permettant de creer la table "similarities"
def createSimilarityHashtable(t, l):
    nSize=len(t)
    dico = OrderedDict()
    for i in range (0,nSize):
        for j in range (0,nSize):
            dico[''.join(l[i]),''.join(l[j])]=t[i][j]
    return dico


#prends la liste de tag et renvoie une matrice de similarité
def csvToHashtable(path_file):
    with open(path_file, 'r') as csvfile:
        tags=csv.reader(csvfile)
        l=list(map(tuple,tags))
        nSize=len(l)
        t=np.zeros((nSize-1, nSize-1),dtype='float')
        for i in range (0,nSize-1):
            for j in range (0,nSize-1):
                t[i][j]=getSimilarity(''.join(l[i]),''.join(l[j]))
    dico=createSimilarityHashtable(t, l)


#Initialisation de la base de données
def dbInit():
    db=GraphDB('/tmp/test_graph.db')
    for a in range(10):
        b = a + 1
        print(a, b)
        db.store_relation(a, 'comes_before', b)


csvToHashtable("../data/tags.csv")
dbInit()
###############################################################################
