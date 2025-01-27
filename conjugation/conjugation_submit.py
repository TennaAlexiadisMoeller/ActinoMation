#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:56:20 2022

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

import os
from ipywidgets import Button, HBox, VBox, Layout, Label, Dropdown, Select, SelectMultiple, HTML
import pandas as pd

################################ Dropdown menus ################################
  
def display_form(ecoli,streptomyces):
    
    #list of all E. coli and streptomyces mixes
    mix_list = [""]
    
    #final dictionary of information for Opentrons protocol
    conjugation_mix = {}
    
    #final list of E. coli used for Opentrons protocol
    ecoli_tubes = []
    
    #labels
    lbl_save_top = Label(value = '', layout = Layout(justify_content="center"))
    lbl_save_bottom = Label(value ='', layout = lbl_save_top.layout)
    lbl_choice = Label(value = '', layout = Layout(height='40px'))
    lbl_delete = Label(value = '', layout = Layout(height='40px'))
    lbl_horizontal_spacer = Label(value = '', layout = Layout(height='30px')) 
    lbl_title = HTML(value="<h1 style='font-size:18px'>Choose what streptomyce(s) you want to test with which E. coli. When done, check all combinations are registered and delete any unwanted ones. Each use of an E.coli is 160ul and creating combinations of more than the tube (5-6mL) carries will lead to error on the Opentrons.<br><br></h1>")
    lbl_ecoli = Label(value = "Choose your E. coli:")
    lbl_strepto = Label(value = "Choose all streptomyces you want to test with chosen E. coli:")
    lbl_submit = Label(value = "4. Press submit to create mix plate design", layout = Layout(height='30px'))
    lbl_mix = Label(value = "E.coli and streptomyces mixes that will be pipetted:")
    
    
    #Takes the single E. coli choice and the N number of streptomyces and creates the visual list for the user that will then be used to create the dictionary for the opentron protocol
    def on_button_clicked_submit(choice):  
        
        if ecoli_dropdown.value == "" or strepto_dropdown.value == "":
            lbl_choice.value = "At least 1 E. coli and 1 Streptomyces must be added."
        
        else:
            lbl_choice.value = ""
            
            #Creating the mix information in the widget as well as in dict and list for Opentrons
            for i in range(len(strepto_dropdown.value)):
                mix_list.append(ecoli_dropdown.value + ": " + strepto_dropdown.value[i])
                
                if not ecoli_dropdown.value in ecoli_tubes:
                    ecoli_tubes.append(ecoli_dropdown.value)
                
                if not ecoli_dropdown.value in conjugation_mix:
                    conjugation_mix[ecoli_dropdown.value] = [strepto_dropdown.value[i]]
                
                else:
                    conjugation_mix[ecoli_dropdown.value].append(strepto_dropdown.value[i])
            
            if mix_list[0] == "":
                mix_list.pop(0)

            mix_dropdown.options = mix_list
            
    
    #Deletes the mixes chosen from the mix_dropdown menu and from the ecoli_tubes list and the conjugation_mix dict
    def on_button_clicked_delete(delete):
        
        if ecoli_dropdown.value == "" or strepto_dropdown.value == "":
            lbl_delete.value = "No mixes added for the conjugation to be removed."
        
        else:
            lbl_delete.value = ""
        
            for i in range(len(mix_dropdown.value)):

                mix_list.remove(mix_dropdown.value[i])
                mix_to_remove =  mix_dropdown.value[i].split(": ")

                if mix_to_remove[1] in conjugation_mix[mix_to_remove[0]]:

                    conjugation_mix[mix_to_remove[0]].remove(mix_to_remove[1])

                if len(conjugation_mix[mix_to_remove[0]]) == 0:

                    del conjugation_mix[mix_to_remove[0]]

                    ecoli_tubes.remove(mix_to_remove[0])
                
                
                #del conjugation_mix[mix_dropdown.value[i].replace(": ","::\n")]
            

            mix_dropdown.options = mix_list

            
    
    ecoli_dropdown = Select(options = ecoli, 
                            value = ecoli[0] , 
                            disabled = False,
                            layout = Layout(width = '350px',
                                            height = '150px',
                                    )
                           )
    strepto_dropdown = SelectMultiple(options = streptomyces, 
                                      value = [streptomyces[0]], 
                                      disabled = False,
                                      layout = ecoli_dropdown.layout
                                     )
    
    mix_dropdown = SelectMultiple(options = mix_list, 
                                  value = [mix_list[0]], 
                                  disabled = False,
                                  layout = ecoli_dropdown.layout
                                 )
    
    #Button for submitting mixes of streptomyces + E. coli
    submit_button = Button(description='Submit',
                                   button_style='success',
                                   layout = Layout(width = '300px',
                                                   height = '50px'
                                                  )
                                  )
    
    #Button for deleting mixes
    delete_button = Button(description='Delete',
                               button_style='danger',
                               layout = submit_button.layout
                          )
    
    #Creating the function of the buttons
    submit_button.on_click(on_button_clicked_submit)
    delete_button.on_click(on_button_clicked_delete)       
    

    
    ecoli_box = VBox([lbl_ecoli, ecoli_dropdown],
                     layout=Layout(display='flex',
                                    width='50%',
                                  )
                    )
    
    streptomyces_box = VBox([lbl_strepto, 
                             strepto_dropdown,
                             lbl_horizontal_spacer,
                             submit_button,
                             lbl_choice],
                            layout = ecoli_box.layout,
                           )
    
    #The box showing the combiation of streptomyces + E. coli as a dropdown menu
    mix_box = VBox([lbl_mix, mix_dropdown],
             layout = ecoli_box.layout,
            )
    
    #The box with delete and save button as well as diagram of plate
    buttons_box = VBox([delete_button, lbl_delete],
             layout = ecoli_box.layout,
            )    
    
    #Top half of widget box with E. coli selection box and mix box
    top_box = HBox([ecoli_box, mix_box],
                     layout=Layout(display='flex',
                                  )
                    )
    
    #Bottom half of widget box with streptomyces selection box and illustrated plate design(?)
    bottom_box = HBox([streptomyces_box, buttons_box],
                     layout=top_box.layout,
                    )
    
    
    #Final combination of widgets that is illustrated
    scene = VBox([lbl_title, top_box, lbl_horizontal_spacer, bottom_box],
                latout = Layout(width = '100%',
                               )
                )

    display(scene)
    
    
    return conjugation_mix, ecoli_tubes
