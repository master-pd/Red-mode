# file: method_08_cookies.py
import json
import re
import base64
from datetime import datetime

class CookieAnalyzer:
    """Cookie Data Analyzer"""
    
    def __init__(self):
        self.name = "Cookie Data Analyzer"
        
    def execute(self, cookies_data):
        """Cookie ডাটা অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            if isinstance(cookies_data, str):
                cookies = json.loads(cookies_data)
            else:
                cookies = cookies_data
            
            analysis = {
                'total_cookies': len(cookies),
                'facebook_cookies': self.analyze_facebook_cookies(cookies),
                'session_cookies': self.find_session_cookies(cookies),
                'authentication_cookies': self.find_auth_cookies(cookies),
                'tracking_cookies': self.find_tracking_cookies(cookies),
                'cookie_patterns': self.analyze_cookie_patterns(cookies),
                'security_analysis': self.security_analysis(cookies)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def analyze_facebook_cookies(self, cookies):
        """ফেসবুক কুকি অ্যানালাইসিস"""
        fb_cookies = []
        
        for cookie in cookies:
            if 'domain' in cookie and 'facebook' in cookie['domain'].lower():
                cookie_info = {
                    'name': cookie.get('name', ''),
                    'domain': cookie.get('domain', ''),
                    'path': cookie.get('path', '/'),
                    'secure': cookie.get('secure', False),
                    'http_only': cookie.get('http_only', False),
                    'session': cookie.get('expires') is None,
                    'purpose': self.guess_cookie_purpose(cookie.get('name', ''))
                }
                
                fb_cookies.append(cookie_info)
        
        return fb_cookies
    
    def guess_cookie_purpose(self, cookie_name):
        """কুকির উদ্দেশ্য অনুমান"""
        purposes = {
            'c_user': 'User ID',
            'xs': 'Session token',
            'fr': 'Browser fingerprint',
            'datr': 'Device recognition',
            'sb': 'Browser ID',
            'wd': 'Window size',
            'presence': 'Online status',
            'locale': 'Language preference',
            'pl': 'Page load',
            'lu': 'Last user',
            'm_pixel_ratio': 'Device pixel ratio'
        }
        
        for key, purpose in purposes.items():
            if key in cookie_name.lower():
                return purpose
        
        return 'Unknown'
    
    def find_session_cookies(self, cookies):
        """সেশন কুকি খোঁজা"""
        session_cookies = []
        
        for cookie in cookies:
            # সেশন কুকি (no expires date)
            if 'expires' not in cookie or cookie['expires'] is None:
                session_cookies.append({
                    'name': cookie.get('name', ''),
                    'domain': cookie.get('domain', ''),
                    'secure': cookie.get('secure', False)
                })
        
        return session_cookies
    
    def find_auth_cookies(self, cookies):
        """অথেন্টিকেশন কুকি"""
        auth_patterns = ['token', 'auth', 'session', 'login', 'access', 'refresh']
        auth_cookies = []
        
        for cookie in cookies:
            cookie_name = cookie.get('name', '').lower()
            if any(pattern in cookie_name for pattern in auth_patterns):
                auth_cookies.append({
                    'name': cookie.get('name', ''),
                    'domain': cookie.get('domain', ''),
                    'value_length': len(str(cookie.get('value', '')))
                })
        
        return auth_cookies
    
    def find_tracking_cookies(self, cookies):
        """ট্র্যাকিং কুকি"""
        tracking_patterns = ['_ga', '_gid', '_gat', 'fbp', 'fbc', '_uetsid']
        tracking_cookies = []
        
        for cookie in cookies:
            cookie_name = cookie.get('name', '')
            if any(pattern in cookie_name.lower() for pattern in tracking_patterns):
                tracking_cookies.append({
                    'name': cookie_name,
                    'domain': cookie.get('domain', ''),
                    'purpose': self.get_tracking_purpose(cookie_name)
                })
        
        return tracking_cookies
    
    def get_tracking_purpose(self, cookie_name):
        """ট্র্যাকিং কুকির উদ্দেশ্য"""
        purposes = {
            '_ga': 'Google Analytics',
            '_gid': 'Google Analytics',
            '_gat': 'Google Analytics Throttle',
            'fbp': 'Facebook Pixel',
            'fbc': 'Facebook Click ID',
            '_uetsid': 'Bing Ads'
        }
        
        return purposes.get(cookie_name, 'Tracking')
    
    def analyze_cookie_patterns(self, cookies):
        """কুকি প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'hashed_values': 0,
            'base64_values': 0,
            'json_values': 0,
            'long_values': 0
        }
        
        for cookie in cookies:
            value = str(cookie.get('value', ''))
            
            # হ্যাশড ভ্যালু চেক
            if re.match(r'^[a-fA-F0-9]{32,}$', value):
                patterns['hashed_values'] += 1
            
            # Base64 ভ্যালু চেক
            try:
                if len(value) % 4 == 0 and re.match(r'^[A-Za-z0-9+/]+={0,2}$', value):
                    base64.b64decode(value)
                    patterns['base64_values'] += 1
            except:
                pass
            
            # JSON ভ্যালু চেক
            if value.startswith('{') and value.endswith('}'):
                try:
                    json.loads(value)
                    patterns['json_values'] += 1
                except:
                    pass
            
            # লং ভ্যালু
            if len(value) > 100:
                patterns['long_values'] += 1
        
        return patterns
    
    def security_analysis(self, cookies):
        """সিকিউরিটি অ্যানালাইসিস"""
        security = {
            'secure_cookies': 0,
            'http_only_cookies': 0,
            'same_site_cookies': 0,
            'insecure_cookies': 0
        }
        
        for cookie in cookies:
            if cookie.get('secure'):
                security['secure_cookies'] += 1
            else:
                security['insecure_cookies'] += 1
            
            if cookie.get('http_only'):
                security['http_only_cookies'] += 1
            
            if 'same_site' in cookie:
                security['same_site_cookies'] += 1
        
        return security