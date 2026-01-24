import pandas as pd


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
                }
            )

        outlier_results[col] = {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound),
            "outliers": outlier_list,
        }

    return outlier_results
