#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:56:20 2022

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def transformation_consumables_position():

    #For 1 run:
    consumables_labware = {"96 deepwell plate": [6],
                    "300p tipbox": [11],
                    "Heating module w. aluminum block": [9],
                    "Cooling module w. aluminum block": [7],
                    "Pre-cooled aluminum block": [8]}
    
    consumables_material = {"LB media": [6],
                    "300p tipbox": [11],
                    "96-well PCR plate: empty": [9],
                    "96-well PCR plate: plasmid(s)": [7],
                    "96-well PCR plate: competent cell(s)": [8]}
    
    return consumables_labware, consumables_material   
    

    
    
def transformation_consumables_all(plasmid_names, competent_cell, plasmid_antibiotics, competent_antibiotics):
    transf_num = len(plasmid_names)

    labware = {"Heating/cooling module": "2", "Aluminum block": "3"}
    consume = {"300p tipbox": "1", "96-well fully skirted 200ul PCR plate": "3", "96-well deep-well 2ml plate": "1"}


    title_name = []
    title_type = []
    title_amount_volume = []

    #labware
    for item in labware:
        title_name.append(item)
        title_type.append("Labware")
        title_amount_volume.append(labware[item])

    #consumables
    for item in consume:
        title_name.append(item)
        title_type.append("Consumables")
        title_amount_volume.append(consume[item])

    title_name.append("LB media (liquid)")
    title_type.append("Consumables")
    title_amount_volume.append(str((transf_num*950)/1000) + " mL")

    title_name.append("LB plates with " + ", ".join(plasmid_antibiotics) + ", " + ", ".join(competent_antibiotics))
    title_type.append("Consumables")
    title_amount_volume.append(str(transf_num))

    #Antibiotics
    for i in range(len(plasmid_antibiotics)):
        title_name.append(plasmid_antibiotics[i])
        title_type.append("Antibiotic (plasmid selection)")
        title_amount_volume.append("Experiment specific")

    for i in range(len(competent_antibiotics)):
        title_name.append(competent_antibiotics[i])
        title_type.append("Antibiotic (competent cell selection)")
        title_amount_volume.append("Experiment specific")


    #Plasmid cells
    for plasmid in plasmid_names:
        title_name.append(plasmid)
        title_type.append("Sample (E. coli with plasmid)")
        title_amount_volume.append("2 uL")

    #Competent cell
    title_name.append(competent_cell[0])
    title_type.append("Sample (E. coli with competent cell)")
    title_amount_volume.append(str(transf_num*50) + " uL")

    #Notes
    title_notes = [""]*len(title_type)

    #Creating the dataframe
    titles = ["Name", "Type", "Amount/Volume", "Notes"]

    df = pd.DataFrame(list(zip(title_name, title_type, title_amount_volume, title_notes)), columns = titles)
    df = df.sort_values(by=['Type'])
    
    
    #Saving as Excel table
    dt_string = datetime.now().strftime("%Y%m%d")

    writer_transformation = pd.ExcelWriter(dt_string + "_Transformation_materials.xlsx", engine='xlsxwriter')

    df.to_excel(writer_transformation, sheet_name="All materials", startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer_transformation.book
    worksheet = writer_transformation.sheets["All materials"]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = []
    for header in df.columns:
        column_settings.append({'header': header})

    # Add the table.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 30)

    writer_transformation.save()
    #writer_transformation.close()

    #Nice print in Jupyter
    df_toshow = df[(df['Type'] == "Sample (E. coli with plasmid)") | (df['Type'] == "Sample (E. coli with competent cell)")].iloc[:,:-1]
    df_toshow.index = np.arange(1, len(df_toshow)+1)
    display(df_toshow)
    

