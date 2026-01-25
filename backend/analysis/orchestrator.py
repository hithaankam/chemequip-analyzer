from . import data_loader
from . import metrics
from . import insights
from . import outliers
from . import efficiency
import json
import numpy as np


def convert_to_json_serializable(obj):
    """Convert numpy types and other non-serializable types to JSON-serializable types"""
    if isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return list(convert_to_json_serializable(list(obj)))
    elif isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        # Handle NaN and infinity values
        if np.isnan(obj):
            return None
        elif np.isinf(obj):
            return None
        else:
            return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif hasattr(obj, 'item'):  # numpy scalar
        item_val = obj.item()
        # Check if the item is NaN or infinity
        if isinstance(item_val, float) and (np.isnan(item_val) or np.isinf(item_val)):
            return None
        return item_val
    elif hasattr(obj, 'tolist'):  # pandas series or similar
        return convert_to_json_serializable(obj.tolist())
    elif str(type(obj)).startswith('<class \'pandas.'):
        # Handle pandas objects
        if hasattr(obj, 'to_dict'):
            return convert_to_json_serializable(obj.to_dict())
        elif hasattr(obj, 'tolist'):
            return convert_to_json_serializable(obj.tolist())
        else:
            return str(obj)
    elif obj is None or isinstance(obj, (str, int, bool)):
        return obj
    elif isinstance(obj, float):
        # Handle regular Python float NaN and infinity
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    else:
        # Fallback: convert to string
        return str(obj)


def analyze_equipment_data(file_obj):
    df_clean = data_loader.load_and_clean_data(file_obj)

    basic_metrics = metrics.compute_basic_metrics(df_clean)
    type_metrics = metrics.compute_type_metrics(df_clean)
    advanced_statistics = metrics.compute_advanced_statistics(df_clean)
    performance_statistics = metrics.compute_equipment_performance_statistics(df_clean)

    type_distribution = insights.get_equipment_type_distribution(df_clean)
    grouped_averages = insights.get_grouped_averages(df_clean)
    correlations = insights.compute_correlation_matrix(df_clean)
    high_temp_equipment = insights.detect_high_temperature_equipment(df_clean)
    top_performers = insights.get_top_performers(df_clean)

    outlier_analysis = outliers.detect_outliers_iqr(df_clean)
    comprehensive_outliers = outliers.comprehensive_outlier_analysis(df_clean)
    outlier_patterns = outliers.analyze_outlier_patterns(df_clean)

    efficiency_rankings = efficiency.rank_equipment_by_efficiency(df_clean)
    efficiency_by_type = efficiency.compute_efficiency_by_type(df_clean)
    composite_performance = efficiency.compute_composite_performance_metrics(df_clean)

    comprehensive_insights = insights.generate_comprehensive_insights(
        df_clean, efficiency_rankings, correlations
    )

    result = {
        "dataset_info": {
            "cleaned_size": len(df_clean),
            "original_columns": list(df_clean.columns),
            "equipment_types": list(df_clean["Type"].unique()),
            "data_quality": {
                "missing_values": df_clean.isnull().sum().to_dict(),
                "duplicate_rows": int(df_clean.duplicated().sum()),
                "data_completeness": float((df_clean.count().sum() / (len(df_clean) * len(df_clean.columns))) * 100)
            }
        },
        "summary_metrics": basic_metrics,
        "type_metrics": type_metrics,
        "advanced_statistics": advanced_statistics,
        "performance_statistics": performance_statistics,
        "distributions": {
            "equipment_types": type_distribution,
            "grouped_averages": grouped_averages,
        },
        "correlations": correlations,
        "high_temperature_analysis": high_temp_equipment,
        "top_performers": top_performers,
        "outliers": {
            "basic_analysis": outlier_analysis,
            "comprehensive_analysis": comprehensive_outliers,
            "patterns": outlier_patterns
        },
        "efficiency": {
            "rankings": efficiency_rankings,
            "by_type": efficiency_by_type,
            "composite_performance": composite_performance
        },
        "comprehensive_insights": comprehensive_insights,
        "analysis_metadata": {
            "analysis_version": "2.0",
            "analysis_date": "2025-01-25",
            "features_analyzed": [
                "Basic Statistics",
                "Advanced Statistics", 
                "Correlation Analysis",
                "Outlier Detection (IQR & Z-Score)",
                "Efficiency Scoring",
                "Performance Ranking",
                "Equipment Type Analysis",
                "High-Performance Analysis",
                "Comprehensive Insights"
            ]
        }
    }
    
    # Convert all data to JSON-serializable format
    return convert_to_json_serializable(result)
