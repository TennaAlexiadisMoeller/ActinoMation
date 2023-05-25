from opentrons.simulate import simulate, format_runlog
import os
import zipfile

def build_report(runner, runlog, extra_lines="", samples = 0):
    now = runner.now
    assay = runner.assay
    email = runner.email
    user = runner.email.split("@")[0]
    dt_string = now.strftime("%Y%m%d")
        
    text_file = open(dt_string + "_" + assay + "_runlog.txt", "w")

    text_file.write("########################################################### META DATA ##########################################################\n\n" +
                    "Date:                                   " + str(now.strftime("%d-%m-%Y")) + 
                    "\nTime:                                   " + str(now.strftime("%-H:%M")) +
                    "\nUser/email:                             " + email.split("@")[0] + "/" + email +
                    "\nAssay:                                  " + assay +
                    "\nRun time (incl. homing):                " + str(runner.total_runtime) + 
                    "\n"                                         + extra_lines +
                    "\n\n############################################################ RUN LOG ###########################################################\n\n")
    
    text_file.write(format_runlog(runlog))
    text_file.close()   
    
    #Zipping the files#
    filenames = list()
    
    for file in os.listdir():
        if dt_string in file:
            if assay in file:
                
                #insert username from email in all files
                new_file = (dt_string + "_" + user).join(file.split(dt_string))
                os.rename(os.getcwd() + "/" + file, os.getcwd() + "/" + new_file)
                
                filenames.append(new_file)
    
    with zipfile.ZipFile(dt_string + "_" + user + "_" + assay +  "_files.zip", mode="w") as archive:
        for filename in filenames:
            archive.write(filename)
    
    for file in filenames:
        os.remove(file)