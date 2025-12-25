# file: method_04_api.py
import requests
import json
import re

class APIScanner:
    """API Endpoint Scanner"""
    
    def __init__(self):
        self.name = "API Endpoint Scanner"
        self.api_patterns = [
            r'https?://[^"\']+\.facebook\.com/[^"\']+api[^"\']*',
            r'https?://api\.facebook\.com/[^"\']+',
            r'https?://graph\.facebook\.com/[^"\']+',
            r'https?://[^"\']+/api/[^"\']+',
            r'window\.__APIS__\s*=\s*({[^}]+})',
            r'"api_url"\s*:\s*"([^"]+)"',
            r"'api_url'\s*:\s*'([^']+)'",
            r'apiEndpoint[^=]+=\s*["\']([^"\']+)["\']'
        ]
    
    def execute(self, url_or_html):
        """API স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            # যদি URL হয়, তাহলে HTML নিয়ে আসো
            if url_or_html.startswith('http'):
                html = self.fetch_html(url_or_html)
            else:
                html = url_or_html
            
            if html:
                api_endpoints = self.extract_api_endpoints(html)
                api_responses = self.test_api_endpoints(api_endpoints)
                
                results['data'] = {
                    'endpoints_found': len(api_endpoints),
                    'endpoints': api_endpoints,
                    'tested_responses': api_responses
                }
                results['success'] = True
                
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def fetch_html(self, url):
        """HTML fetch"""
        try:
            response = requests.get(url, timeout=30)
            return response.text if response.status_code == 200 else None
        except:
            return None
    
    def extract_api_endpoints(self, html):
        """API endpoints extract"""
        endpoints = []
        
        for pattern in self.api_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                # JSON থেকে API URL বের করা
                if match.startswith('{'):
                    try:
                        data = json.loads(match)
                        endpoints.extend(self.extract_urls_from_json(data))
                    except:
                        pass
                else:
                    if match not in endpoints:
                        endpoints.append(match)
        
        # ডুপ্লিকেট রিমুভ
        return list(set(endpoints))
    
    def extract_urls_from_json(self, data):
        """JSON থেকে URL বের করা"""
        urls = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and ('http' in value.lower() or 'api' in key.lower()):
                    urls.append(value)
                elif isinstance(value, (dict, list)):
                    urls.extend(self.extract_urls_from_json(value))
        elif isinstance(data, list):
            for item in data:
                urls.extend(self.extract_urls_from_json(item))
        
        return urls
    
    def test_api_endpoints(self, endpoints):
        """API endpoints test"""
        results = []
        
        for endpoint in endpoints[:10]:  # প্রথম ১০টা টেস্ট
            try:
                response = requests.get(endpoint, timeout=10)
                
                result = {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type', ''),
                    'content_length': len(response.text),
                    'is_json': 'application/json' in response.headers.get('content-type', '')
                }
                
                # যদি JSON হয়, কিছু ডাটা সেভ
                if result['is_json']:
                    try:
                        json_data = response.json()
                        # শুধু প্রথম কয়েকটা key
                        result['json_keys'] = list(json_data.keys())[:5]
                    except:
                        result['json_keys'] = []
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'endpoint': endpoint,
                    'error': str(e)
                })
        
        return results