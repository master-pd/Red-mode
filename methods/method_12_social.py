# file: method_12_social.py
import requests
import re
import json
from urllib.parse import urlparse, urljoin

class SocialMediaScanner:
    """সোশ্যাল মিডিয়া স্ক্যানার"""
    
    def __init__(self):
        self.name = "Social Media Scanner"
        self.platforms = {
            'facebook': {
                'patterns': [
                    r'facebook\.com/([^/?"\']+)',
                    r'fb\.com/([^/?"\']+)',
                    r'fb\.me/([^/?"\']+)'
                ],
                'api_urls': [
                    'https://graph.facebook.com/{username}',
                    'https://www.facebook.com/{username}'
                ]
            },
            'twitter': {
                'patterns': [
                    r'twitter\.com/([^/?"\']+)',
                    r'x\.com/([^/?"\']+)'
                ],
                'api_urls': [
                    'https://api.twitter.com/1.1/users/show.json?screen_name={username}'
                ]
            },
            'instagram': {
                'patterns': [
                    r'instagram\.com/([^/?"\']+)',
                    r'instagr\.am/([^/?"\']+)'
                ],
                'api_urls': [
                    'https://www.instagram.com/{username}/?__a=1'
                ]
            },
            'linkedin': {
                'patterns': [
                    r'linkedin\.com/in/([^/?"\']+)',
                    r'linkedin\.com/company/([^/?"\']+)'
                ]
            },
            'youtube': {
                'patterns': [
                    r'youtube\.com/(?:user/|channel/|@)([^/?"\']+)'
                ]
            },
            'tiktok': {
                'patterns': [
                    r'tiktok\.com/@([^/?"\']+)'
                ]
            },
            'whatsapp': {
                'patterns': [
                    r'wa\.me/(\d+)',
                    r'whatsapp\.com/(?:send\?phone=)?(\d+)'
                ]
            },
            'telegram': {
                'patterns': [
                    r't\.me/([^/?"\']+)'
                ]
            }
        }
    
    def execute(self, target):
        """সোশ্যাল মিডিয়া স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            social_profiles = {}
            
            # Direct username scan
            if not '/' in target and not '@' in target:
                # Assume it's a username
                social_profiles['username_search'] = self.search_by_username(target)
            
            # URL scan
            elif 'http' in target:
                social_profiles['url_scan'] = self.scan_url(target)
            
            # Text/content scan
            else:
                social_profiles['text_scan'] = self.scan_text(target)
            
            # Platform specific checks
            social_profiles['platform_checks'] = self.check_all_platforms(target)
            
            results['data'] = social_profiles
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def search_by_username(self, username):
        """ইউজারনেম দিয়ে সার্চ"""
        profiles = {}
        
        for platform, info in self.platforms.items():
            for api_url_template in info.get('api_urls', []):
                try:
                    api_url = api_url_template.format(username=username)
                    response = requests.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        profiles[platform] = {
                            'url': api_url,
                            'exists': True,
                            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:500]
                        }
                except:
                    continue
        
        return profiles
    
    def scan_url(self, url):
        """URL স্ক্যান"""
        url_data = {
            'original_url': url,
            'parsed': urlparse(url),
            'social_links_found': []
        }
        
        # Fetch the page
        try:
            response = requests.get(url, timeout=10)
            html = response.text
            
            # Extract all social links
            all_links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
            
            for link in all_links:
                for platform, info in self.platforms.items():
                    for pattern in info['patterns']:
                        if re.search(pattern, link, re.IGNORECASE):
                            url_data['social_links_found'].append({
                                'platform': platform,
                                'url': link,
                                'matched_pattern': pattern
                            })
                            break
            
            # Also check meta tags for social info
            url_data['meta_tags'] = self.extract_social_meta(html)
            
        except Exception as e:
            url_data['error'] = str(e)
        
        return url_data
    
    def extract_social_meta(self, html):
        """সোশ্যাল মেটাডাটা এক্সট্র্যাক্ট"""
        social_meta = {}
        
        # Facebook meta
        fb_patterns = {
            'fb:app_id': r'fb:app_id["\'][^>]*content=["\']([^"\']+)["\']',
            'og:url': r'property="og:url"\s+content="([^"]+)"',
            'og:title': r'property="og:title"\s+content="([^"]+)"',
            'og:description': r'property="og:description"\s+content="([^"]+)"',
            'og:image': r'property="og:image"\s+content="([^"]+)"'
        }
        
        for key, pattern in fb_patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                social_meta[key] = match.group(1)
        
        # Twitter meta
        twitter_patterns = {
            'twitter:site': r'twitter:site["\'][^>]*content=["\']([^"\']+)["\']',
            'twitter:creator': r'twitter:creator["\'][^>]*content=["\']([^"\']+)["\']',
            'twitter:title': r'twitter:title["\'][^>]*content=["\']([^"\']+)["\']'
        }
        
        for key, pattern in twitter_patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                social_meta[key] = match.group(1)
        
        return social_meta
    
    def scan_text(self, text):
        """টেক্সট থেকে সোশ্যাল লিংক খোঁজা"""
        text_data = {
            'text_length': len(text),
            'social_mentions': [],
            'hashtags': [],
            'mentions': []
        }
        
        # Find social URLs
        for platform, info in self.platforms.items():
            for pattern in info['patterns']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    text_data['social_mentions'].append({
                        'platform': platform,
                        'username': match,
                        'url': f"https://{platform}.com/{match}"
                    })
        
        # Find hashtags
        hashtags = re.findall(r'#(\w+)', text)
        text_data['hashtags'] = list(set(hashtags))
        
        # Find mentions (@username)
        mentions = re.findall(r'@(\w+)', text)
        text_data['mentions'] = list(set(mentions))
        
        return text_data
    
    def check_all_platforms(self, identifier):
        """সব প্ল্যাটফর্ম চেক"""
        platform_results = {}
        
        for platform, info in self.platforms.items():
            platform_data = {
                'patterns_matched': [],
                'possible_profiles': [],
                'check_status': 'not_found'
            }
            
            # Check if identifier matches platform patterns
            for pattern in info['patterns']:
                matches = re.findall(pattern, identifier, re.IGNORECASE)
                if matches:
                    platform_data['patterns_matched'].extend(matches)
                    platform_data['check_status'] = 'pattern_matched'
            
            # Generate possible profile URLs
            if platform_data['patterns_matched']:
                for username in set(platform_data['patterns_matched']):
                    if platform == 'facebook':
                        platform_data['possible_profiles'].append(f"https://facebook.com/{username}")
                    elif platform == 'twitter':
                        platform_data['possible_profiles'].append(f"https://twitter.com/{username}")
                    elif platform == 'instagram':
                        platform_data['possible_profiles'].append(f"https://instagram.com/{username}")
                    elif platform == 'linkedin':
                        platform_data['possible_profiles'].append(f"https://linkedin.com/in/{username}")
                    elif platform == 'youtube':
                        platform_data['possible_profiles'].append(f"https://youtube.com/@{username}")
                    elif platform == 'tiktok':
                        platform_data['possible_profiles'].append(f"https://tiktok.com/@{username}")
                    elif platform == 'whatsapp':
                        platform_data['possible_profiles'].append(f"https://wa.me/{username}")
                    elif platform == 'telegram':
                        platform_data['possible_profiles'].append(f"https://t.me/{username}")
            
            platform_results[platform] = platform_data
        
        return platform_results