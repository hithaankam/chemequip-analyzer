"""
API Client for communicating with Django backend
Replicates the same API calls used by the React frontend
"""

import requests
import json
from typing import Dict, Any, Optional, List
from config import API_ENDPOINTS

class APIClient:
    """Client for interacting with the Django backend API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user = None
        
    def set_auth_token(self, token: str):
        """Set authentication token for API requests"""
        self.token = token
        self.session.headers.update({'Authorization': f'Token {token}'})
        
    def clear_auth(self):
        """Clear authentication"""
        self.token = None
        self.user = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def register(self, username: str, password: str, email: str) -> Dict[str, Any]:
        """Register a new user account"""
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        
        response = self.session.post(
            API_ENDPOINTS['register'],
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            self.set_auth_token(result['token'])
            self.user = result['user']
            return result
        else:
            response.raise_for_status()
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login with existing user credentials"""
        data = {
            'username': username,
            'password': password
        }
        
        response = self.session.post(
            API_ENDPOINTS['login'],
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            self.set_auth_token(result['token'])
            self.user = result['user']
            return result
        else:
            response.raise_for_status()
    
    def upload_and_analyze(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file and get analysis results"""
        if not self.token:
            raise Exception("Authentication required")
            
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
            
            response = self.session.post(
                API_ENDPOINTS['analyze'],
                files=files,
                headers={'Authorization': f'Token {self.token}'}
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_history(self) -> Dict[str, Any]:
        """Get dataset upload history"""
        if not self.token:
            raise Exception("Authentication required")
            
        response = self.session.get(
            API_ENDPOINTS['history'],
            headers={'Authorization': f'Token {self.token}'}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Get specific dataset analysis results"""
        if not self.token:
            raise Exception("Authentication required")
            
        url = API_ENDPOINTS['dataset'].format(id=dataset_id)
        response = self.session.get(
            url,
            headers={'Authorization': f'Token {self.token}'}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_upload_history(self) -> List[Dict[str, Any]]:
        """Get dataset upload history for current user"""
        if not self.token:
            raise Exception("Authentication required")
            
        response = self.session.get(
            API_ENDPOINTS['history'],
            headers={'Authorization': f'Token {self.token}'}
        )
        
        if response.status_code == 200:
            result = response.json()
            # Backend returns {'count': X, 'datasets': [...]} but we need just the list
            if isinstance(result, dict) and 'datasets' in result:
                return result['datasets']
            elif isinstance(result, list):
                return result
            else:
                return []
        else:
            response.raise_for_status()
    
    def delete_dataset(self, dataset_id: int) -> bool:
        """Delete a dataset"""
        if not self.token:
            raise Exception("Authentication required")
            
        url = API_ENDPOINTS['dataset'].format(id=dataset_id)
        response = self.session.delete(
            url,
            headers={'Authorization': f'Token {self.token}'}
        )
        
        return response.status_code == 204
    
    def test_connection(self) -> bool:
        """Test if backend API is accessible"""
        try:
            response = self.session.get(API_ENDPOINTS['root'], timeout=5)
            return response.status_code == 200
        except:
            return False