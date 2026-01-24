import pandas as pd
import numpy as np

def load_and_clean_data(file_obj):
    df = pd.read_csv(file_obj)
    
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if df[numeric_cols].isnull().sum().sum() > 0:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    df_clean = df.dropna(thresh=3).copy()
    
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)
    
    return df_clean