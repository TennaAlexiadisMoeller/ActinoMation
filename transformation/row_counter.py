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


def count_rows_numbers(s_num):
    
    c_num = int(np.floor(s_num / 8))    
    r_num = s_num - (c_num*8)
    
    return c_num, r_num
    
    
    