import React, { useState } from 'react';
import FileUpload from './FileUpload';
import DataVisualization from './DataVisualization';
import History from './History';
import { dataAPI } from '../../services/api';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pdfGenerating, setPdfGenerating] = useState(false);

  const handleUploadSuccess = (analysisData) => {
    setCurrentAnalysis(analysisData);
  };

  const handleSelectDataset = async (datasetId) => {
    setLoading(true);
    try {
      const response = await dataAPI.getDataset(datasetId);
      setCurrentAnalysis({
        upload_id: response.data.id,
        analysis_results: response.data.analysis_results
      });
    } catch (error) {
      console.error('Failed to load dataset:', error);
      alert('Failed to load dataset. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    if (!currentAnalysis) {
      alert('No analysis data available for PDF generation');
      return;
    }

    setPdfGenerating(true);
    try {
      const datasetInfo = {
        filename: 'equipment_data.csv', // You can get this from currentAnalysis if available
        upload_date: new Date().toISOString(),
        equipment_count: currentAnalysis.analysis_results?.summary_metrics?.dataset_overview?.total_equipment_count || 0
      };

      const response = await dataAPI.generatePDF(currentAnalysis.analysis_results, datasetInfo);
      
      // Create blob and download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `equipment_analysis_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      alert('PDF report generated successfully!');
    } catch (error) {
      console.error('PDF generation failed:', error);
      alert('Failed to generate PDF report. Please try again.');
    } finally {
      setPdfGenerating(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    onLogout();
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1 className="dashboard-title">Chemical Equipment Analyzer</h1>
        <div className="user-info">
          <span>Welcome, {user.username}!</span>
          {currentAnalysis && (
            <button 
              onClick={handleGeneratePDF} 
              disabled={pdfGenerating}
              className="pdf-button"
            >
              {pdfGenerating ? 'Generating PDF...' : '📄 Generate PDF Report'}
            </button>
          )}
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
        <History onSelectDataset={handleSelectDataset} />
      </div>

      {loading && (
        <div className="loading">Loading dataset...</div>
      )}

      {currentAnalysis && !loading && (
        <DataVisualization analysisData={currentAnalysis} />
      )}
    </div>
  );
};

export default Dashboard;