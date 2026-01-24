from . import data_loader
from . import metrics
from . import insights
from . import outliers
from . import efficiency

def analyze_equipment_data(file_obj):
    df_clean = data_loader.load_and_clean_data(file_obj)
    
    basic_metrics = metrics.compute_basic_metrics(df_clean)
    type_metrics = metrics.compute_type_metrics(df_clean)
    
    type_distribution = insights.get_equipment_type_distribution(df_clean)
    grouped_averages = insights.get_grouped_averages(df_clean)
    correlations = insights.compute_correlation_matrix(df_clean)
    high_temp_equipment = insights.detect_high_temperature_equipment(df_clean)
    top_performers = insights.get_top_performers(df_clean)
    
    outlier_analysis = outliers.detect_outliers_iqr(df_clean)
    
    efficiency_rankings = efficiency.rank_equipment_by_efficiency(df_clean)
    efficiency_by_type = efficiency.compute_efficiency_by_type(df_clean)
    
    return {
        'dataset_info': {
            'cleaned_size': len(df_clean),
            'original_columns': list(df_clean.columns)
        },
        'summary_metrics': basic_metrics,
        'type_metrics': type_metrics,
        'distributions': {
            'equipment_types': type_distribution,
            'grouped_averages': grouped_averages
        },
        'correlations': correlations,
        'high_temperature_analysis': high_temp_equipment,
        'top_performers': top_performers,
        'outliers': outlier_analysis,
        'efficiency': {
            'rankings': efficiency_rankings,
            'by_type': efficiency_by_type
        }
    }