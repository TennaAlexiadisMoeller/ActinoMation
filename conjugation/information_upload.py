#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 14:12:21 2023

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

import pandas as pd
import io
import ipywidgets as widgets
from ipywidgets import Button, FileUpload, HBox, Output, Box, Layout, HTML
from IPython.display import display

def conjugation_upload():

    ecoli = None
    streptomyces = None
    plasmid_antibiotics_list = None
    competent_antibiotics_list = None
    
    
    # label for the user
    lbl = HTML(value="<h1 style='font-size:18px'> Please choose your tab-separated .txt file. Remember all important information necessary for the run.<br><br>See the example for further information.<br><br></h1>")

    # Create an output widget for the upload message
    upload_message = Output(layout=Layout(max_height='50px', overflow='auto'))

    # Function to handle the file upload
    def handle_upload(change):
        nonlocal ecoli
        nonlocal streptomyces
        nonlocal plasmid_antibiotics_list
        nonlocal competent_antibiotics_list

        uploaded_filename = next(iter(change['new'].keys()))
        uploaded_file = change['new'][uploaded_filename]['content']
        
        # Print upload message above the widgets
        with upload_message:
            print("File uploaded. Antibiotic(s), ecoli(s) and streptomyces(s) has been registered.") 

        # Use pandas to read the uploaded file into a DataFrame
        uploaded_df = pd.read_csv(io.BytesIO(uploaded_file), sep='\t', header=None, index_col=0)
        
        #Extracting the necessary lines
        ecoli = uploaded_df.loc["ECOLI"].dropna().tolist()
        streptomyces = uploaded_df.loc["STREPTOMYCES"].dropna().tolist()
        plasmid_antibiotics_list = uploaded_df.loc["ANTIBIOTICS_PLASMID"].dropna().tolist()
        competent_antibiotics_list = uploaded_df.loc["ANTIBIOTICS_COMPETENT"].dropna().tolist()


    # Create a file upload widget allowing only single file
    file_upload = FileUpload(accept='.txt', multiple=False)

    # Attach the handle_upload function to the 'value' attribute of the file_upload widget
    file_upload.observe(handle_upload, names='value')

    # Function to show or hide example
    def toggle_example(change):
        if show_example_button.description == 'Show Example':
            show_example_button.description = 'Hide Example'
            example_output.clear_output(wait=True)
            with example_output:
                print_example()
            example_box.layout.visibility = 'visible'
            example_box.layout.max_height = 'none'  # Set max_height to 'none'
            example_box.layout.overflow = 'visible'  # Set overflow to 'visible'
            example_box.layout.display = ''  # Set display to default
            # Update the maximum height of the upload_message output
            upload_message.layout.max_height = '50px' if example_box.layout.visibility == 'hidden' else 'none'
        else:
            show_example_button.description = 'Show Example'
            example_output.clear_output(wait=True)
            example_box.layout.visibility = 'hidden'
            example_box.layout.max_height = '0px'  # Reset max_height to 0px
            example_box.layout.overflow = 'hidden'  # Set overflow to 'hidden'
            example_box.layout.display = 'none'  # Hide example box
            # Update the maximum height of the upload_message output
            upload_message.layout.max_height = '50px' if example_box.layout.visibility == 'hidden' else 'none'

    # Function to print the example content
    def print_example():
        example_content = "Filename: File_example.txt\n\n\nECOLI\t\t\tMach1::pGUS\tMach1::pC2\nSTREPTOMYCES\t\tcoelicolor\talbus\nANTIBIOTICS_PLASMID\tKanamycin\tChloramphenicol\t\tApramycin\nANTIBIOTICS_COMPETENT\tNalidixic acid\n\n\nThe capslock titles are mandatory. Use tab-separation only. If more than 1 tube\nhas the same E. coli, or the same Streptomyces, remember to state this with a number at end of name or similar indicator. See example."

        print(example_content)

    # Create a button to show or hide example
    show_example_button = Button(description="Show Example", layout=Layout(overflow='visible', max_height='none'))
    show_example_button.on_click(toggle_example)

    # Create an output widget to display the example
    example_output = Output()

    # Create a box to wrap around the example output
    example_box = Box(children=[example_output], layout=Layout(border='0.5px solid black', visibility='hidden', max_height='0px', overflow='hidden'))

    # Display the widgets
    display(lbl)
    display(upload_message)
    display(HBox([file_upload, show_example_button, example_box]))
    
    # Return a function to access the uploaded file content
    def uploaded_conjugation_content():
        return ecoli, streptomyces, plasmid_antibiotics_list, competent_antibiotics_list

    return uploaded_conjugation_content
