from opentrons.simulate import simulate, format_runlog
import os
import zipfile

def build_report(runner, runlog, extra_lines="", samples = 0):
    files = "files"
    now = runner.now
    assay = runner.assay
    email = runner.email
    user = runner.email.split("@")[0]
    dt_string = now.strftime("%Y%m%d")
    filename_zip = dt_string + "_" + user + "_" + assay +  "_" + files + ".zip"
        
    text_file = open(dt_string + "_" + assay + "_runlog.txt", "w")

    text_file.write("########################################################### META DATA ##########################################################\n\n" +
                    "Date:                                   " + str(now.strftime("%d-%m-%Y")) + 
                    "\nTime:                                   " + str(now.strftime("%-H:%M")) +
                    "\nUser/email:                             " + email.split("@")[0] + "/" + email +
                    "\nAssay:                                  " + assay + 
                    "\n"                                         + extra_lines +
                    "\n\n############################################################ RUN LOG ###########################################################\n\n")
    
    text_file.write(format_runlog(runlog))
    text_file.close()   
    

    filenames = list()
    
    for file in os.listdir():
        if dt_string in file:
            if assay in file:
                
                #insert username from email in all files
                if ".zip" not in file:
                    new_file = (dt_string + "_" + user).join(file.split(dt_string))
                    os.rename(os.path.join(os.getcwd(), file), os.path.join(os.getcwd(), new_file))

                    filenames.append(new_file)

                    
    #Checking if the file already exists 
    file_path = os.path.join(os.getcwd(), filename_zip)
    if os.path.exists(file_path):
        file_dir, file_name = os.path.split(file_path)
        base_name, ext = os.path.splitext(file_name)
        count = 1
        while os.path.exists(os.path.join(file_dir, f"{base_name}_{count}{ext}")):
            count += 1
        filename_zip = f"{base_name}_{count}{ext}"
 

    #Zipping the files#    
    with zipfile.ZipFile(filename_zip, mode="w") as archive:
        for filename in filenames:
            archive.write(filename)
    
    for file in filenames:
        if ".zip" not in file:
            os.remove(file)  

 

