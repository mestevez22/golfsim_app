#load packages
import pandas as pd
import numpy as np
import os
import json
import datetime
import traceback
import shutil
from pathlib import Path
from create_init import clean


# #set paths 
base_path = Path(__file__).resolve().parent #path of script
csv_path = base_path.parent #path of csv files
out_path = base_path / "master.csv" #path for output 
desktop_path = csv_path.parent

#GSPRO exports to desktop
#check for new gspro files in desktop and move to folder
#print(gspro_files)
try:
    gspro_files = [f for f in os.listdir(desktop_path) if f.startswith("gspro")]
    for f in gspro_files:
        source = os.path.join(desktop_path, f)
        dest = os.path.join(csv_path, f)
        shutil.move(source, dest)
        print(f"File {f} moved to {csv_path} successfully")

except Exception as e:
    print(f"Error occurred, {str(e)}")



# #open current log file and grab last run date 
# filename = base_path / 'log.json'
# with open(filename, "r") as f:
#     current_log = json.load(f)

# idx = len(current_log) - 1
# target_date = pd.to_datetime(current_log[idx]['last_run'])

# #set initial log status
# status = 'failure'
# err = None
# new_dfs = []

# try:
#     #collect files that need to be added 
#     files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
#     files_to_process = []
 
#     for file in files:
#         try:
#             str_dt = str(file).split("export")[-1].split(".csv")[0]
#             str_dt = str_dt[:-9] #extract date 
#             dt = pd.to_datetime(str_dt) #convert to dt

#             if dt >= target_date:
#                 files_to_process.append(file)
#         except Exception as e:
#             print(f"Skipping {file} - date parsing error, {str(e)}")
#             continue 

#     #process new files if the last run was successful
#     if len(files_to_process) != 0 and current_log[idx]['status'] == 'success':
#         for i, f in enumerate(files_to_process):
#             try:
#                 file_path = os.path.join(csv_path, f)
#                 df = clean(file_path)
#                 df = df.iloc[1:, :] #drop header row 
#                 new_dfs.append(df)
#                 print(f" Processed file {i + 1}/{len(files_to_process)}")
       
#             except Exception as e:
#                 status = 'failure'
#                 err = f"Error processing: {str(e)}"
#                 print("Unable to complete processing", err)
#                 break

#         #update master file if all files were processed successfully 
#         if len(new_dfs) == len(files_to_process):
#             try:
#                 master_df = pd.read_csv(out_path)
#                 new_data = pd.concat(new_dfs, ignore_index = True)
#                 new_master = pd.concat([master_df, new_data], ignore_index = True)
#                 new_master.to_csv(out_path)
#                 status = 'success'
#                 print("Master file updated successfully")

#             except Exception as e:
#                 status = 'failure'
#                 err = f"Master file update failed: {str(e)}"
#                 print("Unable to update Master file", err)

#     elif len(files_to_process) == 0:
#         status = 'success'  
#         print("No new files to process")
    
#     else:
#         status = 'failure'
#         err = "Last run was unsuccessful, cannot process new files. Please confirm target date"
#         print(err)

# except Exception as e:
#     status = 'failure'
#     err = f"Unexpected error, {str(e)}"
#     print(err)
#     traceback.print_exc()


                        
# #### UPDATE LOG FILE #####
# today = datetime.date.today()
# #log_file = []
# log = {'last_run': today.isoformat(),
#         'status': status,
#         'error' : err,
#         'files_processed': files_to_process if len(files_to_process) == len(new_dfs) and status == 'success'else []}
# current_log.append(log)

# with open(filename, 'w') as outfile:
#     json.dump(current_log, outfile, indent = 2)


# print(f"Log data written to '{filename}' successfully.")

            
                            
                
                     
                            



