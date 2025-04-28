#load packages
import pandas as pd
import numpy as np
import os
import json
import datetime
import traceback
from pathlib import Path

#function to clean up csv files
def clean(file):
    #distanceto pin = object (yrds/ft, etc)
    #club = object
    '''
    #1 extract timestamp from filename
    #2 remove cols with 0 across all rows
    #3 add col with timestamp
    #4 standardize distance to pin : all --> yards
    #5 replace ft with yds
    #6 drop original distancetopin col
    ''' 
    ts_str = str(file).split("export")[-1].split(".csv")[0]
    dt = pd.to_datetime(ts_str, format='%m-%d-%y-%H-%M-%S') #convert to dt 
    df = pd.read_csv(file)
    clean = df.loc[:, (df!=0).all(axis=0)].copy() #drop zero cols
    clean['Date'] = dt 
    clean['DistanceToPin_Yrds'] = clean['DistanceToPin'].apply(lambda x: round(float(x.split(" ")[0])/3, 2) if 'ft' in str(x.split(" ")[1]) else x) #change to yrds
    clean['DistanceToPin_Yrds'] = clean['DistanceToPin'].apply(lambda x: f"{x.split(' ')[0]} yds" if "ft" in x else x)
    clean = clean.drop('DistanceToPin', axis = 1)
    return clean



############## DO NOT RERUN - CREATION OF INITIAL MASTER DATA AND LOG FILE ###############
# #set paths 
# base_path = Path(__file__).resolve().parent #path of script
# csv_path = base_path.parent #path of csv files
# out_path = base_path / "master.csv" #path for output 

# #clean and merge csv files
# try:
#     files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
#     all_dfs =[]
#     for i, f in enumerate(files):
#         file_path = csv_path / f
#         #print(file_path)
#         df = clean(file_path)
#         if i != 0:
#             df = df.iloc[1:, :] #drop header row 
#         all_dfs.append(df)
#         print(f" Processed file {i + 1}/{len(files)}")
        
#     print("File processing complete")
#     #join all files
#     master_df = pd.concat(all_dfs, ignore_index = True)
#     master_df.to_csv(out_path)
#     print("Master file written successfully")
#     status = 'success'
#     err = None
    
# except Exception as e:
#     status = 'failure'
#     err = str(e)
#     print("Unable to complete both processing and create master file")
#     print(err)

# #### CREATE SIMPLE LOG FILE #####
# today = datetime.date.today()
# log_file = []
# log = {'last_run': today.isoformat(),
#        'status': status,
#        'error' : err,
#        'files_processed': files}
# log_file.append(log)

# filename = base_path / 'log.json'
# with open(filename, 'w') as outfile:
#     json.dump(log_file, outfile)


# print(f"Log data written to '{filename}' successfully.")
