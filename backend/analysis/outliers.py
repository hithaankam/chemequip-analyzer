import pandas as pd
import numpy as np


def detect_outliers_iqr(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    outlier_results = {}

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        outlier_list = []
        for _, row in outliers.iterrows():
            outlier_list.append(
                {
                    "equipment_name": str(row["Equipment Name"]),
                    "type": str(row["Type"]),
                    "value": float(row[col]),
                    "flowrate": float(row["Flowrate"]),
                    "pressure": float(row["Pressure"]),
                    "temperature": float(row["Temperature"]),
                    "deviation_type": "low" if row[col] < lower_bound else "high"
                }
            )

        outlier_results[col] = {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "normal_range": f"{lower_bound:.2f} to {upper_bound:.2f}",
            "outliers": outlier_list,
            "outlier_count": len(outlier_list),
            "total_equipment": len(df),
            "outlier_percentage": float(len(outlier_list) / len(df) * 100) if len(df) > 0 else 0.0,
            "statistics": {
                "q1": float(Q1),
                "q3": float(Q3),
                "iqr": float(IQR),
                "median": float(df[col].median()),
                "mean": float(df[col].mean())
            }
        }

    return outlier_results


def detect_outliers_zscore(df, threshold=2.0):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    outlier_results = {}
    
    for col in numeric_cols:
        mean_val = df[col].mean()
        std_val = df[col].std()
        
        if std_val == 0:
            outlier_results[col] = {
                "method": "z-score",
                "threshold": threshold,
                "outliers": [],
                "outlier_count": 0,
                "message": "No variation in data - all values are identical"
            }
            continue
        
        z_scores = np.abs((df[col] - mean_val) / std_val)
        outliers = df[z_scores > threshold]
        
        outlier_list = []
        for idx, row in outliers.iterrows():
            z_score = z_scores.loc[idx]
            outlier_list.append({
                "equipment_name": str(row["Equipment Name"]),
                "type": str(row["Type"]),
                "value": float(row[col]),
                "z_score": float(z_score),
                "flowrate": float(row["Flowrate"]),
                "pressure": float(row["Pressure"]),
                "temperature": float(row["Temperature"])
            })
        
        outlier_results[col] = {
            "method": "z-score",
            "threshold": threshold,
            "outliers": outlier_list,
            "outlier_count": len(outlier_list),
            "total_equipment": len(df),
            "outlier_percentage": float(len(outlier_list) / len(df) * 100) if len(df) > 0 else 0.0,
            "statistics": {
                "mean": float(mean_val),
                "std": float(std_val),
                "min_z_score": float(z_scores.min()),
                "max_z_score": float(z_scores.max())
            }
        }
    
    return outlier_results


def comprehensive_outlier_analysis(df):
    analysis = {
        "iqr_method": detect_outliers_iqr(df),
        "zscore_method": detect_outliers_zscore(df, threshold=2.0),
        "summary": {
            "total_equipment": len(df),
            "methods_used": ["IQR", "Z-Score"],
            "outlier_summary": {}
        }
    }
    
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    for col in numeric_cols:
        iqr_outliers = len(analysis["iqr_method"][col]["outliers"])
        zscore_outliers = len(analysis["zscore_method"][col]["outliers"])
        
        analysis["summary"]["outlier_summary"][col] = {
            "iqr_outliers": iqr_outliers,
            "zscore_outliers": zscore_outliers,
            "consensus_outliers": get_consensus_outliers(
                analysis["iqr_method"][col]["outliers"],
                analysis["zscore_method"][col]["outliers"]
            )
        }
    
    return analysis


def get_consensus_outliers(iqr_outliers, zscore_outliers):
    iqr_names = {outlier["equipment_name"] for outlier in iqr_outliers}
    zscore_names = {outlier["equipment_name"] for outlier in zscore_outliers}
    
    consensus_names = iqr_names.intersection(zscore_names)
    
    consensus_outliers = []
    for outlier in iqr_outliers:
        if outlier["equipment_name"] in consensus_names:
            consensus_outliers.append(outlier)
    
    return {
        "count": len(consensus_outliers),
        "equipment": consensus_outliers
    }


def analyze_outlier_patterns(df):
    outlier_analysis = comprehensive_outlier_analysis(df)
    
    patterns = {
        "equipment_type_outliers": {},
        "multi_parameter_outliers": [],
        "outlier_characteristics": {}
    }
    
    all_outlier_equipment = set()
    for col in ["Flowrate", "Pressure", "Temperature"]:
        for outlier in outlier_analysis["iqr_method"][col]["outliers"]:
            all_outlier_equipment.add(outlier["equipment_name"])
    
    for equipment_name in all_outlier_equipment:
        equipment_row = df[df["Equipment Name"] == equipment_name].iloc[0]
        outlier_params = []
        
        for col in ["Flowrate", "Pressure", "Temperature"]:
            for outlier in outlier_analysis["iqr_method"][col]["outliers"]:
                if outlier["equipment_name"] == equipment_name:
                    outlier_params.append(col)
        
        if len(outlier_params) > 1:
            patterns["multi_parameter_outliers"].append({
                "equipment_name": equipment_name,
                "type": str(equipment_row["Type"]),
                "outlier_parameters": outlier_params,
                "parameter_count": len(outlier_params)
            })
    
    type_outlier_counts = {}
    for equipment_name in all_outlier_equipment:
        equipment_row = df[df["Equipment Name"] == equipment_name].iloc[0]
        equipment_type = str(equipment_row["Type"])
        
        if equipment_type not in type_outlier_counts:
            type_outlier_counts[equipment_type] = 0
        type_outlier_counts[equipment_type] += 1
    
    patterns["equipment_type_outliers"] = type_outlier_counts
    
    patterns["outlier_characteristics"] = {
        "total_outlier_equipment": len(all_outlier_equipment),
        "multi_parameter_outliers_count": len(patterns["multi_parameter_outliers"]),
        "single_parameter_outliers_count": len(all_outlier_equipment) - len(patterns["multi_parameter_outliers"])
    }
    
    return patterns
