import pandas as pd
import numpy as np

def normalize_data(df):
    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    df_norm = df.copy()
    
    for col in numeric_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        df_norm[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
    
    return df_norm

def compute_efficiency_scores(df):
    df_efficiency = normalize_data(df)
    
    temp_efficiency = 1 - abs(df_efficiency['Temperature_norm'] - 0.7)
    df_efficiency['Efficiency_Score'] = (
        df_efficiency['Flowrate_norm'] * 0.4 + 
        df_efficiency['Pressure_norm'] * 0.3 + 
        temp_efficiency * 0.3
    )
    
    return df_efficiency

def rank_equipment_by_efficiency(df):
    df_efficiency = compute_efficiency_scores(df)
    df_ranked = df_efficiency.sort_values('Efficiency_Score', ascending=False)
    
    rankings = []
    for _, row in df_ranked.iterrows():
        rankings.append({
            'equipment_name': str(row['Equipment Name']),
            'type': str(row['Type']),
            'flowrate': float(row['Flowrate']),
            'pressure': float(row['Pressure']),
            'temperature': float(row['Temperature']),
            'efficiency_score': float(row['Efficiency_Score'])
        })
    
    return rankings

def compute_efficiency_by_type(df):
    df_efficiency = compute_efficiency_scores(df)
    type_efficiency = {}
    
    for equipment_type in df['Type'].unique():
        subset = df_efficiency[df_efficiency['Type'] == equipment_type]
        type_efficiency[equipment_type] = {
            'mean': float(subset['Efficiency_Score'].mean()),
            'std': float(subset['Efficiency_Score'].std()),
            'count': int(len(subset))
        }
    
    return type_efficiency