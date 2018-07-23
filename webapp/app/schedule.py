#!/usr/bin/env python
# coding: utf-8


###############################################################################
#Fichier contenant les fonction de planification horaire horaire
#Par Arnaud Duhamel et Robin Cavalieri
#Planificateur intelligent
#SOLUTEC Paris
#juillet 2018
###############################################################################


###############################################################################
#LIBRAIRIES
###############################################################################
import datetime
import pandas as pd
import numpy as np
###############################################################################


###############################################################################
#FONCTIONS
###############################################################################
"""
    Retourne en seconde une heure au format HH:MM
    IN : 
        time_str : str(heure au format HH:MM)    
    OUT : 
        int(heure en seconde)
"""
def get_sec(time_str):
    h, m = time_str.split(':')
    return int(h) * 3600 + int(m) * 60


"""
    Permet à l'utlisateur de planifier sur le plan temporel le trajet 
    Arrêt du trajet à partir de 22h et reprise à 9h
    IN : 
        t_dep : str(heure départ "HH:MM")
        t_arr : str(heure arrivée "HH:MM")
        d_repas : int(temps du repas en seconde)
        df : dataframe avec les paramètres trajets (distance, heuristique, temps)
        result_plan : 
    OUT : 
        str_heures : str(["10:21", "20:10, "", ..."])
"""
def schedule_str(t_dep, t_arr, df, result_plan):
    t_dep_conv=get_sec(t_dep)
    t_arr_conv=get_sec(t_arr)
    heures=[t_dep_conv]
    str_heures=[]
    t=t_dep_conv
    for i in range(0, len(result_plan)-1):
        delta=df.loc[((df['cityDep_id']==result_plan[i])&(df['cityArr_id']==result_plan[i+1])) ^ ((df['cityDep_id']==result_plan[i+1])&(df['cityArr_id']==result_plan[i])), 'time'].values[0]
        t=t+delta
        #print(t)
        heures.append(t)
    for i in range(0, len(heures)):
        #Arret après 22h
        if(heures[i]>=79200):
            index=i
            break
    #Début de la journée à 9:00
    delta_t=32400-heures[index]
    for k in range(index, len(heures)):
        heures[k]=heures[k]+delta_t
    for x in heures:
        str_heures.append(str(datetime.timedelta(seconds=int(x))))
    return str_heures
###############################################################################