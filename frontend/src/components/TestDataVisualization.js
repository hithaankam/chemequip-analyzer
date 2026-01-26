import React, { useState, useEffect } from 'react';

const TestDataVisualization = () => {
  const [testData, setTestData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [authToken, setAuthToken] = useState(null);
  const [user, setUser] = useState(null);

  const testAPI = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('=== Starting Frontend API Test ===');
      
      // Test 1: Check API root
      console.log('1. Testing API root...');
      const rootResponse = await fetch('http://127.0.0.1:8000/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!rootResponse.ok) {
        throw new Error(`API root failed: ${rootResponse.status}`);
      }
      
      const rootData = await rootResponse.json();
      console.log('✅ API Root accessible:', rootData);
      
      // Test 2: Register/Login
      console.log('2. Testing authentication...');
      const registerData = {
        username: 'frontendtest123',
        password: 'testpass123',
        email: 'frontendtest@example.com'
      };
      
      let token;
      let userData;
      
      try {
        // Try registration first
        console.log('Attempting registration...');
        const registerResponse = await fetch('http://127.0.0.1:8000/api/register/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(registerData)
        });
        
        console.log('Register response status:', registerResponse.status);
        
        if (registerResponse.status === 201) {
          const result = await registerResponse.json();
          token = result.token;
          userData = result.user;
          console.log('✅ Registration successful');
        } else if (registerResponse.status === 400) {
          // Try login
          console.log('User exists, trying login...');
          const loginResponse = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: registerData.username,
              password: registerData.password
            })
          });
          
          console.log('Login response status:', loginResponse.status);
          
          if (loginResponse.status === 200) {
            const result = await loginResponse.json();
            token = result.token;
            userData = result.user;
            console.log('✅ Login successful');
          } else {
            const errorText = await loginResponse.text();
            throw new Error(`Login failed: ${loginResponse.status} - ${errorText}`);
          }
        } else {
          const errorText = await registerResponse.text();
          throw new Error(`Registration failed: ${registerResponse.status} - ${errorText}`);
        }
      } catch (authError) {
        console.error('Authentication error:', authError);
        throw new Error(`Auth error: ${authError.message}`);
      }
      
      setAuthToken(token);
      setUser(userData);
      console.log('Token:', token.substring(0, 20) + '...');
      console.log('User:', userData);
      
      // Test 3: Test protected endpoint (history)
      console.log('3. Testing protected endpoint...');
      const historyResponse = await fetch('http://127.0.0.1:8000/api/history/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        }
      });
      
      console.log('History response status:', historyResponse.status);
      
      if (historyResponse.status === 200) {
        const historyData = await historyResponse.json();
        console.log('✅ Protected endpoint accessible:', historyData);
      } else {
        const errorText = await historyResponse.text();
        console.log('❌ Protected endpoint failed:', errorText);
      }
      
      // Test 4: Upload and analyze
      console.log('4. Testing file upload...');
      const csvContent = `Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
HeatExchanger-1,HeatExchanger,150,6.2,130
Pump-2,Pump,132,5.6,118`;
      
      const formData = new FormData();
      const blob = new Blob([csvContent], { type: 'text/csv' });
      formData.append('file', blob, 'test_data.csv');
      
      console.log('Uploading file with token:', token.substring(0, 20) + '...');
      
      const uploadResponse = await fetch('http://127.0.0.1:8000/api/analyze/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`
          // Note: Don't set Content-Type for FormData, let browser set it
        },
        body: formData
      });
      
      console.log('Upload response status:', uploadResponse.status);
      console.log('Upload response headers:', Object.fromEntries(uploadResponse.headers.entries()));
      
      if (uploadResponse.status === 200) {
        const result = await uploadResponse.json();
        console.log('✅ Analysis successful!');
        console.log('Upload ID:', result.upload_id);
        console.log('Analysis result keys:', Object.keys(result));
        
        if (result.analysis_results) {
          console.log('Analysis data keys:', Object.keys(result.analysis_results));
          setTestData(result);
        } else {
          console.log('❌ No analysis_results in response');
        }
      } else {
        const errorText = await uploadResponse.text();
        console.log('❌ Upload failed:', errorText);
        throw new Error(`Upload failed: ${uploadResponse.status} - ${errorText.substring(0, 200)}`);
      }
      
    } catch (err) {
      console.error('Test error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderDataStructure = (data, level = 0) => {
    if (!data) return null;
    
    const indent = '  '.repeat(level);
    
    if (typeof data === 'object' && data !== null) {
      if (Array.isArray(data)) {
        return (
          <div>
            {indent}Array ({data.length} items)
            {data.length > 0 && (
              <div style={{ marginLeft: '20px' }}>
                {renderDataStructure(data[0], level + 1)}
              </div>
            )}
          </div>
        );
      } else {
        return (
          <div>
            {Object.keys(data).slice(0, 10).map(key => (
              <div key={key}>
                {indent}{key}: {typeof data[key] === 'object' ? 
                  renderDataStructure(data[key], level + 1) : 
                  `${typeof data[key]} (${String(data[key]).substring(0, 50)}${String(data[key]).length > 50 ? '...' : ''})`
                }
              </div>
            ))}
            {Object.keys(data).length > 10 && <div>{indent}... and {Object.keys(data).length - 10} more</div>}
          </div>
        );
      }
    } else {
      return <span>{String(data)}</span>;
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h2>Frontend API Authentication Test</h2>
      
      <button onClick={testAPI} disabled={loading} style={{ 
        padding: '10px 20px', 
        fontSize: '16px',
        backgroundColor: loading ? '#ccc' : '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: loading ? 'not-allowed' : 'pointer'
      }}>
        {loading ? 'Testing API...' : 'Test Frontend Authentication'}
      </button>
      
      {authToken && (
        <div style={{ margin: '10px 0', padding: '10px', backgroundColor: '#e8f5e8', border: '1px solid #4caf50' }}>
          <strong>Authentication Status:</strong>
          <br />Token: {authToken.substring(0, 30)}...
          <br />User: {user?.username} (ID: {user?.id})
        </div>
      )}
      
      {error && (
        <div style={{ color: 'red', margin: '10px 0', padding: '10px', backgroundColor: '#ffe8e8', border: '1px solid #f44336' }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {testData && (
        <div style={{ marginTop: '20px' }}>
          <h3>API Response Structure:</h3>
          <div style={{ 
            backgroundColor: '#f5f5f5', 
            padding: '10px', 
            border: '1px solid #ddd',
            fontSize: '12px',
            maxHeight: '400px',
            overflow: 'auto'
          }}>
            {renderDataStructure(testData)}
          </div>
          
          {testData.analysis_results && (
            <div style={{ marginTop: '20px' }}>
              <h3>Key Data Sections:</h3>
              <ul>
                <li>summary_metrics: {testData.analysis_results.summary_metrics ? '✅' : '❌'}</li>
                <li>distributions: {testData.analysis_results.distributions ? '✅' : '❌'}</li>
                <li>efficiency: {testData.analysis_results.efficiency ? '✅' : '❌'}</li>
                <li>correlations: {testData.analysis_results.correlations ? '✅' : '❌'}</li>
                <li>type_metrics: {testData.analysis_results.type_metrics ? '✅' : '❌'}</li>
              </ul>
              
              {testData.analysis_results.distributions?.equipment_types && (
                <div>
                  <h4>Equipment Types:</h4>
                  <pre style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
                    {JSON.stringify(testData.analysis_results.distributions.equipment_types, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>
      )}
      
      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        <strong>Instructions:</strong>
        <ol>
          <li>Click the test button above</li>
          <li>Check the browser console (F12) for detailed logs</li>
          <li>Look for any CORS or authentication errors</li>
          <li>If successful, you should see data sections marked with ✅</li>
        </ol>
      </div>
    </div>
  );
};

export default TestDataVisualization;