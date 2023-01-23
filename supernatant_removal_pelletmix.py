#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 09:44:00 2022

@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Supernatant protocol',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for removing most of supernatant after centrifuging',
    'apiLevel': '2.4'
}

""" Variables"""

#The number of rows with liquid = number of tips
rows = 8

columns = 12 #with most it will be 12, but good to make it open for adjusting

tip_placement = {1:'H1',2:'G1',3:'F1',4:'E1',5:'D1',6:'C1',7:'B1',8:'A1'}

#num of runs
num = 1

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    """ load labware """
    source_plate_1 = protocol.load_labware('nest_96_wellplate_2ml_deep', location = '3') 
    dest_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', location = '9')
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', location = '11')


    """ load pipettes """
    p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1])

    """ liquid transfer commands """
    
    for col in range(columns):
        #150ul from source plate with multi following the 8 columns - mixing before moving on 3 times with 150ul
        
        #Transferring 150ul from source plate 1 to destination plate
        p300.pick_up_tip(tiprack_1[tip_placement[rows]]) 
        
        #aspirating at approx. 1/4 of regular speed for less movement in the pellet
        p300.flow_rate.aspirate = 25
        
        #The deepwell plate has a depth of 38mm, trying with going to the middle of the well
        p300.aspirate(200,source_plate_1['A'+str(1+col)].top(-19))
        
        #Disposing of the supernatant in trough instead of waste to reuse tips
        p300.dispense(200,dest_plate['A'+str(1+col)])
        
        #Mixing the pellet with left supernatant
        p300.mix(2,160,source_plate_1['A'+str(1+col)])

        #p300.return_tip()
        p300.drop_tip()
        