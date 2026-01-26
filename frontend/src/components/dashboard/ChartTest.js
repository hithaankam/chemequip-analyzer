import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const ChartTest = () => {
  // Simple test data
  const testBarData = {
    labels: ['Pump', 'Compressor', 'Valve'],
    datasets: [
      {
        label: 'Equipment Count',
        data: [4, 2, 3],
        backgroundColor: 'rgba(135, 206, 235, 0.8)',
        borderColor: 'rgba(0, 0, 0, 1)',
        borderWidth: 1,
      },
    ],
  };

  const testPieData = {
    labels: ['Pump', 'Compressor', 'Valve'],
    datasets: [
      {
        data: [4, 2, 3],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 205, 86, 0.8)',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Test Chart',
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
      title: {
        display: true,
        text: 'Test Pie Chart',
      },
    },
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Chart.js Test</h2>
      <p>This component tests if Chart.js is working properly.</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '10px' }}>
          <h4>Test Bar Chart</h4>
          <Bar data={testBarData} options={chartOptions} />
        </div>
        
        <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '10px' }}>
          <h4>Test Pie Chart</h4>
          <Pie data={testPieData} options={pieOptions} />
        </div>
      </div>
      
      <div style={{ marginTop: '20px', padding: '15px', background: '#e8f5e8', borderRadius: '5px' }}>
        <strong>If you can see the charts above, Chart.js is working correctly!</strong>
        <br />
        If the charts are empty or not showing, there might be an issue with Chart.js setup.
      </div>
    </div>
  );
};

export default ChartTest;