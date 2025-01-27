#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 11:18:20 2023

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

from ipywidgets import Button, HBox, VBox, Layout, Output, Textarea, Label, HTML
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def display_deck_design(deck_fill_ins):
    lbl_top_title = HTML(value="<h1 style='font-size:18px'>Back of robot<br><br></h1>")
    lbl_bottom_title = HTML(value="<h1 style='font-size:18px'>Front of robot<br><br></h1>")

    lbl_layout = layout = Layout(display = "flex", 
                                    #justify_content = "center", 
                                    align_items = 'center',
                                    width = "150px",
                                    height = "40px",
                                )

    lbl_fill = Label(" ", layout = lbl_layout)

    labels = ["<b><p style='text-align:center; font-size:16px'>" + str(x) for x in range(1,12)]+["<b><p style='text-align:center; font-size:18px'>Waste"]
    for i in range(len(labels)):
        labels[i] += "</p></b>"

    #Insert names of consumeables on proper positions    
    for item in deck_fill_ins:
        for i in range(len(deck_fill_ins[item])):

            labels[deck_fill_ins[item][i]-1] = "<b><p style='text-align:center; font-size:18px; color:red'>" + item +  "</p></b>"
        

    #Create the wells, cells and rows of the deck 
    wells = list()
    cells = list()
    rows = list()

    for i in range(len(labels)):
        wells.append(HTML(value=labels[i], 
                          layout = lbl_layout
                         )
                    )

        cells.append(VBox([lbl_fill,wells[i],lbl_fill], 
                          layout = Layout(#display = 'flex',
                                          border = 'solid 1px')
                         )
                    ) 


    for i in range(0,12,3):

        rows.append(HBox([cells[i], cells[i+1], cells[i+2]],
                         layout=Layout(display='flex', 
                                       align_items = 'center', 
                                       width = '49%', 
                                       height = '40%')
                        )
                   )

    # Display the deck
    deck = VBox([lbl_top_title, rows[3], rows[2], rows[1], rows[0], lbl_bottom_title],
             layout=Layout(display='flex',
                           height = '675px',
                           align_items = 'center', 
                           width='100%')
            )

    display(deck)

    
    
def display_96well_plate_design(deck_fill_ins, assay):
    
    wells = [" " for x in range(1,97)]
    #wells = ["Well\n" + str(x) for x in range(1,97)]
    
    #Insert names of consumeables on proper positions    
    for item in deck_fill_ins:
        if item != "":
            wells[deck_fill_ins[item]] = item
    
    #Creating the plot
    fig, ax = plt.subplots(8, 12, figsize=(15,15), 
                           subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

    #Title of first rack
    fig.suptitle('96-well plate design', fontsize=24)
    
    
    # Loop through each subplot and add a circle
    for i in range(12):
        for j in range(8):
            # Add a circle to the current subplot
            circle = plt.Circle((0.5, 0.5), 0.49, edgecolor="black", linewidth=1, facecolor ="white")
            ax[j, i].add_artist(circle)

            # Add text to the center of the circle
            ax[j, i].text(0.5, 0.5, wells[i*8+j], ha='center', va='center', fontsize=15)

            # Remove axis labels and tick marks
            ax[j, i].set_xticks([])
            ax[j, i].set_yticks([])


    # Add rectangle around first rack
    rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
    fig.add_artist(rect)
    
    if len(deck_fill_ins) > 96:
        
        #Creating the plot
        fig2, ax2 = plt.subplots(8, 12, figsize=(15,15), 
                               subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

        #Title of first rack
        fig2.suptitle('2nd 96-well plate design', fontsize=24)


        # Loop through each subplot and add a circle
        for i in range(12):
            for j in range(8):
                # Add a circle to the current subplot
                circle = plt.Circle((0.5, 0.5), 0.49, edgecolor="black", linewidth=1, facecolor ="white")
                ax2[j, i].add_artist(circle)

                # Add text to the center of the circle
                ax2[j, i].text(0.5, 0.5, wells[i*8+j], ha='center', va='center', fontsize=15)

                # Remove axis labels and tick marks
                ax2[j, i].set_xticks([])
                ax2[j, i].set_yticks([])


        # Add rectangle around first rack
        rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
        fig2.add_artist(rect)
    
    #Turning it into a dataframe for saving as .csv file
    mix_list = list()
    fill_lists = list()
    df = pd.DataFrame()

    for mix in deck_fill_ins:
        mix_list.append(mix)
        if len(mix_list) == 8:
            fill_lists.append(mix_list)
            mix_list = list()

    for i in range(12-len(fill_lists)):
        if len(mix_list) != 8:
            mix_list += (8-len(mix_list))*[""]
            fill_lists.append(mix_list)
        else:
            fill_lists.append(8*[""])

    for i in range(len(fill_lists)):
        df[i] = fill_lists[i]

    df = df.set_index(pd.Series(["A","B","C","D","E","F","G","H"]))
    df.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    
    #Saving the plot and the .csv file
    dt_string = datetime.now().strftime("%Y%m%d")
    
    df.to_csv(dt_string + "_" + assay + "_96well_plate_design.csv")
    plt.savefig(dt_string + "_" + assay + "_96well_plate_design.png", facecolor = "w")
    
    
    
def display_15ml_falcon_rack(tubes, assay):
    
    #Original tubes and tube length
    tubes = list(tubes)
    tube_length = len(tubes)
    
    #Falcontube counter
    tube = 1
    
    #Rack counter
    racknum = 1

    #Checking if more than one rack
    if len(tubes) > 15:
        racknum = 2
    
        for i in range(30-tube_length):
            tubes.append(" ")
            #tubes.append("Falcon \ntube " + str(tube_length+i+1))
    
    else:
        for i in range(15-tube_length):
            tubes.append(" ")
            #tubes.append("Falcon \ntube " + str(tube_length+i+1))

    # Create an empty figure
    fig, ax = plt.subplots(3, 5, figsize=(15, 9), 
                           subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

    #Title of first rack
    fig.suptitle('Rack 1 of 15mL Falcon tubes', fontsize=24)

    # Loop through each subplot and add a circle
    for i in range(3):
        for j in range(5):
            # Add a circle to the current subplot
            circle = plt.Circle((0.5, 0.5), 0.45, edgecolor="black", linewidth=1, facecolor ="white")
            ax[i, j].add_artist(circle)

            # Add text to the center of the circle
            ax[i, j].text(0.5, 0.5, tubes[i*5+j], ha='center', va='center', fontsize=20)

            tube += 1

            # Remove axis labels and tick marks
            ax[i, j].set_xticks([])
            ax[i, j].set_yticks([])

    # Add rectangle around first rack
    rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
    fig.add_artist(rect)        

    ###The second rack###
    if racknum == 2:
        fig2, ax2 = plt.subplots(3, 5, figsize=(15, 9), 
                               subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

        #Title of second rack
        fig2.suptitle('Rack 2 of 15mL Falcon tubes', fontsize=24)

        # Loop through each subplot and add a circle
        for i in range(3):
            for j in range(5):
                # Add a circle to the current subplot
                circle = plt.Circle((0.5, 0.5), 0.45, edgecolor="black", linewidth=1, facecolor ="white")
                ax2[i, j].add_artist(circle)

                # Add text to the center of the circle
                ax2[i, j].text(0.5, 0.5, tubes[(i*5+j)+15], ha='center', va='center', fontsize=20 )

                tube += 1

                # Remove axis labels and tick marks
                ax2[i, j].set_xticks([])
                ax2[i, j].set_yticks([])

        # Add rectangle around second rack
        rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
        fig2.add_artist(rect)

    dt_string = datetime.now().strftime("%Y%m%d")
    plt.savefig(dt_string + "_" + assay + "_15ml_falcon_rack_setup.png", facecolor = "w")

    
def display_50ml_falcon_rack(tubes, assay):
    
    #Original tubes and tube length
    tubes = list(tubes)
    tube_length = len(tubes)
    
    #Falcontube counter
    tube = 1
    
    #Rack counter
    racknum = 1
    
    #Checking if more than one rack
    if len(tubes) > 6:
        racknum = 2
    
        for i in range(12-tube_length):
            tubes.append(" ")
            #tubes.append("Falcon \ntube " + str(tube_length+i+1))
    
    else:
        for i in range(6-tube_length):
            tubes.append(" ")
            #tubes.append("Falcon \ntube " + str(tube_length+i+1))

    # Create an empty figure
    fig, ax = plt.subplots(2, 3, figsize=(15, 9), 
                           subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

    #Title of first rack
    fig.suptitle('Rack 1 of 50mL Falcon tubes', fontsize=24)

    # Loop through each subplot and add a circle
    for i in range(2):
        for j in range(3):
            # Add a circle to the current subplot
            circle = plt.Circle((0.5, 0.5), 0.45, edgecolor="black", linewidth=1, facecolor ="white")
            ax[i, j].add_artist(circle)

            # Add text to the center of the circle
            ax[i, j].text(0.5, 0.5, tubes[i*3+j], ha='center', va='center', fontsize=20)

            tube += 1

            # Remove axis labels and tick marks
            ax[i, j].set_xticks([])
            ax[i, j].set_yticks([])

    # Add rectangle around first rack
    rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
    fig.add_artist(rect)        

    ###The second rack###
    if racknum == 2:
        fig2, ax2 = plt.subplots(2, 3, figsize=(15, 9), 
                               subplot_kw={'xticks':[], 'yticks':[],'frame_on':False})

        #Title of second rack
        fig2.suptitle('Rack 2 of 50mL Falcon tubes', fontsize=24)

        # Loop through each subplot and add a circle
        for i in range(2):
            for j in range(3):
                # Add a circle to the current subplot
                circle = plt.Circle((0.5, 0.5), 0.45, edgecolor="black", linewidth=1, facecolor ="white")
                ax2[i, j].add_artist(circle)

                # Add text to the center of the circle
                ax2[i, j].text(0.5, 0.5, tubes[(i*3+j)+6], ha='center', va='center', fontsize=20 )

                tube += 1

                # Remove axis labels and tick marks
                ax2[i, j].set_xticks([])
                ax2[i, j].set_yticks([])

        # Add rectangle around second rack
        rect = plt.Rectangle((0, 0), 1, 1, lw=1, edgecolor='black', facecolor='none')
        fig2.add_artist(rect)

    dt_string = datetime.now().strftime("%Y%m%d")
    plt.savefig(dt_string + "_" + assay + "_50ml_falcon_rack_setup.png", facecolor = "w")
