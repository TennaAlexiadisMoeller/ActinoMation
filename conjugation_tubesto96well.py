#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:08:01 2022
Originally created as part of a PhD project started in 2022
@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Conjugation protocol with tubes - OT 1000 tips',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for transferring a number of 50mL tube(s) and 15mL tube(s) into 96 PCR plate(s)',
    'apiLevel': '2.4'
}

""" Variables"""


default_uses = {"EcoliA":["strept1","strept2","strept3"], "EcoliB":["strept1","strept2","strept3","strept4"]}

ecoli_uses = default_uses  # overwritten by notebook runner

ecoli_tubes = ["EcoliA","EcoliB"]

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions

def run(protocol: protocol_api.ProtocolContext):
    
    """ load labware """
    source_50tubes =  [
        protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', location = '6'),  
        protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', location = '5'),
    ]
    
    source_15tubes = [protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location = '9'),
                      protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location = '8')
                      ]
    dest_plates = [protocol.load_labware('nest_96_wellplate_2ml_deep', location = '3'),
                   protocol.load_labware('nest_96_wellplate_2ml_deep', location = '2')
                  ]
    
    """ load pipettes """
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_1000ul', location = '7')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '11')
    p1000 = protocol.load_instrument('p1000_single', 'left', tip_racks=[tiprack_1])
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_2])
    
    tip_placement = {i + 1: char for i, char in enumerate(reversed("ABCDEFGH"))}
    well_placement = "ABCDEFGH"
    tubes50_placement = {1:'A1', 2:'A2', 3:'A3', 4:'B1', 5:'B2', 6:'B3'}
    tubes15_placement = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C2', 'C3', 'C4', 'C5']

    
    
    """Transfer of E.coli tubes to 96-well plate"""
    
    #150ul per well (up to 6 wells, plus 10ul) aspirated then 150ul is dispensed, more is collected (if necessary)              
    well = 0
    col = 1
    strepto_placement = {key: {} for key in ecoli_tubes}

    uses_needed = {k: len(v) for k, v in ecoli_uses.items()}

    for source_tube, source_name in enumerate(ecoli_tubes, start = 1):
        used = 0
        needed_in_total = uses_needed[source_name]
        strepto = ecoli_uses[source_name]
        strepto_well = strepto_placement[source_name]
        
        tube_row = source_tube % 6  # % the remainder of row divided by 6
        tubes = source_50tubes[source_tube // 6]  # // integer division - the floor of row divided by 6
        tube = tubes[tubes50_placement[tube_row]].bottom(2)
        p1000.pick_up_tip()
        
        while used < needed_in_total:
            volume = (150 * min(needed_in_total - used, 6))+10
            p1000.aspirate(
                volume, # volume to collect
                tube  # which tube to aspirate from
            )
                
            fill_well = well

            for i in range(used, min(needed_in_total, used + 6)):
                
                plate_well = well_placement[well % 8]

                p1000.dispense(
                    150, #volume dispensed
                    dest_plates[0][plate_well + str(col)]) #destination on mix plate
                
                if strepto[i] in strepto_well.keys():
                    strepto_well[strepto[i]] += "," + plate_well + str(col)
                
                else:
                    strepto_well[strepto[i]] = plate_well + str(col)

                well += 1
                used += 1
                if well == fill_well + 6:
                    break


                if well % 8 == 0:
                    col += 1 

        #p1000.return_tip()
        p1000.drop_tip()
    
    """Transfer from streptomyces plate to 96-well plate"""
       
    #Preparing necessary locations of the streptomyces based on where the E.coli is pipetted

    strepto_wells = dict()
    for ecoli in strepto_placement:

        for strepto in strepto_placement[ecoli]:

            well_strepto = strepto_placement[ecoli][strepto]
            wells_split = well_strepto.split(",")

            if strepto in strepto_wells.keys():
                strepto_wells[strepto] += wells_split

            else:

                strepto_wells[strepto] = wells_split
                

    #155ul aspirated then 150ul is dispensed, then it is mixed
    strepto_amount = 1
    strepto_rack = 0
    dest_well = 1
    dest_plate = 0
    
    for strepto in strepto_wells:

        rack15 = source_15tubes[strepto_rack] 
        tube15 = rack15[tubes15_placement[strepto_amount-1]]
        well96 = dest_plates[dest_plate]
     
        for i in range(len(strepto_wells[strepto])):

            p300.pick_up_tip()
            p300.aspirate(
                    155, # volume to collect
                    tube15  # which tube to aspirate from
            )
            p300.dispense(
                150,
                well96[strepto_wells[strepto][i]]
            )
            
            p300.mix(2, #Times it mixes
                     200, #Volume it mixes
                     well96[strepto_wells[strepto][i]]
                    )
            
            #p300.return_tip()
            p300.drop_tip()
            
            dest_well += 1


        strepto_amount += 1

        if strepto_amount > 15:
            strepto_amount = 1
            strepto_rack += 1
          
        if dest_well > 96:
            dest_well = 1
            dest_plate += 1

        