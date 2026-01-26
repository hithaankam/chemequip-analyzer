import React, { useState } from 'react';
import FileUpload from './FileUpload';
import DataVisualization from './DataVisualization';
import History from './History';
import { dataAPI } from '../../services/api';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUploadSuccess = (analysisData) => {
    console.log('Upload success data:', analysisData); // Debug log
    setCurrentAnalysis(analysisData);
  };

  const handleSelectDataset = async (datasetId) => {
    setLoading(true);
    try {
      const response = await dataAPI.getDataset(datasetId);
      console.log('Dataset response:', response.data); // Debug log
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