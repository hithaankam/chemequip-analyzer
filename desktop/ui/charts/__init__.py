"""
Charts package for desktop application
Contains all chart components matching React frontend functionality
"""

from .overview_charts import OverviewCharts
from .statistics_charts import StatisticsCharts
from .efficiency_charts import EfficiencyCharts
from .correlation_charts import CorrelationCharts
from .outlier_charts import OutlierCharts
from .insights_panel import InsightsPanel

__all__ = [
    'OverviewCharts',
    'StatisticsCharts', 
    'EfficiencyCharts',
    'CorrelationCharts',
    'OutlierCharts',
    'InsightsPanel'
]