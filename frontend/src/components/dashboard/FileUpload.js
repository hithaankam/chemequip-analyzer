import React, { useState } from 'react';
import { dataAPI } from '../../services/api';
import './Dashboard.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== 'text/csv' && !selectedFile.name.endsWith('.csv')) {
        setError('Please select a CSV file');
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');

    try {
      const response = await dataAPI.uploadFile(file);
      onUploadSuccess(response.data);
      setFile(null);
      document.getElementById('file-input').value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <h3>Upload Chemical Equipment Data</h3>
      <div className="upload-area">
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="file-input"
        />
        <div className="file-info">
          {file ? (
            <div className="file-selected">
              <span className="file-name">{file.name}</span>
              <span className="file-size">({(file.size / 1024).toFixed(1)} KB)</span>
            </div>
          ) : (
            <span className="file-placeholder">No file selected</span>
          )}
        </div>
        {error && <div className="error-message">{error}</div>}
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload & Analyze'}
        </button>
      </div>
    </div>
  );
};

export default FileUpload;