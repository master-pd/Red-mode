# file: api/facebook_api.py
import requests
import json
import time
from typing import Dict, List, Optional

class FacebookAPI:
    """Facebook API Wrapper"""
    
    def __init__(self, access_token=None):
        self.base_url = "https://graph.facebook.com"
        self.version = "v18.0"
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def set_access_token(self, token):
        """Access token সেট"""
        self.access_token = token
    
    def make_request(self, endpoint, params=None, method='GET'):
        """API রিকুয়েস্ট"""
        if params is None:
            params = {}
        
        if self.access_token:
            params['access_token'] = self.access_token
        
        url = f"{self.base_url}/{self.version}/{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=30)
            elif method == 'POST':
                response = self.session.post(url, json=params, timeout=30)
            else:
                return {'error': f'Unsupported method: {method}'}
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:500]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_public_profile(self, user_id):
        """পাবলিক প্রোফাইল তথ্য"""
        params = {
            'fields': 'id,name,first_name,last_name,middle_name,name_format,picture,short_name'
        }
        
        return self.make_request(f"{user_id}", params)
    
    def get_profile_picture(self, user_id, type='large'):
        """প্রোফাইল পিকচার"""
        params = {
            'redirect': 'false',
            'type': type,
            'height': 500,
            'width': 500
        }
        
        return self.make_request(f"{user_id}/picture", params)
    
    def get_friends(self, user_id, limit=100):
        """ফ্রেন্ডস লিস্ট (যদি পারমিশন থাকে)"""
        params = {
            'fields': 'id,name,picture',
            'limit': limit
        }
        
        return self.make_request(f"{user_id}/friends", params)
    
    def get_photos(self, user_id, limit=50):
        """ফটোস"""
        params = {
            'fields': 'id,name,picture,created_time,images',
            'limit': limit,
            'type': 'uploaded'
        }
        
        return self.make_request(f"{user_id}/photos", params)
    
    def get_posts(self, user_id, limit=50):
        """পোস্টস"""
        params = {
            'fields': 'id,message,created_time,story,attachments',
            'limit': limit
        }
        
        return self.make_request(f"{user_id}/posts", params)
    
    def get_events(self, user_id, limit=50):
        """ইভেন্টস"""
        params = {
            'fields': 'id,name,description,start_time,end_time,place',
            'limit': limit
        }
        
        return self.make_request(f"{user_id}/events", params)
    
    def get_groups(self, user_id, limit=50):
        """গ্রুপস"""
        params = {
            'fields': 'id,name,description,privacy',
            'limit': limit
        }
        
        return self.make_request(f"{user_id}/groups", params)
    
    def get_likes(self, user_id, limit=50):
        """লাইকস"""
        params = {
            'fields': 'id,name,category',
            'limit': limit
        }
        
        return self.make_request(f"{user_id}/likes", params)
    
    def get_comments(self, post_id, limit=100):
        """কমেন্টস"""
        params = {
            'fields': 'id,message,created_time,from',
            'limit': limit
        }
        
        return self.make_request(f"{post_id}/comments", params)
    
    def search_public(self, query, search_type='user', limit=50):
        """পাবলিক সার্চ"""
        params = {
            'q': query,
            'type': search_type,
            'fields': 'id,name,picture',
            'limit': limit
        }
        
        return self.make_request('search', params)
    
    def get_page_info(self, page_id):
        """পেজ ইনফো"""
        params = {
            'fields': 'id,name,about,description,category,fan_count,phone,website,location'
        }
        
        return self.make_request(f"{page_id}", params)
    
    def batch_requests(self, requests_list):
        """ব্যাচ রিকুয়েস্ট"""
        batch = []
        for i, req in enumerate(requests_list):
            batch.append({
                'method': req.get('method', 'GET'),
                'relative_url': req['url'],
                'name': req.get('name', f'request_{i}')
            })
        
        params = {
            'batch': json.dumps(batch),
            'include_headers': 'false'
        }
        
        return self.make_request('', params, method='POST')
    
    def test_token_validity(self):
        """টোকেন ভ্যালিডিটি টেস্ট"""
        if not self.access_token:
            return {'error': 'No access token provided'}
        
        params = {
            'input_token': self.access_token,
            'access_token': self.access_token
        }
        
        return self.make_request('debug_token', params)
    
    def get_token_permissions(self):
        """টোকেন পারমিশন চেক"""
        if not self.access_token:
            return {'error': 'No access token provided'}
        
        params = {
            'fields': 'permissions'
        }
        
        return self.make_request('me', params)
    
    def rate_limited_request(self, endpoint, params=None, delay=1):
        """রেট লিমিটেড রিকুয়েস্ট"""
        if params is None:
            params = {}
        
        result = self.make_request(endpoint, params)
        
        # Check for rate limiting
        if isinstance(result, dict) and 'error' in result:
            error_code = result['error'].get('code', 0)
            if error_code == 4 or error_code == 32:  # Rate limiting codes
                time.sleep(delay * 2)  # Exponential backoff
                return self.rate_limited_request(endpoint, params, delay * 2)
        
        return result