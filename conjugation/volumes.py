#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:11:18 2023

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

import ipywidgets as widgets
import numpy as np
from ipywidgets import  Layout, Textarea, Label, Dropdown, VBox, Box, Text

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
