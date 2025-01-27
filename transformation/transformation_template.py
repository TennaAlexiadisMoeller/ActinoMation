#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:43:03 2022
Originally created as part of a PhD project started in 2022
@author: tgrra
"""

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Transformation protocol with heatshock',
    'author': 'tgrra@biosustain.dtu.dk',
    'description': 'Protocol for combination of two 96-well plates, followed by heat shock and then addition to media',
    'apiLevel': '2.4'
    
}

columns = 12

#The number of rows in last column that isn't full
rows = 0


# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):
    
    """ load labware """
    
    #Run 1
    ecoli_plate_1 = protocol.load_labware('opentrons_96_aluminumblock_nest_wellplate_100ul', '8')

    temp_mod_cold_1 = protocol.load_module('temperature module gen2', '7')
    ligation_plate_1 = temp_mod_cold_1.load_labware('opentrons_96_aluminumblock_nest_wellplate_100ul') 
    
    temp_mod_heat_1 = protocol.load_module('temperature module gen2', '9')
    shock_plate_1 = temp_mod_heat_1.load_labware('opentrons_96_aluminumblock_nest_wellplate_100ul')
    
    media_plate_1 = protocol.load_labware('usascientific_96_wellplate_2.4ml_deep',  '6')
    
    
    """ load pipettes """
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul',  '11')
    p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack_1])
    
    
    #Setting the temperature of the modules
    temp_mod_cold_1.set_temperature(4)
    temp_mod_heat_1.set_temperature(42)

    protocol.pause("The temperatuer modules have now reached the necessary temp. Please place all necessary plates and tips before pressing 'resume'")
    
    tip_placement = {1:'H',2:'G',3:'F',4:'E',5:'D',6:'C',7:'B',8:'A'}

    #Ensuring as few bubbles as possible for the air gap by reducing speed (half speed of standard)
    p300.flow_rate.dispense = 75
    p300.flow_rate.aspirate = 75
    p300.flow_rate.blow_out = 75

    
    """ liquid transfer commands """
    
    
    for col in range(columns):
        
        #Transferring 50ul from E.coli plate 1 to destination ligation plate and returning tips for re-use
        p300.pick_up_tip(tiprack_1['A'+str(1+col)]) 
        p300.aspirate(50,ecoli_plate_1['A'+str(1+col)])
        p300.dispense(50,ligation_plate_1['A'+str(1+col)])
        p300.mix(3,40,ligation_plate_1['A'+str(1+col)])
        p300.return_tip()

    
    if rows != 0:
        
        #Transferring 50ul from E.coli plate 1 to destination ligation plate and returning tips for re-use
        p300.pick_up_tip(tiprack_1[tip_placement[rows]+str(columns+1)]) 
        p300.aspirate(50,ecoli_plate_1['A'+str(columns+1)])
        p300.dispense(50,ligation_plate_1['A'+str(columns+1)])
        p300.mix(3,40,ligation_plate_1['A'+str(columns+1)])
        p300.return_tip()
    
    #Letting the mix sit on ice for 30 minutes
    protocol.delay(minutes=30)
    
    #Resetting the tips to still be at box 1
    p300.starting_tip = tiprack_1.well('A1')

    for col in range(columns):

        #Transferring 52ul mix from ligation plate to the heating plate for a heat shock quickly followed by a transfer to the LB


        #Creating a setup of LB media -> air gap -> E. coli
        p300.pick_up_tip(tiprack_1['A'+str(1+col)]) 
        p300.aspirate(100,media_plate_1['A'+str(1+col)])
        p300.aspirate(30,media_plate_1['A'+str(1+col)].top())       
        p300.aspirate(45,ligation_plate_1['A'+str(1+col)].bottom(1))
        p300.dispense(45,shock_plate_1['A'+str(1+col)])

        protocol.delay(seconds = 30)

        p300.dispense(110,shock_plate_1['A'+str(1+col)])   
        p300.mix(1,110,shock_plate_1['A'+str(1+col)])      

        p300.aspirate(130,shock_plate_1['A'+str(1+col)].bottom(1))
        p300.dispense(130,media_plate_1['A'+str(1+col)])  
        p300.mix(3,200,media_plate_1['A'+str(1+col)])

        p300.drop_tip()    
        
    if rows != 0:
        
        #Resetting the tips to still be at box 1
        p300.starting_tip = tiprack_1.well(tip_placement[rows]+str(columns+1))
        
        #Transferring 52ul mix from ligation plate to the heating plate for a heat shock quickly followed by a transfer to the LB

        #Creating a setup of LB media -> air gap -> E. coli
        p300.pick_up_tip(tiprack_1[tip_placement[rows]+str(columns+1)]) 
        p300.aspirate(100,media_plate_1['A'+str(columns+1)])
        p300.aspirate(30,media_plate_1['A'+str(columns+1)].top())       
        p300.aspirate(45,ligation_plate_1['A'+str(columns+1)].bottom(1))
        p300.dispense(45,shock_plate_1['A'+str(columns+1)])
        
        protocol.delay(seconds = 30)
        
        p300.dispense(110,shock_plate_1['A'+str(columns+1)])   
        p300.mix(1,110,shock_plate_1['A'+str(columns+1)])      

        p300.aspirate(130,shock_plate_1['A'+str(columns+1)].bottom(1))
        p300.dispense(130,media_plate_1['A'+str(columns+1)])  
        p300.mix(3,200,media_plate_1['A'+str(columns+1)])
        
        p300.drop_tip()
        

        
        
        
        
        
        
        
        