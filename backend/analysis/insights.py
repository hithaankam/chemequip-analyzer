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
    corr_matrix = df[numeric_cols].corr()

    correlations = {}
    for i, col1 in enumerate(numeric_cols):
        correlations[col1] = {}
        for j, col2 in enumerate(numeric_cols):
            correlations[col1][col2] = float(corr_matrix.iloc[i, j])

    return correlations


def detect_high_temperature_equipment(df, threshold=100):
    high_temp = df[df["Temperature"] >= threshold]

    results = {
        "count": len(high_temp),
        "total_equipment": len(df),
        "equipment_list": [],
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
