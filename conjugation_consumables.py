#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:56:20 2022

@author: tgrra
"""

def conjugation_consumables(conjugation_mix, ecoli_tubes):

    #For 1 run:
    consumables = {"96 deepwell plate": [3],
                    "300p tipbox": [11],
                    "1000p tipbox": [7],
                    "E. coli in 50ml Falcons": [6],
                    "Streptomyces in 15ml Falcons": [9]}

    conjugations_size = 0
    streptomyces_number = len(sorted(set([i[0] for i in conjugation_mix.values()])))

    for item in conjugation_mix:
        for i in range(len(conjugation_mix[item])):
            conjugations_size += 1

    if conjugations_size > 96:        
        consumables["96 deepwell plate 1"] = consumables["96 deepwell plate"]
        del consumables["96 deepwell plate"]
        consumables["96 deepwell plate 2"] = [2]
        
        consumables["300p tipbox 1"] = consumables["300p tipbox"]
        del consumables["300p tipbox"]
        consumables["300p tipbox 2"] = [10]
  

    if len(ecoli_tubes) > 6:
        consumables["E. coli in 50ml Falcons 1"] = consumables["E. coli in 50ml Falcons"]
        del consumables["E. coli in 50ml Falcons"]
        consumables["E. coli in 50ml Falcons 2"] = [5]

        
    if len(ecoli_tubes) > 12:
        consumebles["E. coli in 50ml Falcons 1"] = consumebles["E. coli in 50ml Falcons"]
        del consumebles["E. coli in 50ml Falcons"]
        consumebles["E. coli in 50ml Falcons 2"] = [4]

        
    if streptomyces_number > 16:
        consumables["Streptomyces in 15ml Falcons 1"] = consumables["Streptomyces in 15ml Falcons"]
        del consumables["Streptomyces in 15ml Falcons"]
        consumables["Streptomyces in 15ml Falcons 2"] = [8]

    return consumables