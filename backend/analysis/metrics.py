import pandas as pd


def compute_basic_metrics(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]

    metrics = {"total_equipment_count": len(df), "overall_stats": {}}

    for col in numeric_cols:
        metrics["overall_stats"][col] = {
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
        }

    return metrics


def compute_type_metrics(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    type_stats = {}

    for equipment_type in df["Type"].unique():
        subset = df[df["Type"] == equipment_type]
        type_stats[equipment_type] = {}

        for col in numeric_cols:
            type_stats[equipment_type][col] = {
                "mean": float(subset[col].mean()),
                "std": float(subset[col].std()),
                "min": float(subset[col].min()),
                "max": float(subset[col].max()),
            }

    return type_stats
