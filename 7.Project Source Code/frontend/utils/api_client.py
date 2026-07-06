"""
API Client - Centralized backend communication
"""

import requests
import streamlit as st


class APIClient:
    """API client for backend communication"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or st.session_state.get('base_url', 'http://127.0.0.1:8000')
        self.timeout = 30
    
    def _request(self, method, endpoint, **kwargs):
        """Make a request to the backend"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        
        try:
            response = requests.request(method, url, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Make sure the server is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    def get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)
    
    def put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)
    
    # === Specific API Methods ===
    
    def health_check(self):
        return self.get('/health')
    
    def analyze_event(self, description, custom_themes=None):
        return self.post('/analyze-event', json={
            'description': description,
            'custom_themes': custom_themes
        })
    
    def generate_conversation(self, event_description, user_interests, max_suggestions=3):
        return self.post('/generate-conversation', json={
            'event_description': event_description,
            'user_interests': user_interests,
            'max_suggestions': max_suggestions
        })
    
    def fact_check(self, query):
        return self.post('/fact-check', json={'query': query})
    
    def submit_feedback(self, suggestion, action):
        return self.post('/feedback', json={
            'suggestion': suggestion,
            'action': action
        })
    
    def get_history(self, limit=10, offset=0):
        return self.get(f'/history?limit={limit}&offset={offset}')
    
    def get_feedback_stats(self):
        return self.get('/feedback/stats')
    
    def get_admin_stats(self):
        return self.get('/admin/stats')


# Singleton instance
api_client = APIClient()