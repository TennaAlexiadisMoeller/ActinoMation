import ipywidgets as widgets
import numpy as np
from ipywidgets import  Layout, Textarea, Label, Dropdown, VBox, Box, Text

def save_transformation():
    
    lbl = widgets.HTML(value="<h1 style='font-size:18px'> Paste the names of the plasmid(s) and competent cell used. Remember to state  any well duplicates with a number, or similar indicator, at end of name.<br><br>Copy columns directly from Excel, or similar software, or write them manually. Tab-separation only.<br><br></h1>")
    
    plasmid_names = widgets.Textarea(description = 'Plasmid(s):', 
                                     disabled = False, 
                                     display = 'flex'
                                    )
    
    competent_cell = widgets.Text(value='',
                                   description='Competent cell:',
                                   disabled=False,
                                   style = {'description_width': 'initial'}
                                  )
    
    names = VBox([lbl, Box([plasmid_names, competent_cell])])
    
    display(names)
    
    return plasmid_names, competent_cell


def create_dropdown_transf():

    lbl = widgets.HTML(value="<h1 style='font-size:18px'>How many samples do you have to transform? This number can be higher than the amount of plasmids as the user will have to take into account the number of replicas<br><br></h1>")
    
    s_num = widgets.Dropdown(options=list(range(1,97)),value=1,description='Samples:',disabled=False) 
    
    names = VBox([lbl, s_num])
    
    display(names)

    return s_num


def create_dropdown_conj():
    p_num = widgets.Dropdown(options=list(range(1,17)),value=1,description='Plasmids:',disabled=False) 
    s_num = widgets.Dropdown(options=list(range(1,25)),value=1,description='Strepto:',disabled=False) 
    
    return p_num, s_num


def count_rows_numbers(s_num):
    
    c_num = int(np.floor(s_num / 8))    
    r_num = s_num - (c_num*8)
    
    return c_num, r_num


def save_conjugation():

    lbl_plasmid = widgets.HTML(value="<h1 style='font-size:18px'> Paste your E. coli and Streptomyces lists here. If more than 1 tube has the same E. coli, or the same Streptomyces, remember to state this with a number at end of name or similar indicator.<br>Copy columns directly from Excel, or similar software, or write them manually. Tab-separation only.<br><br></h1>")
    
    ecoli_names = widgets.Textarea(description='E.coli(s):',
                                   disabled=False,
                                   display='flex'
                                  ) 
    
    streptomyces_names = widgets.Textarea(description='Streptomyce(s):',
                                          disabled=False,
                                          display='flex' ,
                                          style = {'description_width': 'initial'}
                                         ) 
    
    names = VBox([lbl_plasmid, Box([ecoli_names, streptomyces_names])])
    
    display(names)
    
    return ecoli_names, streptomyces_names


def antibiotics():
    
    lbl = widgets.HTML(value="<h1 style='font-size:18px'> Paste the names of the antibiotics necessary for both the competent cell and the plasmid(s).<br>Copy columns directly from Excel, or similar software, or write them manually. Tab-separation only.<br><br></h1>")
    
    plasmid_antibiotics = widgets.Textarea(description = 'Plasmid(s)\n antibiotic(s):', 
                                     disabled = False, 
                                     display = 'flex',
                                     style = {'description_width': 'initial'},
                                     layout=Layout(width="380px")
                                    )
    
    competent_antibiotics = widgets.Textarea(description = 'Competent cell antibiotic(s):', 
                                     disabled = False, 
                                     display = 'flex',
                                     style = {'description_width': 'initial'},
                                     layout=Layout(width="400px")
                                    )
    
    names = VBox([lbl, Box([plasmid_antibiotics, competent_antibiotics])])
    
    display(names)
    
    return plasmid_antibiotics, competent_antibiotics

def conjugation_volumes(conjugation_mix):
    
    volume_strepto = {}
    volume_ecoli = {}
    for ecoli in conjugation_mix:

        num_of_wells = len(conjugation_mix[ecoli])

        volume_ecoli[ecoli] = [num_of_wells]
        volume_ecoli[ecoli].append((num_of_wells * 150) + ((num_of_wells * 150)*0.1))

        for value in conjugation_mix[ecoli]:
            if value in volume_strepto:
                volume_strepto[value] += 1

            else:
                volume_strepto[value] = 1

    for value in volume_strepto:
        volume = volume_strepto[value] * 150

        volume_strepto[value] = [volume_strepto[value]]

        volume_strepto[value].append(volume + (volume * 0.1))
    
   
    return volume_strepto, volume_ecoli
    
    
    