import ipywidgets as widgets
from ipywidgets import interact, Dropdown, Button
import numpy as np

volume_range = [150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,1000,2000,3000,4000,5000,10000,20000]

volume_w = None

def create_dropdown_calc():
    global volume_w
    
    volume_w = Dropdown(options = volume_range)

def print_dropdown_calc():    
    assert volume_w
    
    @interact(mL = volume_w)
    
    def _print_dropdown(mL):
        global l_num
        volume = mL
        liquid_unit = " mL"
        
        mg_weight = 0.02*volume
        
        if volume >= 1000:
            volume = mL/1000
            liquid_unit = " L"

        print("\nYou need the following to create the agar:\n- " + 
              str(mg_weight) + " g Mannitol\n- " + 
              str(mg_weight) + " g Soya Flour\n- " + 
              str(mg_weight) + " g Agar\n- " + 
              str(volume) + liquid_unit + " of tap water")

        
    #return l_num