# file: method_05_osint.py
import requests
import json
import re
from typing import Dict, List

class OSINTScanner:
    """Public OSINT Information Scanner"""
    
    def __init__(self):
        self.name = "OSINT Public Data Scanner"
        self.osint_sources = {
            'hunter': 'https://api.hunter.io/v2/email-finder',
            'phonebook': 'https://phonebook.cz/api/v1/search',
            'haveibeenpwned': 'https://haveibeenpwned.com/api/v3/breachedaccount/',
            'dehashed': 'https://api.dehashed.com/search'
        }
    
    def execute(self, target):
        """OSINT স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            osint_data = {}
            
            # বিভিন্ন OSINT টেস্ট
            osint_data['email_search'] = self.search_emails(target)
            osint_data['username_search'] = self.search_usernames(target)
            osint_data['breach_check'] = self.check_breaches(target)
            osint_data['social_media'] = self.find_social_media(target)
            osint_data['public_records'] = self.search_public_records(target)
            
            results['data'] = osint_data
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def search_emails(self, target):
        """ইমেইল সার্চ"""
        emails = []
        
        # প্যাটার্ন ম্যাচিং
        patterns = [
            rf'{target}@gmail\.com',
            rf'{target}@yahoo\.com',
            rf'{target}@hotmail\.com',
            rf'{target}@outlook\.com',
            r'[\w\.-]+@[\w\.-]+\.\w+'
        ]
        
        # কয়েকটা common combination
        name_parts = re.split(r'[\._\-\s]+', target)
        if len(name_parts) >= 2:
            first, last = name_parts[0], name_parts[-1]
            common_emails = [
                f"{first}.{last}@gmail.com",
                f"{first}{last}@gmail.com",
                f"{first[0]}{last}@gmail.com",
                f"{first}_{last}@gmail.com"
            ]
            emails.extend(common_emails)
        
        return emails
    
    def search_usernames(self, target):
        """ইউজারনেম সার্চ"""
        # Common platforms
        platforms = [
            'github.com/{}',
            'twitter.com/{}',
            'instagram.com/{}',
            'linkedin.com/in/{}',
            'facebook.com/{}',
            'tiktok.com/@{}',
            'youtube.com/@{}'
        ]
        
        profiles = []
        for platform in platforms:
            profiles.append(platform.format(target))
        
        return profiles
    
    def check_breaches(self, target):
        """ব্রিচ চেক (শিক্ষামূলক)"""
        # Note: Real API calls require API keys
        breach_info = {
            'haveibeenpwned': 'API key required',
            'dehashed': 'API key required',
            'breachdirectory': 'API key required'
        }
        
        # স্থানীয় প্যাটার্ন ম্যাচিং
        local_patterns = [
            r'breach.*?' + re.escape(target),
            r'leak.*?' + re.escape(target),
            r'password.*?' + re.escape(target)
        ]
        
        return {
            'api_status': 'Requires authentication',
            'local_check': 'Implemented',
            'patterns': local_patterns
        }
    
    def find_social_media(self, target):
        """সোশ্যাল মিডিয়া খোঁজা"""
        social_links = {}
        
        # সাধারণ প্যাটার্ন
        common_patterns = {
            'facebook': [
                f'https://facebook.com/{target}',
                f'https://fb.com/{target}',
                f'https://www.facebook.com/{target}'
            ],
            'twitter': [
                f'https://twitter.com/{target}',
                f'https://x.com/{target}'
            ],
            'instagram': [
                f'https://instagram.com/{target}',
                f'https://www.instagram.com/{target}'
            ],
            'linkedin': [
                f'https://linkedin.com/in/{target}',
                f'https://www.linkedin.com/in/{target}'
            ]
        }
        
        for platform, links in common_patterns.items():
            social_links[platform] = links
        
        return social_links
    
    def search_public_records(self, target):
        """পাবলিক রেকর্ডস (শিক্ষামূলক)"""
        # এইটা শুধুমাত্র শিক্ষামূলক, রিয়েল API নয়
        return {
            'note': 'Real public record searches require paid APIs',
            'suggested_apis': [
                'whitepages.com',
                'beenverified.com',
                'truthfinder.com',
                'instantcheckmate.com'
            ]
        }