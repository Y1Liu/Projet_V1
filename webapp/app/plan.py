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
import data_mining as dm
import networkx as nx
import dataframes as dtf
from math import sin, cos, acos, radians
import pandas as pd
from node import*
import sys
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
#Obtenir tous les enfants d'un noeud parent
"""
    IN : 
        node : noeud père
        df : matrice de données graphe (get_graph_matrix)
        overallScore : Dataframe city_id - score
        target : noeud cible
        optimization : Type d'otpimisation 'distance', 'time', 'affinity'
        filtre : Matrice 'df' filtrée par les conditions utilisateur
        distance_begin : distance réelle cumulée     
    OUT : 
        liste de nodes  
"""
def children(node, df, overallScore, target, optimization, filtre, distance_begin):
    children=[]
    d1=filtre.loc[filtre['cityDep_id']==node.city]['cityArr_id']
    d2=filtre.loc[filtre['cityArr_id']==node.city]['cityDep_id']
    d2=pd.concat([d1, d2])
    temp=d2.values[:]
    #Renvoie un tableau de noeuds
    for value in temp : 
        if(value != target.city):
            try:
                score=overallScore.loc[overallScore['City_id']==value]['Score'].values[0]
                parent=node
                H=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))]['heuristic'].values[0]
                G=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))][optimization].values[0]+distance_begin
                child=Node(value,score,parent,H,G)
                children.append(child)
            except:
                score=0
                parent=node
                H=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))]['heuristic'].values[0]
                G=df.loc[((df['cityDep_id']==value)&(df['cityArr_id']==target.city))|((df['cityDep_id']==target.city)&(df['cityArr_id']==value))][optimization].values[0]+distance_begin
                child=Node(value,score,parent,H,G)
                children.append(child)
        else : 
            children.append(target)
    return children


#Obtenir le noeud suivant en fonction de G et H 
"""
    IN : liste de nodes
    OUT : node
"""
def get_best_child(liste):
    for i in range(0, len(liste)):
        for j in range(i+1, len(liste)):
            x1=liste[i].H
            y1=liste[i].G
            x2=liste[j].H
            y2=liste[j].G
            if((x1+y1)>(x2+y2)):
                tmp=liste[i]
                liste[i]=liste[j]
                liste[j]=tmp
    return(liste[0])
 
    
#Obtenir le chemin optimal
"""
    IN : 
        start : node
        target : node
        df : matrice de données graphe (get_graph_matrix)
        overallScore : Dataframe city_id - score
        optimization : Type d'otpimisation 'distance', 'time', 'affinity'
        filtre : Matrice 'df' filtrée par les conditions utilisateur
    OUT :    
"""
def get_path(start, target, df, overallScore, optimization, filtre, df_cities):
    stack=[]
    result_id=[]
    stack.append(start)
    pere=start
    tmp=0
    distance_begin=0
    while(tmp!=target.city):
        x=children(pere, df, overallScore, target, optimization, filtre, distance_begin)
        #########################
        temp=x
        for node_s in stack:
            for node_c in x:
                if(node_s.city==node_c.city):
                    temp.remove(node_c)
        #########################
        child=get_best_child(temp)
        stack.append(child)
        pere=child
        tmp=stack[-1].city
        distance_begin += pere.G
    for obj in stack:
        result_id.append(obj.city)
    result_names=[]
    for obj in result_id:
        if (obj==1000):
            result_names.append(['Lille', 0])
        elif (obj==10000):
            result_names.append(['Marseille', 0])
        else:
            result_names.append([df_cities.iloc[int(obj)-1]['name'], overallScore.loc[overallScore['City_id']==obj]['Score'].values[0]])
    return result_names
###############################################################################