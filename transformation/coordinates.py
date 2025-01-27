#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 11:13:02 2022

@author: tgrra
"""

def transformation_coordinates(plasmids, competents):
    
    competent = [competents]*len(plasmids)
    competent_cells_plate = dict()
    for i in range(len(competent)):
        competent_cells_plate[competent[i] + "\n(" + str(i+1) + ")"] = i
        
    mix = dict()
    plasmid_list = list()
    
    for item in plasmids:
        plasmid_list.append(item)
        
    
    for i in range(len(plasmid_list)):
        mix[plasmid_list[i] + ":\n" + competent[i]] = i
    
    return mix, competent_cells_plate