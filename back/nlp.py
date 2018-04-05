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
#prends deux mots en qrguments et renvoie la mesure de similarité
def getSimilarity(str1, str2):
    word1=wordnet.synsets(str1+".n.01")
    word2=wordnet.synsets(str2+".n.01")
    print(word1.wup_similarity(word2))
    s=word1.wup_similarity(word2)
    return(s)


#prends la liste de tag et renvoie une matrice
def csvToMatrix(path_file):
    with open(path_file, 'r') as csvfile:
        tags=csv.reader(csvfile)
        #l = tags(map(tuple, csvfile))
        #l=len(tags)


s=getSimilarity("chien","chat")
print(s)
csvToMatrix("/home/pmaksud/Projet/data/tags.csv")
###############################################################################
