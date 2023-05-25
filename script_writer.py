import os
from datetime import datetime
import python_scripts.conjugation_tubesto96well as conjugation_script
import python_scripts.transformation as transformation_script

def create_conjugation_protocol(runner, conjugation_mix, ecoli_tubes):
    email = runner.email
    user = runner.email.split("@")[0]
    directory = os.getcwd()
    script = os.path.abspath(conjugation_script.__file__)
    dt_string = datetime.now().strftime("%Y%m%d")
    dt_protocol_creation = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = ""
    
    with open(script, 'r') as file:
        for line in file:
            if line.startswith("    'protocolName':"):                
                line = line.split("',")[0]
                line += " (user: " + user + ")',\n"
                #line += " (created: " + dt_protocol_creation + ", user: " + user + ")',\n"
            
            
            if line.startswith("    'author':"):
                line = "    'author': '" + email + ". Created " + dt_protocol_creation + "',\n"
            
            
            if line.startswith("default_uses ="):
                line = "default_uses = %s\n" % conjugation_mix


            if line.startswith("ecoli_tubes ="):
                line = "ecoli_tubes = %s\n" % ecoli_tubes

            changed += line

    text_file = open(directory + "/" + dt_string + "_Conjugation_OTprotocol.py", "w")

    #write string to file
    text_file.write(changed)

    #close file
    text_file.close()


def create_transformation_protocol(runner, rows, cols):
    email = runner.email
    user = runner.email.split("@")[0]
    directory = os.getcwd()
    script = os.path.abspath(transformation_script.__file__)
    dt_string = datetime.now().strftime("%Y%m%d")
    dt_protocol_creation = datetime.now().strftime("%Y-%m-%d %H:%M")
    changed = ""
    
    with open(script, 'r') as file:
        for line in file:
            if line.startswith("    'protocolName':"):                
                line = line.split("',")[0]
                line += " (user: " + user + ")',\n"
                #line += " (created: " + dt_protocol_creation + ", user: " + user + ")',\n"
            
            
            if line.startswith("    'author':"):
                line = "    'author': '" + email + ". Created " + dt_protocol_creation + "',\n"
            
            
            if line.startswith("rows ="):
                line = "rows = %s\n" % rows
                
                
            if line.startswith("columns ="):
                line = "columns = %s\n" % cols

            changed += line

    text_file = open(directory + "/" + dt_string + "_Transformation_OTprotocol.py", "w")

    #write string to file
    text_file.write(changed)

    #close file
    text_file.close()