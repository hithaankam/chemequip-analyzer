import React, { useState, useEffect } from 'react';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import TestDataVisualization from './components/TestDataVisualization';
import ChartTest from './components/Dashboard/ChartTest';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState('login');
  const [loading, setLoading] = useState(true);
  const [showTest, setShowTest] = useState(false);
  const [showChartTest, setShowChartTest] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  const switchToRegister = () => {
    setAuthMode('register');
  };

  const switchToLogin = () => {
    setAuthMode('login');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  // Chart test mode
  if (showChartTest) {
    return (
      <div>
        <button onClick={() => setShowChartTest(false)} style={{ margin: '10px' }}>
          Back to App
        </button>
        <ChartTest />
      </div>
    );
  }

  // API test mode
  if (showTest) {
    return (
      <div>
        <button onClick={() => setShowTest(false)} style={{ margin: '10px' }}>
          Back to App
        </button>
        <TestDataVisualization />
      </div>
    );
  }

  if (!user) {
    return (
      <div>
        <div style={{ margin: '10px', display: 'flex', gap: '10px' }}>
          <button onClick={() => setShowTest(true)}>
            Test API
          </button>
          <button onClick={() => setShowChartTest(true)}>
            Test Charts
          </button>
        </div>
        {authMode === 'login' ? (
          <Login onLogin={handleLogin} switchToRegister={switchToRegister} />
        ) : (
          <Register onLogin={handleLogin} switchToLogin={switchToLogin} />
        )}
      </div>
    );
  }

  return (
    <div>
      <div style={{ margin: '10px', display: 'flex', gap: '10px' }}>
        <button onClick={() => setShowTest(true)}>
          Test API
        </button>
        <button onClick={() => setShowChartTest(true)}>
          Test Charts
        </button>
      </div>
      <Dashboard user={user} onLogout={handleLogout} />
    </div>
  );
}

export default App;
