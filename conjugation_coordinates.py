#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 11:13:02 2022

@author: tgrra
"""

def coordinates(ecoli_uses, ecoli_tubes):

    well_placement = ['A','B','C','D','E','F','G','H']
    tubes_placement = {1:'A1',2:'A2',3:'A3', 4:'B1',5:'B2',6:'B3'}

    well = 0
    col = 1
    strepto_placement = {key: {} for key in ecoli_tubes}
    ecoli_placement = {key: {"volume":[],
                             #"tube":"",
                             "wells":[]} for key in ecoli_tubes}

    uses_needed = {k: len(v) for k, v in ecoli_uses.items()}

    for source_tube, source_name in enumerate(ecoli_tubes, start = 1):
        used = 0
        needed_in_total = uses_needed[source_name]
        strepto = ecoli_uses[source_name]
        strepto_well = strepto_placement[source_name]
        tube = tubes_placement[source_tube]

        while used < needed_in_total:
            ecoli_placement[source_name]["volume"].append((150 * min(needed_in_total - used, 6))+20)
            #ecoli_placement[source_name]["tube"] = tube
            fill_well = well

            for i in range(used, min(needed_in_total, used + 6)):
                plate_well = well_placement[well % 8]
                ecoli_placement[source_name]["wells"].append(plate_well + str(col))

                strepto_well[strepto[i]] = plate_well + str(col)

                well += 1
                used += 1
                if well == fill_well + 6:
                    break


                if well % 8 == 0:
                    col += 1 

    strepto_wells = dict()
    for ecoli in strepto_placement:

        for strepto in strepto_placement[ecoli]:

            if strepto in strepto_wells.keys():
                strepto_wells[strepto].append(strepto_placement[ecoli][strepto])

            else:
                strepto_wells[strepto] = [strepto_placement[ecoli][strepto]]
    
    return ecoli_placement, strepto_placement