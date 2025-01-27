#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:56:20 2022

@author: tgrra
"""

import pandas as pd
import numpy as np
from datetime import datetime

def conjugation_consumables_position(conjugation_mix, ecoli_tubes):

    #For 1 run:
    consumables = {"96 deepwell plate": [3],
                    "300p tipbox": [11],
                    "1000p tipbox": [7],
                    "50ml Falcon tube rack for E. coli": [6],
                    "15ml Falcon tube rack for Streptomyces": [9]}
    
    consumables_list = {"96 deepwell plate(s)": 1,
                    "300p tipbox(es)": 1,
                    "1000p tipbox(es)": 1,
                    "50ml Falcon tube rack(s) for E. coli": 1,
                    "15ml Falcon tube rack(s) for Streptomyces": 1}
    
    conjugations_size = 0
    streptomyces_number = len(sorted(set([i[0] for i in conjugation_mix.values()])))

    for item in conjugation_mix:
        for i in range(len(conjugation_mix[item])):
            conjugations_size += 1

    if conjugations_size > 96:        
        consumables["96 deepwell plate 1"] = consumables["96 deepwell plate"]
        del consumables["96 deepwell plate"]
        consumables["96 deepwell plate 2"] = [2]
        consumables_list["96 deepwell plate"] = 2
        
        consumables["300p tipbox 1"] = consumables["300p tipbox"]
        del consumables["300p tipbox"]
        consumables["300p tipbox 2"] = [10]
        consumables_list["300p tipbox"] = 2
  

    if len(ecoli_tubes) > 6:
        consumables["50ml Falcon tube rack for E. coli 1"] = consumables["50ml Falcon tube rack for E. coli"]
        del consumables["50ml Falcon tube rack for E. coli"]
        consumables["50ml Falcon tube rack for E. coli 2"] = [5]        
        consumables_list["50ml Falcon tube rack for E. coli"] = 2

        
    if len(ecoli_tubes) > 12:
        consumables["50ml Falcon tube rack for E. coli 1"] = consumables["50ml Falcon tube rack for E. coli"]
        del consumebles["50ml Falcon tube rack for E. coli"]
        consumables["50ml Falcon tube rack for E. coli 2"] = [5]
        consumables["50ml Falcon tube rack for E. coli 3"] = [4]
        consumables_list["50ml Falcon tube rack for E. coli"] = 3
        
    if streptomyces_number > 16:
        consumables["15ml Falcon tube rack for Streptomyces 1"] = consumables["15ml Falcon tube rack for Streptomyces"]
        del consumables["15ml Falcon tube rack for Streptomyces"]
        consumables["15ml Falcon tube rack for Streptomyces 2"] = [8]        
        consumables_list["15ml Falcon tube rack for Streptomyces"] = 2

    return consumables, consumables_list




def conjugation_consumables_all(conjugation_mix, consumables_list, plasmid_antibiotics, competent_antibiotics, strep_volume, ecoli_volume):
    title_name = []
    title_type = []
    title_amount_volume = []

    #Consumables
    for key in consumables_list:
        if "rack" in key:
            title_name.append(key)
            title_type.append("Labware")

        if "tipbox" in key or "plate" in key:
            title_name.append(key)
            title_type.append("Consumables")

        title_amount_volume.append(str(consumables_list[key]))

    mix_size = 0
    for i in conjugation_mix:
        if isinstance(conjugation_mix[i], list):
            mix_size += len(conjugation_mix[i])

    title_name.append("MS agar plate(s) with MgCl2")
    title_type.append("Consumables")
    title_amount_volume.append(str(mix_size))

    title_name.append("ISP2 plates with " + ", ".join(plasmid_antibiotics) + " and Nalidixic acid")
    title_type.append("Consumables")
    title_amount_volume.append(str(mix_size))


    #Antibiotics
    for i in range(len(plasmid_antibiotics)):
        title_name.append(plasmid_antibiotics[i])
        title_type.append("Antibiotic (plasmid selection)")
        title_amount_volume.append("Experiment specific")

    for i in range(len(competent_antibiotics)):
        title_name.append(competent_antibiotics[i])
        title_type.append("Antibiotic (competent cell selection)")
        title_amount_volume.append("Experiment specific")

    #15 mL tubes (streptomyces)
    title_name.append("15 mL tube(s)")
    title_type.append("Consumables")
    title_amount_volume.append(str(len(strep_volume)))

    #50 mL tubes (streptomyces)
    title_name.append("50 mL tube(s)")
    title_type.append("Consumables")
    title_amount_volume.append(str(len(ecoli_volume))) 
    
    #Streptomyces    
    for key in strep_volume:
        title_name.append(key)
        title_type.append("Sample (Streptomyces)")
        title_amount_volume.append(str(strep_volume[key][1]) + " uL")
    
    #Ecoli    
    for key in ecoli_volume:
        title_name.append(key)
        title_type.append("Sample (E. coli)")
        title_amount_volume.append(str(ecoli_volume[key][1]) + " uL")
  
    
    #Notes
    title_notes = [""]*len(title_type)
    
    #Creating the dataframe
    titles = ["Name", "Type", "Amount/Volume", "Notes"]

    df = pd.DataFrame(list(zip(title_name, title_type, title_amount_volume, title_notes)), columns = titles)
    df = df.sort_values(by=['Type'])
    
    #Saving as Excel table
    dt_string = datetime.now().strftime("%Y%m%d")

    writer_conjugation = pd.ExcelWriter(dt_string + "_Conjugation_materials.xlsx", engine='xlsxwriter')

    df.to_excel(writer_conjugation, sheet_name="All materials", startrow=1, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer_conjugation.book
    worksheet = writer_conjugation.sheets["All materials"]

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

    writer_conjugation.save()
    #writer_conjugation.close()


    #Nice print in Jupyter
    df_toshow = df[(df['Type'] == "Sample (E. coli)") | (df['Type'] == "Sample (Streptomyces)")].iloc[:,:-1]
    df_toshow.index = np.arange(1, len(df_toshow)+1)
    display(df_toshow)
 