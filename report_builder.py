from opentrons.simulate import simulate, format_runlog

def build_report(runner, runlog, extra_lines="", samples = 0):
    now = runner.now
    assay = runner.assay
    email = runner.email
    dt_string = now.strftime("%Y%m%d")
        
    text_file = open(dt_string + "_" + assay + "_runlog.txt", "w")

    text_file.write("########################################################### META DATA ##########################################################\n\n" +
                    "Date:                      " + str(now.strftime("%d-%m-%Y")) + 
                    "\nTime:                      " + str(now.strftime("%-H:%M")) +
                    "\nUser/email:                " + email.split("@")[0] + "/" + email +
                    "\nAssay:                     " + assay +
                    "\nRun time (incl. homing):   " + str(runner.total_runtime) + 
                    "\n"                            + extra_lines +
                    "\n\n############################################################ RUN LOG ###########################################################\n\n")
    
    text_file.write(format_runlog(runlog))
    text_file.close()
