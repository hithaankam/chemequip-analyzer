import pandas as pd
import numpy as np


def get_equipment_type_distribution(df):
    distribution = df["Type"].value_counts().to_dict()
    return {str(k): int(v) for k, v in distribution.items()}


def get_grouped_averages(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    averages = {}

    for equipment_type in df["Type"].unique():
        subset = df[df["Type"] == equipment_type]
        averages[equipment_type] = {}

        for col in numeric_cols:
            averages[equipment_type][col] = float(subset[col].mean())

    return averages


def compute_correlation_matrix(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    df_encoded = pd.get_dummies(df, columns=['Type'], prefix='Type')
    numeric_df = df_encoded.select_dtypes(include=['number', 'bool'])
    corr_matrix = numeric_df.corr()

    correlations = {}
    for col1 in numeric_cols:
        correlations[col1] = {}
        for col2 in numeric_cols:
            if col1 in corr_matrix.columns and col2 in corr_matrix.columns:
                correlations[col1][col2] = float(corr_matrix.loc[col1, col2])

    key_correlations = {
        "flowrate_temperature": float(corr_matrix.loc['Flowrate', 'Temperature']) if 'Flowrate' in corr_matrix.columns and 'Temperature' in corr_matrix.columns else 0.0,
        "flowrate_pressure": float(corr_matrix.loc['Flowrate', 'Pressure']) if 'Flowrate' in corr_matrix.columns and 'Pressure' in corr_matrix.columns else 0.0,
        "pressure_temperature": float(corr_matrix.loc['Pressure', 'Temperature']) if 'Pressure' in corr_matrix.columns and 'Temperature' in corr_matrix.columns else 0.0
    }

    return {
        "correlation_matrix": correlations,
        "key_correlations": key_correlations,
        "equipment_type_correlations": get_equipment_type_correlations(df_encoded, corr_matrix)
    }


def get_equipment_type_correlations(df_encoded, corr_matrix):
    type_cols = [col for col in df_encoded.columns if col.startswith('Type_')]
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    
    type_correlations = {}
    for type_col in type_cols:
        equipment_type = type_col.replace('Type_', '')
        type_correlations[equipment_type] = {}
        
        for metric in numeric_cols:
            if type_col in corr_matrix.columns and metric in corr_matrix.columns:
                type_correlations[equipment_type][metric] = float(corr_matrix.loc[type_col, metric])
    
    return type_correlations


def detect_high_temperature_equipment(df, threshold=100):
    high_temp = df[df["Temperature"] >= threshold]

    results = {
        "count": len(high_temp),
        "total_equipment": len(df),
        "threshold": threshold,
        "percentage": float(len(high_temp) / len(df) * 100) if len(df) > 0 else 0.0,
        "equipment_list": [],
        "temperature_stats": {
            "min": float(df["Temperature"].min()),
            "max": float(df["Temperature"].max()),
            "mean": float(df["Temperature"].mean()),
            "std": float(df["Temperature"].std())
        }
    }

    for _, row in high_temp.iterrows():
        results["equipment_list"].append(
            {
                "equipment_name": str(row["Equipment Name"]),
                "type": str(row["Type"]),
                "temperature": float(row["Temperature"]),
                "pressure": float(row["Pressure"]),
                "flowrate": float(row["Flowrate"]),
            }
        )

    return results


def get_top_performers(df):
    metrics = ["Flowrate", "Pressure", "Temperature"]
    top_performers = {}

    for metric in metrics:
        top_5 = df.nlargest(5, metric)
        top_performers[metric] = []

        for _, row in top_5.iterrows():
            top_performers[metric].append(
                {
                    "equipment_name": str(row["Equipment Name"]),
                    "type": str(row["Type"]),
                    "flowrate": float(row["Flowrate"]),
                    "pressure": float(row["Pressure"]),
                    "temperature": float(row["Temperature"]),
                }
            )

    return top_performers


def generate_comprehensive_insights(df, efficiency_rankings, correlations):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    
    insights = {
        "dataset_overview": {
            "total_equipment": len(df),
            "equipment_types": len(df["Type"].unique()),
            "parameter_ranges": {}
        },
        "equipment_type_analysis": {},
        "high_performance_equipment": {},
        "correlation_insights": {},
        "recommendations": []
    }
    
    for col in numeric_cols:
        insights["dataset_overview"]["parameter_ranges"][col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": float(df[col].mean()),
            "std": float(df[col].std())
        }
    
    type_counts = df["Type"].value_counts()
    for eq_type, count in type_counts.items():
        subset = df[df["Type"] == eq_type]
        insights["equipment_type_analysis"][eq_type] = {
            "count": int(count),
            "avg_temperature": float(subset["Temperature"].mean()),
            "avg_pressure": float(subset["Pressure"].mean()),
            "avg_flowrate": float(subset["Flowrate"].mean()),
            "performance_summary": f"Avg Temp={subset['Temperature'].mean():.1f}, Pressure={subset['Pressure'].mean():.1f}, Flowrate={subset['Flowrate'].mean():.1f}"
        }
    
    if isinstance(efficiency_rankings, dict) and "overall_efficiency" in efficiency_rankings and len(efficiency_rankings["overall_efficiency"]) > 0:
        best_equipment = efficiency_rankings["overall_efficiency"][0]
        insights["high_performance_equipment"] = {
            "best_performer": {
                "equipment_name": best_equipment["equipment_name"],
                "type": best_equipment["type"],
                "efficiency_score": best_equipment["efficiency_score"]
            },
            "top_3_performers": efficiency_rankings["overall_efficiency"][:3]
        }
    elif isinstance(efficiency_rankings, list) and len(efficiency_rankings) > 0:
        best_equipment = efficiency_rankings[0]
        insights["high_performance_equipment"] = {
            "best_performer": {
                "equipment_name": best_equipment["equipment_name"],
                "type": best_equipment["type"],
                "efficiency_score": best_equipment["efficiency_score"]
            },
            "top_3_performers": efficiency_rankings[:3]
        }
    
    if "key_correlations" in correlations:
        key_corr = correlations["key_correlations"]
        insights["correlation_insights"] = {
            "flowrate_temperature": key_corr.get("flowrate_temperature", 0.0),
            "flowrate_pressure": key_corr.get("flowrate_pressure", 0.0),
            "pressure_temperature": key_corr.get("pressure_temperature", 0.0),
            "strongest_correlation": max(key_corr.items(), key=lambda x: abs(x[1])) if key_corr else ("none", 0.0)
        }
    
    insights["recommendations"] = [
        "Monitor high-temperature equipment for potential efficiency improvements",
        "Consider equipment type-specific optimization strategies",
        "Focus on equipment with strong flowrate-temperature correlations for performance tuning",
        "Implement predictive maintenance for top-performing equipment",
        "Analyze outliers for potential process improvements"
    ]
    
    return insights
