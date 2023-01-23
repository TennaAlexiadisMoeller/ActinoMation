#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 11:18:20 2023

@author: tgrra
"""

from ipywidgets import Button, HBox, VBox, Layout, Output, Textarea, Label, HTML
import matplotlib.pyplot as plt
import numpy as np


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
                           height = '673px',
                           align_items = 'center', 
                           width='100%')
            )

    display(deck)

    
    
def display_96well_plate_design(plate_fill_ins):

    lbl_top_title = HTML(value="<h1 style='font-size:24px'>Top of 96-well plate<br><br></h1>")
    lbl_bottom_title = HTML(value="<h1 style='font-size:24px'>Bottom of 96-well plate<br><br></h1>")

    lbl_layout = layout = Layout(display = "flex", 
                                    #justify_content = "center", 
                                    align_items = 'center',
                                    width = "77px",
                                    height = "83px",
                                 border = 'solid 1px'
                                )


    labels = list()
    for column in range(1,13):
        for row in "ABCDEFGH":
            labels.append("<b><p style='text-align:center; font-size:12px'>" + row + str(column) + "</p></b>")

    #Insert names of consumeables on proper positions    
    for item in plate_fill_ins:
        for i in range(len(plate_fill_ins[item])):

            labels[plate_fill_ins[item][i]] = "<b><p style='text-align:center; font-size:12px; color:red'>" + item +  "</p></b>"


    #Create the wells, cells and rows of the plate 
    cells = list()
    columns = list()

    for i in range(len(labels)):
        cells.append(HTML(value=labels[i], 
                          layout = lbl_layout
                         )
                    )

    for i in range(0,96,8):
        columns.append(VBox([cells[i], cells[i+1], cells[i+2], cells[i+3],
                          cells[i+4], cells[i+5], cells[i+6],
                          cells[i+7]],
                          layout=Layout(display='flex', 
                                        align_items = 'center', 
                                        width = '100%', 
                                        height = '100%')
                        )
                   )

    # Display the deck
    plate = VBox([lbl_top_title, HBox([columns[0], columns[1], columns[2], columns[3],
                                       columns[4], columns[5], columns[6], columns[7],
                                       columns[8], columns[9], columns[10], columns[11]]), lbl_bottom_title],
             layout=Layout(display='flex',
                           height = '848px',
                           align_items = 'center', 
                           width='100%')
            )

    display(plate)
    
    
    
def display_15ml_falcon_rack(tubes):
    
    #Original tube length
    tube_length = len(tubes)
    
    #Falcontube counter
    tube = 1
    
    #Rack counter
    racknum = 1
    
    if len(tubes) > 15:
        #print(tube_length, tubes)
        racknum = 2
    
        for i in range(30-tube_length):
            tubes.append("Falcon \ntube " + str(tube_length+i+1))
    
    else:
        for i in range(15-tube_length):
            tubes.append("Falcon \ntube " + str(tube_length+i+1))

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

    #plt.show()
    plt.savefig("15ml_falcon_rack_output.png")

    
def display_50ml_falcon_rack(tubes):
    
    #Original tube length
    tube_length = len(tubes)
    
    #Falcontube counter
    tube = 1
    
    #Rack counter
    racknum = 1
    
    if len(tubes) > 6:
        #print(tube_length, tubes)
        racknum = 2
    
        for i in range(12-tube_length):
            tubes.append("Falcon \ntube " + str(tube_length+i+1))
    
    else:
        for i in range(6-tube_length):
            tubes.append("Falcon \ntube " + str(tube_length+i+1))

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

    #plt.show()
    plt.savefig("50ml_falcon_rack_output.png")