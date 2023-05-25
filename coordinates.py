#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 11:13:02 2022

@author: tgrra
"""

def conjugation_coordinates(ecoli_uses):

    strepto_list = list()
    mix_dict = dict()
    n = 0
    num = 2

    for ecoli in ecoli_uses:
        for strepto in ecoli_uses[ecoli]:
            
            
            if strepto not in strepto_list:
                strepto_list.append(strepto)
            
            
            if ecoli + "::\n" + strepto in mix_dict:
                
                if ecoli + "::\n" + strepto + "(" + str(num) + ")" in mix_dict:
                    num += 1
                
                mix_dict[ecoli + "::\n" + strepto + "(" + str(num) + ")"] = n
            
            else:
                mix_dict[ecoli + "::\n" + strepto] = n
                num = 2
            
            n += 1
            
    return strepto_list, mix_dict


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