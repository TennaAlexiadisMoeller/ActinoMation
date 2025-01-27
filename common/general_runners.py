#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:20:20 2023

@author: tgrra

This script is licensed under the MIT License. See the LICENSE.txt file for details.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from ipywidgets import Textarea, Layout, Label, Button, HBox, VBox
from pyisemail import is_email

text_area_email = Textarea(layout = Layout(width = '300px', height = '40px'))
lbl_choice = Label(value = "")

@dataclass
class Runner:
    now: float = None
    total_runtime: float = None
    rows: int = 0
    cols: int = 0
    email: str = "ERROR_User"

    def __post_init__(self):
        if self.now is None:
            self.now = datetime.now()


    def finished(self):
        self.total_runtime = datetime.now() - self.now

    def check_args(self, **kwargs):
        raise NotImplementedError()

    def run(self, **kwargs):
        raise NotImplementedError()

    @classmethod
    def from_notebook(cls, notebook):
        raise NotImplementedError()
        
    @staticmethod
    def get_script():
        raise NotImplementedError()
        
    def display_form(self, **kwargs):
        lbl_email = Label(value = "Write your email address to create your .py protocol and save all necessary files.")

        submit_button_save=Button(description='Submit',button_style='success',
                         layout = text_area_email.layout)

        def on_button_clicked_submit(_choice):

            self.email = text_area_email.value
            is_email_valid = is_email(self.email, check_dns=True)

            if is_email_valid == False:
                lbl_choice.value = "'" + text_area_email.value + "' does not have a valid email domain. Please check and press 'submit' again."

            else:
                errors = self.check_args(**kwargs)
                if errors:
                    lbl_choice.value = errors
                else:
                    lbl_choice.value = "protocol, runlog and all relevant files have now been saved in a .zip file"
                    self.run()


        submit_button_save.on_click(on_button_clicked_submit)

        email_submit_box = HBox([text_area_email,submit_button_save],
                         layout=Layout(display='flex',
                                        width='100%',
                                        height = '50px'))

        scene = VBox([lbl_email,email_submit_box,lbl_choice],
                     layout= Layout(display='flex',
                                   width='100%'))
    
        display(scene)

    
    
