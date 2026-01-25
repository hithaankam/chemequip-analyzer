import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def normalize_data(df):
    """Enhanced data normalization with multiple scaling methods"""
    numeric_cols = ["Flowrate", "Pressure", "Temperature"]
    df_norm = df.copy()

    # Min-Max normalization
    scaler = MinMaxScaler()
    normalized_values = scaler.fit_transform(df[numeric_cols])
    
    for i, col in enumerate(numeric_cols):
        df_norm[f"{col}_norm"] = normalized_values[:, i]
        
        # Additional normalization methods
        df_norm[f"{col}_zscore"] = (df[col] - df[col].mean()) / df[col].std()
        df_norm[f"{col}_robust"] = (df[col] - df[col].median()) / (df[col].quantile(0.75) - df[col].quantile(0.25))

    return df_norm


def compute_efficiency_scores(df):
    """Comprehensive efficiency scoring system matching EDA analysis"""
    df_efficiency = normalize_data(df)

    # Multiple efficiency calculation methods
    
    # Method 1: Weighted composite score (from EDA)
    temp_efficiency = 1 - abs(df_efficiency["Temperature_norm"] - 0.7)  # Optimal around 70% of max temp
    df_efficiency["Efficiency_Score"] = (
        df_efficiency["Flowrate_norm"] * 0.4
        + df_efficiency["Pressure_norm"] * 0.3
        + temp_efficiency * 0.3
    )
    
    # Method 2: Performance index based on operational zones
    df_efficiency["Performance_Index"] = calculate_performance_index(df_efficiency)
    
    # Method 3: Equipment-specific efficiency
    df_efficiency["Equipment_Efficiency"] = calculate_equipment_specific_efficiency(df_efficiency)
    
    # Method 4: Operational effectiveness score
    df_efficiency["Operational_Score"] = calculate_operational_score(df_efficiency)

    return df_efficiency


def calculate_performance_index(df_efficiency):
    """Calculate performance index based on operational parameters"""
    # High flowrate and pressure are generally good, moderate temperature is optimal
    flowrate_score = df_efficiency["Flowrate_norm"]
    pressure_score = df_efficiency["Pressure_norm"]
    
    # Temperature scoring: penalize very high and very low temperatures
    temp_score = 1 - abs(df_efficiency["Temperature_norm"] - 0.6)  # Optimal at 60% of range
    temp_score = np.maximum(temp_score, 0)  # Ensure non-negative
    
    performance_index = (flowrate_score * 0.35 + pressure_score * 0.35 + temp_score * 0.3)
    return performance_index


def calculate_equipment_specific_efficiency(df_efficiency):
    """Calculate efficiency specific to equipment type"""
    efficiency_scores = []
    
    for _, row in df_efficiency.iterrows():
        equipment_type = row["Type"]
        
        # Type-specific efficiency calculations
        if equipment_type == "Pump":
            # For pumps: high flowrate and moderate pressure are optimal
            score = row["Flowrate_norm"] * 0.5 + row["Pressure_norm"] * 0.3 + (1 - abs(row["Temperature_norm"] - 0.5)) * 0.2
        elif equipment_type == "Compressor":
            # For compressors: high pressure is key, moderate temperature
            score = row["Pressure_norm"] * 0.5 + row["Flowrate_norm"] * 0.3 + (1 - abs(row["Temperature_norm"] - 0.4)) * 0.2
        elif equipment_type == "HeatExchanger":
            # For heat exchangers: high temperature and flowrate are important
            score = row["Temperature_norm"] * 0.4 + row["Flowrate_norm"] * 0.4 + row["Pressure_norm"] * 0.2
        elif equipment_type == "Reactor":
            # For reactors: high temperature and pressure, moderate flowrate
            score = row["Temperature_norm"] * 0.4 + row["Pressure_norm"] * 0.4 + row["Flowrate_norm"] * 0.2
        elif equipment_type == "Condenser":
            # For condensers: high flowrate, moderate temperature
            score = row["Flowrate_norm"] * 0.5 + (1 - abs(row["Temperature_norm"] - 0.6)) * 0.3 + row["Pressure_norm"] * 0.2
        elif equipment_type == "Valve":
            # For valves: moderate pressure and flowrate
            score = (1 - abs(row["Pressure_norm"] - 0.5)) * 0.4 + row["Flowrate_norm"] * 0.4 + (1 - abs(row["Temperature_norm"] - 0.5)) * 0.2
        else:
            # Default scoring
            score = row["Flowrate_norm"] * 0.4 + row["Pressure_norm"] * 0.3 + (1 - abs(row["Temperature_norm"] - 0.6)) * 0.3
        
        efficiency_scores.append(max(0, min(1, score)))  # Clamp between 0 and 1
    
    return pd.Series(efficiency_scores, index=df_efficiency.index)


def calculate_operational_score(df_efficiency):
    """Calculate operational effectiveness score"""
    # Based on how well equipment operates within expected ranges
    flowrate_effectiveness = 1 - abs(df_efficiency["Flowrate_norm"] - 0.75)  # Target 75% of max
    pressure_effectiveness = 1 - abs(df_efficiency["Pressure_norm"] - 0.65)   # Target 65% of max
    temp_effectiveness = 1 - abs(df_efficiency["Temperature_norm"] - 0.7)     # Target 70% of max
    
    # Ensure non-negative scores
    flowrate_effectiveness = np.maximum(flowrate_effectiveness, 0)
    pressure_effectiveness = np.maximum(pressure_effectiveness, 0)
    temp_effectiveness = np.maximum(temp_effectiveness, 0)
    
    operational_score = (flowrate_effectiveness * 0.4 + pressure_effectiveness * 0.3 + temp_effectiveness * 0.3)
    return operational_score


def rank_equipment_by_efficiency(df):
    """Enhanced equipment ranking with multiple efficiency metrics"""
    df_efficiency = compute_efficiency_scores(df)
    
    # Create comprehensive rankings
    rankings = {
        "overall_efficiency": [],
        "performance_index": [],
        "equipment_specific": [],
        "operational_score": [],
        "top_performers_by_type": {},
        "efficiency_statistics": {}
    }
    
    # Overall efficiency ranking
    df_ranked = df_efficiency.sort_values("Efficiency_Score", ascending=False)
    for _, row in df_ranked.iterrows():
        rankings["overall_efficiency"].append({
            "equipment_name": str(row["Equipment Name"]),
            "type": str(row["Type"]),
            "flowrate": float(row["Flowrate"]),
            "pressure": float(row["Pressure"]),
            "temperature": float(row["Temperature"]),
            "efficiency_score": float(row["Efficiency_Score"]),
            "performance_index": float(row["Performance_Index"]),
            "equipment_efficiency": float(row["Equipment_Efficiency"]),
            "operational_score": float(row["Operational_Score"]),
            "rank": int(df_ranked.index.get_loc(row.name) + 1)
        })
    
    # Performance index ranking
    df_perf_ranked = df_efficiency.sort_values("Performance_Index", ascending=False)
    for _, row in df_perf_ranked.iterrows():
        rankings["performance_index"].append({
            "equipment_name": str(row["Equipment Name"]),
            "type": str(row["Type"]),
            "performance_index": float(row["Performance_Index"]),
            "rank": int(df_perf_ranked.index.get_loc(row.name) + 1)
        })
    
    # Equipment-specific efficiency ranking
    df_equip_ranked = df_efficiency.sort_values("Equipment_Efficiency", ascending=False)
    for _, row in df_equip_ranked.iterrows():
        rankings["equipment_specific"].append({
            "equipment_name": str(row["Equipment Name"]),
            "type": str(row["Type"]),
            "equipment_efficiency": float(row["Equipment_Efficiency"]),
            "rank": int(df_equip_ranked.index.get_loc(row.name) + 1)
        })
    
    # Top performers by equipment type
    for equipment_type in df["Type"].unique():
        type_subset = df_efficiency[df_efficiency["Type"] == equipment_type].sort_values("Efficiency_Score", ascending=False)
        rankings["top_performers_by_type"][equipment_type] = []
        
        for _, row in type_subset.iterrows():
            rankings["top_performers_by_type"][equipment_type].append({
                "equipment_name": str(row["Equipment Name"]),
                "efficiency_score": float(row["Efficiency_Score"]),
                "performance_index": float(row["Performance_Index"]),
                "equipment_efficiency": float(row["Equipment_Efficiency"]),
                "operational_score": float(row["Operational_Score"]),
                "rank_in_type": int(type_subset.index.get_loc(row.name) + 1)
            })
    
    # Efficiency statistics
    rankings["efficiency_statistics"] = {
        "overall_efficiency": {
            "mean": float(df_efficiency["Efficiency_Score"].mean()),
            "std": float(df_efficiency["Efficiency_Score"].std()),
            "min": float(df_efficiency["Efficiency_Score"].min()),
            "max": float(df_efficiency["Efficiency_Score"].max()),
            "median": float(df_efficiency["Efficiency_Score"].median())
        },
        "performance_index": {
            "mean": float(df_efficiency["Performance_Index"].mean()),
            "std": float(df_efficiency["Performance_Index"].std()),
            "min": float(df_efficiency["Performance_Index"].min()),
            "max": float(df_efficiency["Performance_Index"].max()),
            "median": float(df_efficiency["Performance_Index"].median())
        }
    }

    return rankings


def compute_efficiency_by_type(df):
    """Comprehensive efficiency analysis by equipment type matching EDA depth"""
    df_efficiency = compute_efficiency_scores(df)
    type_efficiency = {}

    for equipment_type in df["Type"].unique():
        subset = df_efficiency[df_efficiency["Type"] == equipment_type]
        
        type_efficiency[equipment_type] = {
            "count": int(len(subset)),
            "efficiency_metrics": {
                "overall_efficiency": {
                    "mean": float(subset["Efficiency_Score"].mean()),
                    "std": float(subset["Efficiency_Score"].std()),
                    "min": float(subset["Efficiency_Score"].min()),
                    "max": float(subset["Efficiency_Score"].max()),
                    "median": float(subset["Efficiency_Score"].median()),
                    "range": float(subset["Efficiency_Score"].max() - subset["Efficiency_Score"].min())
                },
                "performance_index": {
                    "mean": float(subset["Performance_Index"].mean()),
                    "std": float(subset["Performance_Index"].std()),
                    "min": float(subset["Performance_Index"].min()),
                    "max": float(subset["Performance_Index"].max()),
                    "median": float(subset["Performance_Index"].median())
                },
                "equipment_specific": {
                    "mean": float(subset["Equipment_Efficiency"].mean()),
                    "std": float(subset["Equipment_Efficiency"].std()),
                    "min": float(subset["Equipment_Efficiency"].min()),
                    "max": float(subset["Equipment_Efficiency"].max()),
                    "median": float(subset["Equipment_Efficiency"].median())
                },
                "operational_score": {
                    "mean": float(subset["Operational_Score"].mean()),
                    "std": float(subset["Operational_Score"].std()),
                    "min": float(subset["Operational_Score"].min()),
                    "max": float(subset["Operational_Score"].max()),
                    "median": float(subset["Operational_Score"].median())
                }
            },
            "top_performer": get_enhanced_top_performer_for_type(subset),
            "performance_distribution": analyze_type_performance_distribution(subset),
            "operational_characteristics": analyze_type_operational_characteristics(subset, df),
            "efficiency_ranking": get_type_efficiency_ranking(equipment_type, df_efficiency)
        }

    return type_efficiency


def get_enhanced_top_performer_for_type(subset):
    """Get comprehensive top performer analysis for equipment type"""
    if len(subset) == 0:
        return None
    
    top_performer = subset.loc[subset["Efficiency_Score"].idxmax()]
    return {
        "equipment_name": str(top_performer["Equipment Name"]),
        "efficiency_score": float(top_performer["Efficiency_Score"]),
        "performance_index": float(top_performer["Performance_Index"]),
        "equipment_efficiency": float(top_performer["Equipment_Efficiency"]),
        "operational_score": float(top_performer["Operational_Score"]),
        "flowrate": float(top_performer["Flowrate"]),
        "pressure": float(top_performer["Pressure"]),
        "temperature": float(top_performer["Temperature"]),
        "normalized_scores": {
            "flowrate_norm": float(top_performer["Flowrate_norm"]),
            "pressure_norm": float(top_performer["Pressure_norm"]),
            "temperature_norm": float(top_performer["Temperature_norm"])
        }
    }


def analyze_type_performance_distribution(subset):
    """Analyze performance distribution within equipment type"""
    efficiency_scores = subset["Efficiency_Score"]
    
    return {
        "quartiles": {
            "q1": float(efficiency_scores.quantile(0.25)),
            "q2": float(efficiency_scores.quantile(0.5)),
            "q3": float(efficiency_scores.quantile(0.75))
        },
        "performance_categories": {
            "high_performers": int(len(efficiency_scores[efficiency_scores >= efficiency_scores.quantile(0.75)])),
            "medium_performers": int(len(efficiency_scores[(efficiency_scores >= efficiency_scores.quantile(0.25)) & 
                                                          (efficiency_scores < efficiency_scores.quantile(0.75))])),
            "low_performers": int(len(efficiency_scores[efficiency_scores < efficiency_scores.quantile(0.25)]))
        },
        "coefficient_of_variation": float(efficiency_scores.std() / efficiency_scores.mean()) if efficiency_scores.mean() != 0 else 0.0,
        "skewness": float(efficiency_scores.skew()),
        "kurtosis": float(efficiency_scores.kurtosis())
    }


def analyze_type_operational_characteristics(subset, full_df):
    """Analyze operational characteristics of equipment type"""
    return {
        "average_operational_parameters": {
            "flowrate": float(subset["Flowrate"].mean()),
            "pressure": float(subset["Pressure"].mean()),
            "temperature": float(subset["Temperature"].mean())
        },
        "relative_to_overall": {
            "flowrate_ratio": float(subset["Flowrate"].mean() / full_df["Flowrate"].mean()),
            "pressure_ratio": float(subset["Pressure"].mean() / full_df["Pressure"].mean()),
            "temperature_ratio": float(subset["Temperature"].mean() / full_df["Temperature"].mean())
        },
        "operational_ranges": {
            "flowrate_range": float(subset["Flowrate"].max() - subset["Flowrate"].min()),
            "pressure_range": float(subset["Pressure"].max() - subset["Pressure"].min()),
            "temperature_range": float(subset["Temperature"].max() - subset["Temperature"].min())
        },
        "consistency_metrics": {
            "flowrate_cv": float(subset["Flowrate"].std() / subset["Flowrate"].mean()) if subset["Flowrate"].mean() != 0 else 0.0,
            "pressure_cv": float(subset["Pressure"].std() / subset["Pressure"].mean()) if subset["Pressure"].mean() != 0 else 0.0,
            "temperature_cv": float(subset["Temperature"].std() / subset["Temperature"].mean()) if subset["Temperature"].mean() != 0 else 0.0
        }
    }


def get_type_efficiency_ranking(equipment_type, df_efficiency):
    """Get efficiency ranking of equipment type relative to others"""
    type_means = df_efficiency.groupby("Type")["Efficiency_Score"].mean().sort_values(ascending=False)
    ranking = list(type_means.index).index(equipment_type) + 1
    
    return {
        "rank": int(ranking),
        "total_types": int(len(type_means)),
        "percentile": float((len(type_means) - ranking + 1) / len(type_means) * 100),
        "efficiency_score": float(type_means[equipment_type])
    }


def analyze_efficiency_distribution(df):
    df_efficiency = compute_efficiency_scores(df)
    
    efficiency_scores = df_efficiency["Efficiency_Score"]
    
    distribution_analysis = {
        "quartiles": {
            "q1": float(efficiency_scores.quantile(0.25)),
            "q2": float(efficiency_scores.quantile(0.5)),
            "q3": float(efficiency_scores.quantile(0.75))
        },
        "performance_categories": {
            "high_performers": len(efficiency_scores[efficiency_scores >= efficiency_scores.quantile(0.75)]),
            "medium_performers": len(efficiency_scores[(efficiency_scores >= efficiency_scores.quantile(0.25)) & (efficiency_scores < efficiency_scores.quantile(0.75))]),
            "low_performers": len(efficiency_scores[efficiency_scores < efficiency_scores.quantile(0.25)])
        },
        "statistics": {
            "mean": float(efficiency_scores.mean()),
            "std": float(efficiency_scores.std()),
            "min": float(efficiency_scores.min()),
            "max": float(efficiency_scores.max()),
            "range": float(efficiency_scores.max() - efficiency_scores.min())
        }
    }
    
    return distribution_analysis


def compute_composite_performance_metrics(df):
    df_efficiency = compute_efficiency_scores(df)
    
    rankings = rank_equipment_by_efficiency(df)
    
    composite_metrics = {
        "overall_performance_index": float(df_efficiency["Efficiency_Score"].mean()),
        "performance_variance": float(df_efficiency["Efficiency_Score"].var()),
        "equipment_rankings": rankings["overall_efficiency"][:10] if "overall_efficiency" in rankings else [],
        "type_performance": compute_efficiency_by_type(df),
        "distribution_analysis": analyze_efficiency_distribution(df)
    }
    
    return composite_metrics
