import React, { useState, useEffect } from 'react';
import { dataAPI } from '../../services/api';
import './Dashboard.css';

const History = ({ onSelectDataset }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await dataAPI.getHistory();
      setHistory(response.data.datasets);
    } catch (err) {
      setError('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const formatFileSize = (bytes) => {
    return (bytes / 1024).toFixed(1) + ' KB';
  };

  if (loading) return <div className="loading">Loading history...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="history-container">
      <h3>Upload History</h3>
      {history.length === 0 ? (
        <div className="no-data">No uploads yet. Upload your first CSV file to get started!</div>
      ) : (
        <div className="history-list">
          {history.map((dataset) => (
            <div key={dataset.id} className="history-item">
              <div className="history-info">
                <div className="history-filename">{dataset.filename}</div>
                <div className="history-meta">
                  <span>Uploaded: {formatDate(dataset.upload_date)}</span>
                  <span>Size: {formatFileSize(dataset.file_size)}</span>
                  <span>Equipment: {dataset.equipment_count}</span>
                </div>
                {dataset.summary_stats && (
                  <div className="history-stats">
                    <span>Avg Flowrate: {dataset.summary_stats.overall_stats?.Flowrate?.mean?.toFixed(1) || 'N/A'}</span>
                    <span>Avg Pressure: {dataset.summary_stats.overall_stats?.Pressure?.mean?.toFixed(1) || 'N/A'}</span>
                    <span>Avg Temperature: {dataset.summary_stats.overall_stats?.Temperature?.mean?.toFixed(1) || 'N/A'}</span>
                  </div>
                )}
              </div>
              <button
                onClick={() => onSelectDataset(dataset.id)}
                className="view-button"
              >
                View Details
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;