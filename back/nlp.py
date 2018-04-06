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


#Creation du fichier csv permettant de creer la table "similarities"
def createSimilarityCSV(path_file, t, l):
    with open(path_file, 'w+') as csvfile:
        word=csv.writer(csvfile, delimiter=',')
        word.writerow(['similarity_id:ID', 'word_id1', 'word_id2', 'similarity:float'])
        nSize=len(t)
        for i in range (0,nSize):
            for j in range (0,nSize):
                word.writerow(["s"+str(i)+str(j),''.join(l[i]),''.join(l[j]), t[i][j]])


#prends la liste de tag et renvoie une matrice de similarité
def csvToMatrix(path_file):
    with open(path_file, 'r') as csvfile:
        tags=csv.reader(csvfile)
        l=list(map(tuple,tags))
        nSize=len(l)
        t=np.zeros((nSize-1, nSize-1),dtype='float')
        for i in range (0,nSize-1):
            for j in range (0,nSize-1):
                t[i][j]=getSimilarity(''.join(l[i]),''.join(l[j]))
        print(t)
        createSimilarityCSV("../data/similarities.csv", t, l)
    return(t)


csvToMatrix("../data/tags.csv")
###############################################################################
