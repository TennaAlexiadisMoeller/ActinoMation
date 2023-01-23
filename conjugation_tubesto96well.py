#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 09:08:01 2022

@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Conjugation protocol with tubes',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for transferring a number of 50mL tube(s) and 12-well plate(s) into 96 PCR plate(s)',
    'apiLevel': '2.4'
}

""" Variables"""

#num = 1 #num of runs

default_uses = {
    "EcoliA":["strept1","strept2","strept3"], "EcoliB":["strept1","strept2","strept3","strept4"],
    "EcoliC":["strept2","strept3"], 
    "EcoliD":["strept1","strept2","strept3","strept4","strept5","strept6","strept7"]
}

ecoli_uses = default_uses  # overwritten by notebook runner

ecoli_tubes = ["EcoliA","EcoliB","EcoliC","EcoliD"]

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions

def run(protocol: protocol_api.ProtocolContext):
    
    """ load labware """
    source_tubes =  [
        protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', location = '6'),  
        protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', location = '5'),
    ]
    
    source_12plates = [protocol.load_labware('nest_96_wellplate_2ml_deep', location = '9'),
                      ]
    dest_plates = [protocol.load_labware('nest_96_wellplate_2ml_deep', location = '3'),
                  ]
    
    """ load pipettes """
    tiprack_1 = protocol.load_labware('geb_96_tiprack_1000ul', location = '7')
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '11')
    p1000 = protocol.load_instrument('p1000_single', 'left', tip_racks=[tiprack_1])
    p300 = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack_2])
    
    tip_placement = {i + 1: char for i, char in enumerate(reversed("ABCDEFGH"))}
    well_placement = [char for i, char in enumerate("ABCDEFGH")]
    tubes_placement = {1:'A1',2:'A2',3:'A3', 4:'B1',5:'B2',6:'B3'}
    #tubes_placement = {i + 1: "AB"[i // 3] + str(i + 1 % 3) for i in range(6)}
    
    
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
        tubes = source_tubes[source_tube // 6]  # // integer division - the floor of row divided by 6
        tube = tubes[tubes_placement[tube_row]]
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
                    strepto_well[strepto[i]] += ", " + plate_well + str(col)
                
                else:
                    strepto_well[strepto[i]] = plate_well + str(col)

                well += 1
                used += 1
                if well == fill_well + 6:
                    break


                if well % 8 == 0:
                    #print("new line")
                    col += 1 

        p1000.return_tip()
        #p300.drop_tip()
    
    """Transfer from streptomyces plate to 96-well plate"""
       
    #Preparing necessary locations of the streptomyces based on where the E.coli is pipetted
    ""
    strepto_wells = dict()
    for ecoli in strepto_placement:

        for strepto in strepto_placement[ecoli]:

            if strepto in strepto_wells.keys():

                strepto_wells[strepto].append(strepto_placement[ecoli][strepto])

            else:
                well = strepto_placement[ecoli][strepto]
                
                #strepto_wells[strepto] = [strepto_placement[ecoli][strepto]]
                strepto_wells[strepto] = [w.strip() for w in well.split(",")]

    #150ul per well (up to 6 wells, plus 20ul) aspirated then 150ul is dispensed, more is collected (if necessary)
    strepto_amount = 1
    strepto_plate = 0
    dest_well = 1
    dest_plate = 0
    
    for strepto in strepto_wells:

        well12 = source_12plates[strepto_plate] #12-well source
        well96 = dest_plates[dest_plate]
     
        for i in range(len(strepto_wells[strepto])):

            p300.pick_up_tip()
            p300.aspirate(
                    155, # volume to collect
                    well12["A" + str(strepto_amount)]  # which well to aspirate from
            )

            p300.dispense(
                150,
                well96[strepto_wells[strepto][i]]
            )
            
            p300.return_tip()
            #p300.drop_tip()
            
            dest_well += 1


        strepto_amount += 1

        if strepto_amount > 12:
            strepto_amount = 1
            strepto_plate += 1
          
        if dest_well > 96:
            dest_well = 1
            dest_plate += 1

    
    
  
    