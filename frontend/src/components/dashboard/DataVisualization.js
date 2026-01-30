import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
  ScatterController,
  LinearScale as LinearScaleScatter,
} from 'chart.js';
import { Bar, Pie, Line, Scatter, Doughnut } from 'react-chartjs-2';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
  ScatterController,
  LinearScaleScatter
);

// Correlation Heatmap Component
const CorrelationHeatmap = ({ correlations }) => {
  const parameters = ['Flowrate', 'Pressure', 'Temperature'];
  
  // Create correlation matrix
  const correlationMatrix = [
    [1.0, correlations.flowrate_pressure || 0, correlations.flowrate_temperature || 0],
    [correlations.flowrate_pressure || 0, 1.0, correlations.pressure_temperature || 0],
    [correlations.flowrate_temperature || 0, correlations.pressure_temperature || 0, 1.0]
  ];

  // Get color based on correlation value
  const getColor = (value) => {
    // Use RdBu_r colormap (Red-Blue reversed) like matplotlib
    // Positive correlations: red shades, Negative correlations: blue shades
    const intensity = Math.abs(value);
    
    if (value > 0.75) return '#8B0000'; // Dark red
    else if (value > 0.5) return '#DC143C'; // Crimson
    else if (value > 0.25) return '#FF6347'; // Tomato
    else if (value > 0) return '#FFA07A'; // Light salmon
    else if (value === 0) return '#F5F5F5'; // Very light gray
    else if (value > -0.25) return '#87CEEB'; // Sky blue
    else if (value > -0.5) return '#4682B4'; // Steel blue
    else if (value > -0.75) return '#1E90FF'; // Dodger blue
    else return '#000080'; // Navy blue
  };

  // Get text color for readability
  const getTextColor = (value) => {
    return Math.abs(value) > 0.5 ? 'white' : 'black';
  };

  return (
    <div className="correlation-heatmap">
      <div className="heatmap-grid">
        {/* Header row */}
        <div className="heatmap-cell header"></div>
        {parameters.map(param => (
          <div key={param} className="heatmap-cell header">{param}</div>
        ))}
        
        {/* Data rows */}
        {parameters.map((rowParam, i) => (
          <React.Fragment key={rowParam}>
            <div className="heatmap-cell header">{rowParam}</div>
            {parameters.map((colParam, j) => (
              <div 
                key={`${i}-${j}`}
                className="heatmap-cell data"
                style={{
                  backgroundColor: getColor(correlationMatrix[i][j]),
                  color: getTextColor(correlationMatrix[i][j])
                }}
              >
                {correlationMatrix[i][j].toFixed(3)}
              </div>
            ))}
          </React.Fragment>
        ))}
      </div>
      
      {/* Legend */}
      <div className="heatmap-legend">
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#000080'}}></div>
          <span>-1.0</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#4682B4'}}></div>
          <span>-0.5</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#F5F5F5', border: '1px solid #ccc'}}></div>
          <span>0.0</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#FF6347'}}></div>
          <span>+0.5</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#8B0000'}}></div>
          <span>+1.0</span>
        </div>
      </div>
    </div>
  );
};

const DataVisualization = ({ analysisData }) => {
  const [activeTab, setActiveTab] = useState('overview');

  // Debug logging
  console.log('DataVisualization received analysisData:', analysisData);
  console.log('analysisData type:', typeof analysisData);
  console.log('analysisData keys:', analysisData ? Object.keys(analysisData) : 'null');

  if (!analysisData || !analysisData.analysis_results) {
    console.log('DataVisualization: No analysis data or analysis_results');
    return null;
  }

  const { 
    summary_metrics, 
    distributions, 
    efficiency, 
    correlations,
    outliers,
    comprehensive_insights,
    advanced_statistics,
    high_temperature_analysis,
    type_metrics,
    performance_statistics
  } = analysisData.analysis_results;

  // Debug logging for data structure
  console.log('Extracted data:');
  console.log('- summary_metrics:', summary_metrics);
  console.log('- distributions:', distributions);
  console.log('- efficiency:', efficiency);
  console.log('- type_metrics:', type_metrics);

  if (!summary_metrics || !distributions || !efficiency) {
    console.log('DataVisualization: Missing required data sections');
    console.log('- summary_metrics exists:', !!summary_metrics);
    console.log('- distributions exists:', !!distributions);
    console.log('- efficiency exists:', !!efficiency);
    return <div className="loading">Loading analysis data...</div>;
  }

  const equipmentTypes = distributions.equipment_types || {};
  const overallStats = summary_metrics.overall_stats || {};
  const statisticalSummary = summary_metrics.statistical_summary || {};
  const efficiencyRankings = efficiency.rankings?.overall_efficiency || [];
  const keyCorrelations = correlations?.key_correlations || {};
  const outlierData = outliers?.basic_analysis || {};
  const insights = comprehensive_insights || {};
  const advancedStats = advanced_statistics || {};
  const typeMetrics = type_metrics || {};

  // Debug logging for chart data preparation
  console.log('Chart data preparation:');
  console.log('- equipmentTypes:', equipmentTypes);
  console.log('- overallStats:', overallStats);
  console.log('- efficiencyRankings length:', efficiencyRankings.length);
  console.log('- keyCorrelations:', keyCorrelations);

  // Validate that we have minimum required data for charts
  const hasEquipmentTypes = equipmentTypes && Object.keys(equipmentTypes).length > 0;
  const hasOverallStats = overallStats && Object.keys(overallStats).length > 0;
  const hasEfficiencyData = efficiencyRankings && efficiencyRankings.length > 0;
  const hasCorrelationData = keyCorrelations && Object.keys(keyCorrelations).length > 0;

  console.log('Data validation:');
  console.log('- hasEquipmentTypes:', hasEquipmentTypes);
  console.log('- hasOverallStats:', hasOverallStats);
  console.log('- hasEfficiencyData:', hasEfficiencyData);
  console.log('- hasCorrelationData:', hasCorrelationData);

  if (!hasEquipmentTypes && !hasOverallStats && !hasEfficiencyData) {
    return (
      <div className="visualization-container">
        <h3>Analysis Results</h3>
        <div className="loading">
          No chart data available. Please check that your dataset contains valid equipment data.
        </div>
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
          <h4>Debug Information:</h4>
          <pre>{JSON.stringify({ equipmentTypes, overallStats, efficiencyRankings: efficiencyRankings.slice(0, 3) }, null, 2)}</pre>
        </div>
      </div>
    );
  }

  // Equipment Type Distribution (matching notebook bar chart)
  const equipmentTypeBarData = {
    labels: Object.keys(equipmentTypes),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(equipmentTypes),
        backgroundColor: 'rgba(135, 206, 235, 0.8)',
        borderColor: 'rgba(0, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Debug logging for chart data
  console.log('Equipment Type Bar Data:', equipmentTypeBarData);
  console.log('Labels:', equipmentTypeBarData.labels);
  console.log('Data:', equipmentTypeBarData.datasets[0].data);

  // Statistical Summary Data (matching notebook describe() output)
  // Ensure we have valid statistical data
  const validStatisticalSummary = {
    Flowrate: statisticalSummary.Flowrate || {},
    Pressure: statisticalSummary.Pressure || {},
    Temperature: statisticalSummary.Temperature || {}
  };

  const statisticalData = {
    labels: ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'],
    datasets: [
      {
        label: 'Flowrate',
        data: [
          parseFloat(validStatisticalSummary.Flowrate.count || 0),
          parseFloat(validStatisticalSummary.Flowrate.mean || 0),
          parseFloat(validStatisticalSummary.Flowrate.std || 0),
          parseFloat(validStatisticalSummary.Flowrate.min || 0),
          parseFloat(validStatisticalSummary.Flowrate['25%'] || 0),
          parseFloat(validStatisticalSummary.Flowrate['50%'] || 0),
          parseFloat(validStatisticalSummary.Flowrate['75%'] || 0),
          parseFloat(validStatisticalSummary.Flowrate.max || 0),
        ],
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Pressure',
        data: [
          parseFloat(validStatisticalSummary.Pressure.count || 0),
          parseFloat(validStatisticalSummary.Pressure.mean || 0),
          parseFloat(validStatisticalSummary.Pressure.std || 0),
          parseFloat(validStatisticalSummary.Pressure.min || 0),
          parseFloat(validStatisticalSummary.Pressure['25%'] || 0),
          parseFloat(validStatisticalSummary.Pressure['50%'] || 0),
          parseFloat(validStatisticalSummary.Pressure['75%'] || 0),
          parseFloat(validStatisticalSummary.Pressure.max || 0),
        ],
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Temperature',
        data: [
          parseFloat(validStatisticalSummary.Temperature.count || 0),
          parseFloat(validStatisticalSummary.Temperature.mean || 0),
          parseFloat(validStatisticalSummary.Temperature.std || 0),
          parseFloat(validStatisticalSummary.Temperature.min || 0),
          parseFloat(validStatisticalSummary.Temperature['25%'] || 0),
          parseFloat(validStatisticalSummary.Temperature['50%'] || 0),
          parseFloat(validStatisticalSummary.Temperature['75%'] || 0),
          parseFloat(validStatisticalSummary.Temperature.max || 0),
        ],
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Debug logging for statistical data
  console.log('Statistical Data:', statisticalData);
  console.log('Valid statistical summary:', validStatisticalSummary);

  // Box Plot Data (simulated using quartiles)
  const boxPlotData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Q1',
        data: [
          overallStats.Flowrate?.q25 || 0,
          overallStats.Pressure?.q25 || 0,
          overallStats.Temperature?.q25 || 0,
        ],
        backgroundColor: 'rgba(173, 216, 230, 0.8)',
      },
      {
        label: 'Median',
        data: [
          overallStats.Flowrate?.median || 0,
          overallStats.Pressure?.median || 0,
          overallStats.Temperature?.median || 0,
        ],
        backgroundColor: 'rgba(144, 238, 144, 0.8)',
      },
      {
        label: 'Q3',
        data: [
          overallStats.Flowrate?.q75 || 0,
          overallStats.Pressure?.q75 || 0,
          overallStats.Temperature?.q75 || 0,
        ],
        backgroundColor: 'rgba(240, 128, 128, 0.8)',
      },
    ],
  };

  // Equipment Type Performance (matching notebook grouped analysis)
  const validTypeMetrics = Object.keys(typeMetrics).filter(type => 
    typeMetrics[type] && typeMetrics[type].metrics
  );

  const typePerformanceData = {
    labels: validTypeMetrics,
    datasets: [
      {
        label: 'Avg Flowrate',
        data: validTypeMetrics.map(type => 
          parseFloat(typeMetrics[type].metrics?.Flowrate?.mean || 0)
        ),
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
        yAxisID: 'y',
      },
      {
        label: 'Avg Pressure',
        data: validTypeMetrics.map(type => 
          parseFloat(typeMetrics[type].metrics?.Pressure?.mean || 0)
        ),
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
        yAxisID: 'y1',
      },
      {
        label: 'Avg Temperature',
        data: validTypeMetrics.map(type => 
          parseFloat(typeMetrics[type].metrics?.Temperature?.mean || 0)
        ),
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
        yAxisID: 'y2',
      },
    ],
  };

  // Debug logging for type performance data
  console.log('Type Performance Data:', typePerformanceData);
  console.log('Valid type metrics:', validTypeMetrics);

  // Advanced Statistics Visualization
  const varianceAnalysisData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Variance',
        data: [
          advancedStats.variance_analysis?.Flowrate?.variance || 0,
          advancedStats.variance_analysis?.Pressure?.variance || 0,
          advancedStats.variance_analysis?.Temperature?.variance || 0,
        ],
        backgroundColor: 'rgba(153, 102, 255, 0.8)',
      },
      {
        label: 'Coefficient of Variation',
        data: [
          advancedStats.variance_analysis?.Flowrate?.coefficient_of_variation || 0,
          advancedStats.variance_analysis?.Pressure?.coefficient_of_variation || 0,
          advancedStats.variance_analysis?.Temperature?.coefficient_of_variation || 0,
        ],
        backgroundColor: 'rgba(255, 159, 64, 0.8)',
      },
    ],
  };

  // Distribution Analysis (Skewness and Kurtosis)
  const distributionAnalysisData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Skewness',
        data: [
          advancedStats.distribution_analysis?.Flowrate?.skewness || 0,
          advancedStats.distribution_analysis?.Pressure?.skewness || 0,
          advancedStats.distribution_analysis?.Temperature?.skewness || 0,
        ],
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
      },
      {
        label: 'Kurtosis',
        data: [
          advancedStats.distribution_analysis?.Flowrate?.kurtosis || 0,
          advancedStats.distribution_analysis?.Pressure?.kurtosis || 0,
          advancedStats.distribution_analysis?.Temperature?.kurtosis || 0,
        ],
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
      },
    ],
  };

  const metricsData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Mean Values',
        data: [
          overallStats.Flowrate?.mean || 0,
          overallStats.Pressure?.mean || 0,
          overallStats.Temperature?.mean || 0,
        ],
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Standard Deviation',
        data: [
          overallStats.Flowrate?.std || 0,
          overallStats.Pressure?.std || 0,
          overallStats.Temperature?.std || 0,
        ],
        backgroundColor: 'rgba(255, 99, 132, 0.8)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Efficiency Rankings - ensure we have valid data
  const validEfficiencyRankings = efficiencyRankings.filter(item => 
    item && item.equipment_name && typeof item.efficiency_score === 'number'
  );

  const efficiencyData = {
    labels: validEfficiencyRankings.slice(0, 10).map(item => item.equipment_name || 'Unknown'),
    datasets: [
      {
        label: 'Efficiency Score',
        data: validEfficiencyRankings.slice(0, 10).map(item => 
          parseFloat((item.efficiency_score || 0).toFixed(3))
        ),
        backgroundColor: 'rgba(75, 192, 192, 0.8)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Debug logging for efficiency data
  console.log('Efficiency Data:', efficiencyData);
  console.log('Valid rankings count:', validEfficiencyRankings.length);

  // Correlation data - ensure we have valid numbers
  const validCorrelations = {
    flowrate_temperature: parseFloat(keyCorrelations.flowrate_temperature || 0),
    flowrate_pressure: parseFloat(keyCorrelations.flowrate_pressure || 0),
    pressure_temperature: parseFloat(keyCorrelations.pressure_temperature || 0)
  };

  const correlationData = {
    labels: ['Flowrate-Temperature', 'Flowrate-Pressure', 'Pressure-Temperature'],
    datasets: [
      {
        label: 'Correlation Coefficient',
        data: [
          validCorrelations.flowrate_temperature,
          validCorrelations.flowrate_pressure,
          validCorrelations.pressure_temperature,
        ],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 205, 86, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 205, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Debug logging for correlation data
  console.log('Correlation Data:', correlationData);
  console.log('Valid correlations:', validCorrelations);

  // Correlation interpretation function
  const interpretCorrelation = (correlation) => {
    const absCorr = Math.abs(correlation);
    let strength = '';
    if (absCorr > 0.8) strength = 'Very Strong';
    else if (absCorr > 0.6) strength = 'Strong';
    else if (absCorr > 0.4) strength = 'Moderate';
    else if (absCorr > 0.2) strength = 'Weak';
    else strength = 'Very Weak';
    
    const direction = correlation > 0 ? 'Positive' : 'Negative';
    return `${strength} ${direction}`;
  };

  const outlierSummaryData = {
    labels: Object.keys(outlierData),
    datasets: [
      {
        label: 'Number of Outliers',
        data: Object.values(outlierData).map(data => data.outlier_count || 0),
        backgroundColor: 'rgba(255, 159, 64, 0.8)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  const pieOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
      },
    },
  };

  const correlationOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: false,
        min: -1,
        max: 1,
      },
    },
  };

  const multiAxisOptions = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
      },
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Flowrate',
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Pressure',
        },
        grid: {
          drawOnChartArea: false,
        },
      },
      y2: {
        type: 'linear',
        display: false,
        position: 'right',
      },
    },
  };

  const barChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Equipment Distribution',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  const renderOverview = () => (
    <div>
      {/* Dataset Information Section */}
      <div className="dataset-info">
        <h4>Dataset Information</h4>
        <div className="info-grid">
          <div className="info-item">
            <strong>Dataset Shape:</strong> ({summary_metrics.dataset_overview?.total_equipment || 0}, 5)
          </div>
          <div className="info-item">
            <strong>Columns:</strong> Equipment Name, Type, Flowrate, Pressure, Temperature
          </div>
          <div className="info-item">
            <strong>Missing Values:</strong> {summary_metrics.dataset_overview?.missing_values ? 
              Object.values(summary_metrics.dataset_overview.missing_values).reduce((a, b) => a + b, 0) : 0}
          </div>
          <div className="info-item">
            <strong>Duplicate Rows:</strong> {summary_metrics.dataset_overview?.duplicate_rows || 0}
          </div>
        </div>
      </div>

      {/* Statistical Summary Cards */}
      <div className="stats-summary">
        <div className="stat-card">
          <h4>Total Equipment</h4>
          <span className="stat-value">{summary_metrics.dataset_overview?.total_equipment_count || 0}</span>
        </div>
        <div className="stat-card">
          <h4>Equipment Types</h4>
          <span className="stat-value">{summary_metrics.dataset_overview?.equipment_types_count || 0}</span>
        </div>
        <div className="stat-card">
          <h4>Avg Flowrate</h4>
          <span className="stat-value">{(overallStats.Flowrate?.mean || 0).toFixed(1)}</span>
        </div>
        <div className="stat-card">
          <h4>Avg Temperature</h4>
          <span className="stat-value">{(overallStats.Temperature?.mean || 0).toFixed(1)}</span>
        </div>
      </div>

      {/* Equipment Types Analysis */}
      <div className="charts-grid">
        <div className="chart-container">
          <h4>Equipment Type Distribution (Bar Chart)</h4>
          {hasEquipmentTypes ? (
            <Bar data={equipmentTypeBarData} options={barChartOptions} />
          ) : (
            <div className="no-data">No equipment type data available</div>
          )}
        </div>

        <div className="chart-container">
          <h4>Equipment Type Distribution (Pie Chart)</h4>
          {hasEquipmentTypes ? (
            <Pie data={equipmentTypeBarData} options={pieOptions} />
          ) : (
            <div className="no-data">No equipment type data available</div>
          )}
        </div>
      </div>

      {/* Equipment Type Details */}
      <div className="equipment-types-detail">
        <h4>Equipment Type Details</h4>
        <div className="types-grid">
          {Object.entries(equipmentTypes).map(([type, count]) => (
            <div key={type} className="type-card">
              <h5>{type}</h5>
              <p>Count: {count}</p>
              <p>Percentage: {((count / Object.values(equipmentTypes).reduce((a, b) => a + b, 0)) * 100).toFixed(1)}%</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderStatistics = () => (
    <div>
      {/* Statistical Summary Table */}
      <div className="statistics-section">
        <h4>Statistical Summary (describe() equivalent)</h4>
        <div className="chart-container full-width">
          <Bar data={statisticalData} options={chartOptions} />
        </div>
      </div>

      {/* Box Plot Simulation */}
      <div className="charts-grid">
        <div className="chart-container">
          <h4>Box Plot Analysis (Quartiles)</h4>
          <Bar data={boxPlotData} options={chartOptions} />
        </div>

        <div className="chart-container">
          <h4>Variance Analysis</h4>
          <Bar data={varianceAnalysisData} options={chartOptions} />
        </div>
      </div>

      {/* Distribution Analysis */}
      <div className="charts-grid">
        <div className="chart-container">
          <h4>Distribution Analysis (Skewness & Kurtosis)</h4>
          <Bar data={distributionAnalysisData} options={correlationOptions} />
        </div>

        <div className="chart-container">
          <h4>Equipment Type Performance Comparison</h4>
          <Bar data={typePerformanceData} options={multiAxisOptions} />
        </div>
      </div>

      {/* Detailed Statistics Table */}
      <div className="detailed-stats">
        <h4>Detailed Statistical Analysis</h4>
        <div className="stats-table">
          <table>
            <thead>
              <tr>
                <th>Parameter</th>
                <th>Count</th>
                <th>Mean</th>
                <th>Std</th>
                <th>Min</th>
                <th>25%</th>
                <th>50%</th>
                <th>75%</th>
                <th>Max</th>
              </tr>
            </thead>
            <tbody>
              {['Flowrate', 'Pressure', 'Temperature'].map(param => (
                <tr key={param}>
                  <td><strong>{param}</strong></td>
                  <td>{statisticalSummary[param]?.count?.toFixed(0) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.mean?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.std?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.min?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.['25%']?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.['50%']?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.['75%']?.toFixed(2) || 'N/A'}</td>
                  <td>{statisticalSummary[param]?.max?.toFixed(2) || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Advanced Statistics */}
      {advancedStats.variance_analysis && (
        <div className="advanced-stats">
          <h4>Advanced Statistical Measures</h4>
          <div className="advanced-stats-grid">
            {['Flowrate', 'Pressure', 'Temperature'].map(param => (
              <div key={param} className="advanced-stat-card">
                <h5>{param}</h5>
                <p><strong>Variance:</strong> {advancedStats.variance_analysis[param]?.variance?.toFixed(4) || 'N/A'}</p>
                <p><strong>CV:</strong> {advancedStats.variance_analysis[param]?.coefficient_of_variation?.toFixed(4) || 'N/A'}</p>
                <p><strong>Skewness:</strong> {advancedStats.distribution_analysis?.[param]?.skewness?.toFixed(4) || 'N/A'}</p>
                <p><strong>Kurtosis:</strong> {advancedStats.distribution_analysis?.[param]?.kurtosis?.toFixed(4) || 'N/A'}</p>
                <p><strong>Distribution:</strong> {advancedStats.distribution_analysis?.[param]?.distribution_type || 'N/A'}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
  const renderEfficiency = () => (
    <div>
      {/* Efficiency Rankings */}
      <div className="charts-grid">
        <div className="chart-container full-width">
          <h4>Top 10 Equipment by Efficiency Score</h4>
          <Bar data={efficiencyData} options={chartOptions} />
        </div>
      </div>
      
      {/* Efficiency by Type */}
      <div className="efficiency-by-type">
        <h4>Efficiency Analysis by Equipment Type</h4>
        <div className="efficiency-type-grid">
          {efficiency.by_type && Object.entries(efficiency.by_type).map(([type, stats]) => (
            <div key={type} className="efficiency-type-card">
              <h5>{type}</h5>
              <div className="efficiency-metrics">
                <p><strong>Count:</strong> {stats.count || 0}</p>
                <p><strong>Mean Efficiency:</strong> {(stats.efficiency_metrics?.overall_efficiency?.mean || 0).toFixed(3)}</p>
                <p><strong>Std Dev:</strong> {(stats.efficiency_metrics?.overall_efficiency?.std || 0).toFixed(3)}</p>
                <p><strong>Min:</strong> {(stats.efficiency_metrics?.overall_efficiency?.min || 0).toFixed(3)}</p>
                <p><strong>Max:</strong> {(stats.efficiency_metrics?.overall_efficiency?.max || 0).toFixed(3)}</p>
                {stats.top_performer && (
                  <div className="top-performer">
                    <p><strong>Top Performer:</strong> {stats.top_performer.equipment_name}</p>
                    <p><strong>Score:</strong> {stats.top_performer.efficiency_score?.toFixed(3)}</p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Efficiency Rankings Table */}
      <div className="efficiency-rankings">
        <h4>Complete Efficiency Rankings</h4>
        <div className="rankings-table">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Equipment Name</th>
                <th>Type</th>
                <th>Flowrate</th>
                <th>Pressure</th>
                <th>Temperature</th>
                <th>Efficiency Score</th>
              </tr>
            </thead>
            <tbody>
              {efficiencyRankings.slice(0, 15).map((equipment, index) => (
                <tr key={equipment.equipment_name} className={index < 5 ? 'top-performer' : ''}>
                  <td>{equipment.rank || index + 1}</td>
                  <td>{equipment.equipment_name}</td>
                  <td>{equipment.type}</td>
                  <td>{equipment.flowrate?.toFixed(1)}</td>
                  <td>{equipment.pressure?.toFixed(2)}</td>
                  <td>{equipment.temperature?.toFixed(1)}</td>
                  <td>{equipment.efficiency_score?.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderCorrelations = () => (
    <div>
      <div className="charts-grid">
        <div className="chart-container">
          <h4>Parameter Correlations</h4>
          <Bar data={correlationData} options={correlationOptions} />
        </div>
        
        <div className="chart-container">
          <h4>Correlation Matrix Heatmap</h4>
          <CorrelationHeatmap correlations={keyCorrelations} />
        </div>
      </div>
      
      <div className="correlation-insights">
        <h4>Correlation Insights</h4>
        <div className="correlation-details">
          <div className="correlation-item">
            <strong>Flowrate-Temperature:</strong> {(keyCorrelations.flowrate_temperature || 0).toFixed(3)}
            <span className="correlation-strength">({interpretCorrelation(keyCorrelations.flowrate_temperature || 0)})</span>
          </div>
          <div className="correlation-item">
            <strong>Flowrate-Pressure:</strong> {(keyCorrelations.flowrate_pressure || 0).toFixed(3)}
            <span className="correlation-strength">({interpretCorrelation(keyCorrelations.flowrate_pressure || 0)})</span>
          </div>
          <div className="correlation-item">
            <strong>Pressure-Temperature:</strong> {(keyCorrelations.pressure_temperature || 0).toFixed(3)}
            <span className="correlation-strength">({interpretCorrelation(keyCorrelations.pressure_temperature || 0)})</span>
          </div>
        </div>
        
        <div className="correlation-implications">
          <h5>Operational Implications</h5>
          <div className="implications-list">
            {Math.abs(keyCorrelations.flowrate_temperature || 0) > 0.5 && (
              <p>• Strong flowrate-temperature relationship suggests thermal efficiency considerations</p>
            )}
            {Math.abs(keyCorrelations.flowrate_pressure || 0) > 0.5 && (
              <p>• Significant flowrate-pressure correlation indicates hydraulic system interdependencies</p>
            )}
            {Math.abs(keyCorrelations.pressure_temperature || 0) > 0.5 && (
              <p>• Pressure-temperature correlation suggests thermodynamic relationships</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderOutliers = () => (
    <div className="charts-grid">
      <div className="chart-container">
        <h4>Outlier Detection Summary</h4>
        <Bar data={outlierSummaryData} options={chartOptions} />
      </div>
      
      <div className="outlier-details">
        <h4>Outlier Analysis</h4>
        {Object.entries(outlierData).map(([parameter, data]) => (
          <div key={parameter} className="outlier-parameter">
            <h5>{parameter}</h5>
            <p>Normal Range: {data.normal_range || 'N/A'}</p>
            <p>Outliers Found: {data.outlier_count || 0}</p>
            <p>Percentage: {(data.outlier_percentage || 0).toFixed(1)}%</p>
            {data.outliers && data.outliers.length > 0 && (
              <div className="outlier-list">
                <strong>Outlier Equipment:</strong>
                <ul>
                  {data.outliers.slice(0, 5).map((outlier, idx) => (
                    <li key={idx}>
                      {outlier.equipment_name} ({outlier.type}): {outlier.value.toFixed(2)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderInsights = () => (
    <div className="insights-container">
      <h4>Key Insights & Recommendations</h4>
      
      {insights.dataset_overview && (
        <div className="insight-section">
          <h5>Dataset Overview</h5>
          <p>Total Equipment: {insights.dataset_overview.total_equipment}</p>
          <p>Equipment Types: {insights.dataset_overview.equipment_types}</p>
        </div>
      )}

      {insights.equipment_type_analysis && (
        <div className="insight-section">
          <h5>Equipment Type Analysis</h5>
          {Object.entries(insights.equipment_type_analysis).map(([type, analysis]) => (
            <div key={type} className="type-analysis">
              <strong>{type} ({analysis.count} units):</strong>
              <p>{analysis.performance_summary}</p>
            </div>
          ))}
        </div>
      )}

      {insights.high_performance_equipment && insights.high_performance_equipment.best_performer && (
        <div className="insight-section">
          <h5>High-Performance Equipment</h5>
          <p><strong>Best Performer:</strong> {insights.high_performance_equipment.best_performer.equipment_name} 
             ({insights.high_performance_equipment.best_performer.type})</p>
          <p><strong>Efficiency Score:</strong> {insights.high_performance_equipment.best_performer.efficiency_score.toFixed(3)}</p>
        </div>
      )}

      {insights.recommendations && (
        <div className="insight-section">
          <h5>Recommendations</h5>
          <ul>
            {insights.recommendations.map((rec, idx) => (
              <li key={idx}>{rec}</li>
            ))}
          </ul>
        </div>
      )}

      {high_temperature_analysis && (
        <div className="insight-section">
          <h5>High Temperature Analysis</h5>
          <p>Equipment above {high_temperature_analysis.threshold}°: {high_temperature_analysis.count} 
             ({high_temperature_analysis.percentage.toFixed(1)}%)</p>
          <p>Temperature Range: {high_temperature_analysis.temperature_stats.min.toFixed(1)}° - 
             {high_temperature_analysis.temperature_stats.max.toFixed(1)}°</p>
        </div>
      )}
    </div>
  );

  return (
    <div className="visualization-container">
      <h3>Comprehensive Analysis Results</h3>
      
      <div className="analysis-tabs">
        <button 
          className={activeTab === 'overview' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={activeTab === 'statistics' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('statistics')}
        >
          Statistics
        </button>
        <button 
          className={activeTab === 'efficiency' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('efficiency')}
        >
          Efficiency
        </button>
        <button 
          className={activeTab === 'correlations' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('correlations')}
        >
          Correlations
        </button>
        <button 
          className={activeTab === 'outliers' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('outliers')}
        >
          Outliers
        </button>
        <button 
          className={activeTab === 'insights' ? 'tab-active' : 'tab'}
          onClick={() => setActiveTab('insights')}
        >
          Insights
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'statistics' && renderStatistics()}
        {activeTab === 'efficiency' && renderEfficiency()}
        {activeTab === 'correlations' && renderCorrelations()}
        {activeTab === 'outliers' && renderOutliers()}
        {activeTab === 'insights' && renderInsights()}
      </div>
    </div>
  );
};

export default DataVisualization;