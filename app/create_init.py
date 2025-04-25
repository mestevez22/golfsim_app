#load packages
import pandas as pd
import numpy as np
import os
import json
import datetime
import traceback
from pathlib import Path

#function to clean up csv files
def clean(df):
    #distanceto pin = object (yrds/ft, etc)
    #club = object
    '''
    #1 remove cols with 0 across all rows
    #2 standardize distance to pin : all --> yards
    # replace ft with yds
    ''' 

    clean = df.loc[:, (df!=0).all(axis=0)].copy() #drop zero cols
    clean['DistanceToPin_Yrds'] = clean['DistanceToPin'].apply(lambda x: round(float(x.split(" ")[0])/3, 2) if 'ft' in str(x.split(" ")[1]) else x) #change to yrds
    clean['DistanceToPin_Yrds'] = clean['DistanceToPin'].apply(lambda x: str(x.split(" ")[1]) .replace("ft", "yds")) #change to yrds
    clean = clean.drop('DistanceToPin', axis = 1)
    return clean

############### DO NOT RERUN - CREATION OF INITIAL MASTER DATA AND LOG FILE ###############
#set paths 
base_path = Path(__file__).resolve().parent #path of script
csv_path = base_path.parent #path of csv files
out_path = base_path / "master.csv" #path for output 

#clean and merge csv files
try:
    files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
    all_dfs =[]
    for i, f in enumerate(files):
        df = pd.read_csv(f)
        df = clean(df)
        if i != 0:
            df = df.iloc[1:, :] #drop header row 
        all_dfs.append(df)
        print(f" Processed file {i + 1}/{len(files)}")
        
    print("File processing complete")
    #join all files
    master_df = pd.concat(all_dfs, ignore_index = True)
    master_df.to_csv(out_path)
    print("Master file written successfully")
    status = 'success'
    err = None
    
except Exception as e:
    status = 'failure'
    err = str(e)
    print("Unable to complete both processing and create master file")

#### CREATE SIMPLE LOG FILE #####
today = datetime.date.today()
log_file = []
log = {'last_run': today.isoformat(),
       'status': status,
       'error' : err,
       'files_processed': files}
log_file.append(log)

filename = base_path / 'log.json'
with open(filename, 'w') as outfile:
    json.dump(log_file, outfile)


print(f"Log data written to '{filename}' successfully.")
