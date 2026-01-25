import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import MinMaxScaler


def compute_basic_metrics(df):
    """Compute comprehensive basic metrics matching the EDA notebook analysis"""
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]

    metrics = {
        "dataset_overview": {
            "total_equipment_count": len(df),
            "equipment_types_count": len(df["Type"].unique()),
            "equipment_types": list(df["Type"].unique()),
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "duplicate_equipment_names": int(df.duplicated(subset=['Equipment Name']).sum())
        },
        "overall_stats": {},
        "statistical_summary": {},
        "data_quality": {
            "completeness": float((1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100),
            "uniqueness": {
                "equipment_names": len(df["Equipment Name"].unique()),
                "total_rows": len(df)
            }
        }
    }

    # Enhanced statistical analysis
    for col in numeric_cols:
        series = df[col]
        metrics["overall_stats"][col] = {
            "mean": float(series.mean()),
            "min": float(series.min()),
            "max": float(series.max()),
            "std": float(series.std()),
            "median": float(series.median()),
            "q25": float(series.quantile(0.25)),
            "q75": float(series.quantile(0.75)),
            "range": float(series.max() - series.min()),
            "variance": float(series.var()),
            "coefficient_of_variation": float(series.std() / series.mean()) if series.mean() != 0 else 0.0,
            "skewness": float(series.skew()),
            "kurtosis": float(series.kurtosis()),
            "percentiles": {
                "p10": float(series.quantile(0.1)),
                "p90": float(series.quantile(0.9)),
                "p95": float(series.quantile(0.95)),
                "p99": float(series.quantile(0.99))
            }
        }

    # Detailed statistical summary
    describe_stats = df[numeric_cols].describe()
    for col in numeric_cols:
        metrics["statistical_summary"][col] = {
            "count": float(describe_stats.loc["count", col]),
            "mean": float(describe_stats.loc["mean", col]),
            "std": float(describe_stats.loc["std", col]),
            "min": float(describe_stats.loc["min", col]),
            "25%": float(describe_stats.loc["25%", col]),
            "50%": float(describe_stats.loc["50%", col]),
            "75%": float(describe_stats.loc["75%", col]),
            "max": float(describe_stats.loc["max", col])
        }

    return metrics


def compute_type_metrics(df):
    """Enhanced equipment type analysis matching EDA notebook depth"""
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    type_stats = {}

    # Equipment type distribution analysis
    type_counts = df["Type"].value_counts()
    
    for equipment_type in df["Type"].unique():
        subset = df[df["Type"] == equipment_type]
        type_stats[equipment_type] = {
            "count": len(subset),
            "percentage": float(len(subset) / len(df) * 100),
            "metrics": {},
            "performance_summary": {},
            "operational_characteristics": {}
        }

        # Detailed metrics for each parameter
        for col in numeric_cols:
            series = subset[col]
            type_stats[equipment_type]["metrics"][col] = {
                "mean": float(series.mean()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "median": float(series.median()),
                "range": float(series.max() - series.min()),
                "coefficient_of_variation": float(series.std() / series.mean()) if series.mean() != 0 else 0.0,
                "quartiles": {
                    "q1": float(series.quantile(0.25)),
                    "q3": float(series.quantile(0.75)),
                    "iqr": float(series.quantile(0.75) - series.quantile(0.25))
                }
            }
        
        # Performance characteristics
        type_stats[equipment_type]["performance_summary"] = {
            "avg_flowrate": float(subset["Flowrate"].mean()),
            "avg_pressure": float(subset["Pressure"].mean()),
            "avg_temperature": float(subset["Temperature"].mean()),
            "performance_index": float(
                (subset["Flowrate"].mean() / df["Flowrate"].mean() + 
                 subset["Pressure"].mean() / df["Pressure"].mean() + 
                 subset["Temperature"].mean() / df["Temperature"].mean()) / 3
            )
        }
        
        # Operational characteristics
        type_stats[equipment_type]["operational_characteristics"] = {
            "high_temperature_count": int(len(subset[subset["Temperature"] >= 120])),
            "high_pressure_count": int(len(subset[subset["Pressure"] >= 7.0])),
            "high_flowrate_count": int(len(subset[subset["Flowrate"] >= 140])),
            "operational_efficiency": calculate_type_efficiency(subset)
        }

    return type_stats


def calculate_type_efficiency(subset):
    """Calculate operational efficiency for equipment type"""
    if len(subset) == 0:
        return 0.0
    
    # Normalize values within the subset
    scaler = MinMaxScaler()
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    
    try:
        normalized = scaler.fit_transform(subset[numeric_cols])
        # Calculate efficiency score (higher flowrate and pressure, moderate temperature)
        temp_efficiency = 1 - abs(normalized[:, 2] - 0.7)  # Optimal around 70% of max temp
        efficiency_scores = (normalized[:, 0] * 0.4 + normalized[:, 1] * 0.3 + temp_efficiency * 0.3)
        return float(np.mean(efficiency_scores))
    except:
        return 0.0


def compute_advanced_statistics(df):
    """Comprehensive advanced statistical analysis matching EDA notebook"""
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    
    advanced_stats = {
        "variance_analysis": {},
        "distribution_analysis": {},
        "normality_tests": {},
        "percentile_analysis": {},
        "correlation_analysis": {},
        "parameter_relationships": {}
    }
    
    for col in numeric_cols:
        series = df[col]
        
        # Variance and dispersion analysis
        advanced_stats["variance_analysis"][col] = {
            "variance": float(series.var()),
            "standard_deviation": float(series.std()),
            "coefficient_of_variation": float(series.std() / series.mean()) if series.mean() != 0 else 0.0,
            "mean_absolute_deviation": float(np.mean(np.abs(series - series.mean()))),
            "range": float(series.max() - series.min()),
            "interquartile_range": float(series.quantile(0.75) - series.quantile(0.25))
        }
        
        # Distribution characteristics
        advanced_stats["distribution_analysis"][col] = {
            "skewness": float(series.skew()),
            "kurtosis": float(series.kurtosis()),
            "is_normal_distributed": bool(abs(series.skew()) < 0.5 and abs(series.kurtosis()) < 0.5),
            "distribution_type": classify_distribution(series)
        }
        
        # Normality tests
        try:
            shapiro_stat, shapiro_p = stats.shapiro(series)
            advanced_stats["normality_tests"][col] = {
                "shapiro_wilk_statistic": float(shapiro_stat),
                "shapiro_wilk_p_value": float(shapiro_p),
                "is_normal_shapiro": bool(shapiro_p > 0.05)
            }
        except:
            advanced_stats["normality_tests"][col] = {
                "shapiro_wilk_statistic": None,
                "shapiro_wilk_p_value": None,
                "is_normal_shapiro": None
            }
        
        # Comprehensive percentile analysis
        advanced_stats["percentile_analysis"][col] = {
            "p1": float(series.quantile(0.01)),
            "p5": float(series.quantile(0.05)),
            "p10": float(series.quantile(0.1)),
            "p25": float(series.quantile(0.25)),
            "p50": float(series.quantile(0.5)),
            "p75": float(series.quantile(0.75)),
            "p90": float(series.quantile(0.9)),
            "p95": float(series.quantile(0.95)),
            "p99": float(series.quantile(0.99))
        }
    
    # Correlation analysis
    corr_matrix = df[numeric_cols].corr()
    advanced_stats["correlation_analysis"] = {
        "correlation_matrix": corr_matrix.to_dict(),
        "strong_correlations": find_strong_correlations(corr_matrix),
        "correlation_summary": {
            "flowrate_pressure": float(corr_matrix.loc["Flowrate", "Pressure"]),
            "flowrate_temperature": float(corr_matrix.loc["Flowrate", "Temperature"]),
            "pressure_temperature": float(corr_matrix.loc["Pressure", "Temperature"])
        }
    }
    
    # Parameter relationships
    advanced_stats["parameter_relationships"] = analyze_parameter_relationships(df)
    
    return advanced_stats


def classify_distribution(series):
    """Classify the distribution type based on skewness and kurtosis"""
    skew = series.skew()
    kurt = series.kurtosis()
    
    if abs(skew) < 0.5 and abs(kurt) < 0.5:
        return "Normal"
    elif skew > 0.5:
        return "Right-skewed"
    elif skew < -0.5:
        return "Left-skewed"
    elif kurt > 0.5:
        return "Heavy-tailed"
    elif kurt < -0.5:
        return "Light-tailed"
    else:
        return "Unknown"


def find_strong_correlations(corr_matrix, threshold=0.7):
    """Find strong correlations above threshold"""
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                strong_corr.append({
                    "variable1": corr_matrix.columns[i],
                    "variable2": corr_matrix.columns[j],
                    "correlation": float(corr_val),
                    "strength": "Strong" if abs(corr_val) >= 0.8 else "Moderate"
                })
    return strong_corr


def analyze_parameter_relationships(df):
    """Analyze relationships between operational parameters"""
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    relationships = {}
    
    # Analyze parameter ratios and derived metrics
    relationships["parameter_ratios"] = {
        "flowrate_to_pressure": float(df["Flowrate"].mean() / df["Pressure"].mean()),
        "temperature_to_pressure": float(df["Temperature"].mean() / df["Pressure"].mean()),
        "flowrate_to_temperature": float(df["Flowrate"].mean() / df["Temperature"].mean())
    }
    
    # Equipment performance zones
    relationships["performance_zones"] = {
        "high_performance": len(df[(df["Flowrate"] > df["Flowrate"].quantile(0.75)) & 
                                  (df["Pressure"] > df["Pressure"].quantile(0.75))]),
        "moderate_performance": len(df[(df["Flowrate"] > df["Flowrate"].quantile(0.25)) & 
                                      (df["Flowrate"] <= df["Flowrate"].quantile(0.75))]),
        "low_performance": len(df[df["Flowrate"] <= df["Flowrate"].quantile(0.25)])
    }
    
    return relationships


def compute_equipment_performance_statistics(df):
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    
    performance_stats = df.groupby('Type')[numeric_cols].agg(['mean', 'std', 'min', 'max']).round(2)
    
    formatted_stats = {}
    for equipment_type in df['Type'].unique():
        formatted_stats[equipment_type] = {}
        for col in numeric_cols:
            formatted_stats[equipment_type][col] = {
                "mean": float(performance_stats.loc[equipment_type, (col, 'mean')]),
                "std": float(performance_stats.loc[equipment_type, (col, 'std')]),
                "min": float(performance_stats.loc[equipment_type, (col, 'min')]),
                "max": float(performance_stats.loc[equipment_type, (col, 'max')])
            }
    
    return formatted_stats
