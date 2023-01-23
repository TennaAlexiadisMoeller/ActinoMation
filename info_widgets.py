import ipywidgets as widgets
import numpy as np
from ipywidgets import  Layout, Textarea, Label, Dropdown, VBox, Box

def save_transformation():
    plasmid_names = widgets.Textarea(description = 'Plasmid(s):', 
                                     disabled = False, 
                                     display = 'flex'
                                    )
    
    competent_cells = widgets.Textarea(description = 'Competent cell(s):',
                                       disabled = False,
                                       display = 'flex',
                                       style = {'description_width': 'initial'}
                                      ) 
    
    names = Box([plasmid_names,competent_cells])
    
    display(names)
    
    return plasmid_names, competent_cells


def create_dropdown_transf():
    s_num = widgets.Dropdown(options=list(range(1,97)),value=1,description='Samples:',disabled=False) 
    
    display(s_num)

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

    lbl_plasmid = widgets.HTML(value="<h1 style='font-size:18px'> Paste your E. coli and Streptomyces lists here. If more than 1 tube has the same E. coli, or the same Streptomyces, remember to state this with a number at end of name or similar indicator.<br><br>Copy columns directly from Excel or similar software. Tab-separation only.<br><br></h1>")
    
    ecoli_names = widgets.Textarea(description='E.coli(s):',
                                   disabled=False,
                                   display='flex'
                                  ) 
    
    streptomyces_names = widgets.Textarea(description='Streptomyce(s):',
                                          disabled=False,
                                          display='flex' ,
                                          style = {'description_width': 'initial'}
                                         ) 
    
    names = VBox([lbl_plasmid,Box([ecoli_names,streptomyces_names])])
    
    display(names)
    
    return ecoli_names, streptomyces_names