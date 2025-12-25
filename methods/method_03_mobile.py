# file: method_03_mobile.py
import requests
import re
from urllib.parse import urlparse, urljoin

class MobileSiteScanner:
    """Mobile Facebook Site Scanner"""
    
    def __init__(self):
        self.name = "Mobile Site Scanner"
        self.mobile_urls = {
            'm.facebook.com': 'https://m.facebook.com/{}',
            'mbasic.facebook.com': 'https://mbasic.facebook.com/{}',
            'touch.facebook.com': 'https://touch.facebook.com/{}'
        }
    
    def execute(self, username_or_id):
        """মোবাইল সাইট স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            all_data = {}
            
            for site_name, url_template in self.mobile_urls.items():
                try:
                    url = url_template.format(username_or_id)
                    site_data = self.scan_mobile_site(url, site_name)
                    if site_data:
                        all_data[site_name] = site_data
                except Exception as e:
                    results['errors'].append(f"{site_name}: {str(e)}")
            
            if all_data:
                results['data'] = all_data
                results['success'] = True
                
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def scan_mobile_site(self, url, site_name):
        """ইনডিভিজুয়াল মোবাইল সাইট স্ক্যান"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                html = response.text
                
                # মোবাইল সাইট থেকে বিশেষ তথ্য
                mobile_data = {
                    'url': url,
                    'site': site_name,
                    'title': self.extract_title(html),
                    'profile_exists': self.check_profile_exists(html),
                    'contact_info': self.extract_mobile_contacts(html),
                    'about_section': self.extract_about_section(html),
                    'friends_count': self.extract_friends_count(html),
                    'photos_count': self.extract_photos_count(html),
                    'raw_html_length': len(html)
                }
                
                return mobile_data
                
        except Exception as e:
            return {'error': str(e)}
        
        return None
    
    def extract_title(self, html):
        """মোবাইল সাইট টাইটেল"""
        match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1) if match else None
    
    def check_profile_exists(self, html):
        """প্রোফাইল আছে কি না চেক"""
        not_found_patterns = [
            r'sorry.*?page.*?found',
            r'not.*?found',
            r'does.*?not.*?exist',
            r'content.*?unavailable'
        ]
        
        html_lower = html.lower()
        for pattern in not_found_patterns:
            if re.search(pattern, html_lower):
                return False
        
        return True if 'profile' in html_lower or 'timeline' in html_lower else False
    
    def extract_mobile_contacts(self, html):
        """মোবাইল সাইট থেকে কন্টাক্ট"""
        contacts = {
            'phones': [],
            'emails': []
        }
        
        # মোবাইল সাইটে সাধারণত কন্টাক্ট বেশি থাকে
        phone_patterns = [
            r'01[3-9]\d{8}',
            r'8801[3-9]\d{8}',
            r'tel:(\+\d+)',
            r'phone.*?(\d{10,15})',
            r'mobile.*?(\d{10,15})'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                phone = re.sub(r'[^\d\+]', '', str(match))
                if 10 <= len(phone) <= 15 and phone not in contacts['phones']:
                    contacts['phones'].append(phone)
        
        # ইমেইল
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        emails = re.findall(email_pattern, html)
        contacts['emails'] = list(set(emails))
        
        return contacts
    
    def extract_about_section(self, html):
        """About সেকশন"""
        about_data = {}
        
        # মোবাইল about প্যাটার্ন
        patterns = {
            'work': r'work.*?>([^<]+)<',
            'education': r'education.*?>([^<]+)<',
            'location': r'location.*?>([^<]+)<',
            'hometown': r'hometown.*?>([^<]+)<',
            'relationship': r'relationship.*?>([^<]+)<'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                about_data[key] = match.group(1).strip()
        
        return about_data
    
    def extract_friends_count(self, html):
        """ফ্রেন্ডস কাউন্ট"""
        patterns = [
            r'friends.*?(\d+[,]?\d*)',
            r'(\d+[,]?\d*)\s*friends',
            r'friend.*?count.*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def extract_photos_count(self, html):
        """ফটোস কাউন্ট"""
        patterns = [
            r'photos.*?(\d+[,]?\d*)',
            r'(\d+[,]?\d*)\s*photos',
            r'photo.*?count.*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None