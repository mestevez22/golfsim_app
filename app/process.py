#load packages
import pandas as pd
import numpy as np
from pathlib import Path

class Preprocessor:
    def __init__(self, filename = 'master.csv'):
        self.path = Path(__file__).resolve().parent
        self.filename = filename
        self.file = self.path / self.filename
        self.raw_df = None
        self.clean_df = None
    
    def load_data(self):
        self.raw_df = pd.read_csv(self.file)
        self.raw_df['Date'] = pd.to_datetime(self.raw_df['Date'])
        self.raw_df['DistanceToPin_Yrds'] = self.raw_df['DistanceToPin_Yrds'].apply(lambda x: float(x.split(' ')[0]) if pd.notnull(x) else np.nan) #exclude "yrds" string
        self.raw_df = self.raw_df.rename(columns = {'DistanceToPin_Yrds': 'DistanceToPin'})
        return self.raw_df
    
    def remove_outliers(self, col):
        if not np.issubdtype(col.dtype, np.number):
            return col  #skip cols non-numeric
    
        #IQR method
        q1 = np.percentile(col.dropna(), 25, method='midpoint') #exclude nans
        q3 = np.percentile(col.dropna(), 75, method='midpoint') #exclude nans
        IQR = q3 -q1  
        upper = q3+1.5*IQR
        lower = q1-1.5*IQR
        return col.where((col >= lower) & (col <= upper))
    
    def round_vals(self, col):
        if not np.issubdtype(col.dtype, np.number):
            return col  #skip cols non-numeric
        return col.round(3)
    
    def process_data(self):
        if self.raw_df is None:
            self.load_data()
        df = self.raw_df.copy()
        #loop thru numeric cols 
        for col in df.select_dtypes(include='number').columns:
            df[col] = self.remove_outliers(df[col]) #remoce outliers
            df[col] = self.round_vals(df[col]) #round vals with > dec. points
        self.clean_df = df
        return self.clean_df

    def get_data(self):
        if self.clean_df is None:
            self.process_data()
        return self.clean_df

        

