import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  
  // Debug logging
  console.log('API Request:', {
    method: config.method,
    url: config.url,
    headers: config.headers,
    data: config.data
  });
  
  return config;
});

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response Success:', {
      status: response.status,
      url: response.config.url,
      data: response.data
    });
    return response;
  },
  (error) => {
    console.error('API Response Error:', {
      status: error.response?.status,
      url: error.config?.url,
      data: error.response?.data,
      message: error.message
    });
    
    // If unauthorized, clear auth data
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.reload();
    }
    
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (userData) => api.post('/register/', userData),
  login: (credentials) => api.post('/login/', credentials),
};

export const dataAPI = {
  // Test connection to backend using health check endpoint
  testConnection: () => api.get('/health/', { baseURL: 'http://127.0.0.1:8000' }),
  
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/analyze/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  getHistory: () => api.get('/history/'),
  getDataset: (id) => api.get(`/dataset/${id}/`),
  generatePDF: (analysisResults, datasetInfo) => {
    return api.post('/generate-pdf/', {
      analysis_results: analysisResults,
      dataset_info: datasetInfo
    }, {
      responseType: 'blob', // Important for PDF download
      headers: {
        'Content-Type': 'application/json',
      },
    });
  },
  generatePDFFromDataset: (datasetId) => {
    return api.get(`/generate-pdf/${datasetId}/`, {
      responseType: 'blob', // Important for PDF download
    });
  },
};

export default api;