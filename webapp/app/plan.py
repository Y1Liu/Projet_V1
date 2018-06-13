#!/usr/bin/env python
# coding: utf-8 


###############################################################################
#Fichier contenant les fonction de planification
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#juin 2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import computing as cp
import networkx as nx
###############################################################################


###############################################################################
#VALEURS DE TEST
###############################################################################
add_dep=" "
add_arr=" "
waypoint=" "
mode=" "
tab_tags=['Art', 'Museum']
#optimization='time'
optimization='distance'
#optimization='affinity'
#Durée Maximale sans pause (s)
t_max=7200
#Duree maximale du repas (s)
eat=900
#Dist maximale (m)
dist_max=300000
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
def get_heuristic(a, b):
    print(a)
    print(b)
    #heuristic=0
    heuristic=temp.loc[((temp['cityDep_id']==a) & (temp['cityArr_id']==b))|((temp['cityDep_id']==b) & (temp['cityArr_id']==a))]['heuristic'].values[0]
    return heuristic


def get_bestway():
    #########################################################################################################################  
    if(optimization=='distance'):
        temp=matrix.loc[matrix['distance']<=dist_max]
        A=nx.from_pandas_edgelist(temp, source='cityDep_id', target='cityArr_id', edge_attr=['distance', 'heuristic', 'time'])
        #t=nx.astar_path(A, source=1000, target=10000, heuristic=computeH, weight='distance')
        t=nx.shortest_path(A, source=1000, target=10000, weight='distance')
    #########################################################################################################################
    elif(optimization=='time'):
        temp=matrix.loc[matrix['time']<=t_max]
        A=nx.from_pandas_edgelist(temp, source='cityDep_id', target='cityArr_id', edge_attr=['distance', 'heuristic', 'time'])
        #t=nx.astar_path(A, source=1000, target=10000, heuristic=computeH, weight='time')
        t=nx.shortest_path(A, source=1000, target=10000, weight='time')
    #########################################################################################################################
    elif(optimization=='affinity'):
        #A=nx.from_pandas_edgelist(matrix, source='cityDep_id', target='cityArr_id', edge_attr=['distance', 'heuristic', 'time'])
        #t=nx.astar_path(A, source=1000, target=10000, heuristic=computeH, weight='distance')
        #t=nx.longest_path(A, source=1000, target=10000, weight='ScoreCity2')
        print(1)
    print(t)
###############################################################################