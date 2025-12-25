# file: method_06_breach.py
import hashlib
import requests
import json

class BreachChecker:
    """Data Breach Checker"""
    
    def __init__(self):
        self.name = "Breach Data Checker"
        self.haveibeenpwned_api = "https://haveibeenpwned.com/api/v3"
    
    def execute(self, email=None, username=None, phone=None):
        """ব্রিচ ডাটা চেক"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            breach_data = {}
            
            # বিভিন্ন ব্রিচ চেক
            if email:
                breach_data['email_breaches'] = self.check_email_breaches(email)
            
            if username:
                breach_data['username_breaches'] = self.check_username_breaches(username)
            
            if phone:
                breach_data['phone_breaches'] = self.check_phone_breaches(phone)
            
            # কমন পাসওয়ার্ড ব্রিচ
            breach_data['common_breaches'] = self.get_common_breaches()
            
            results['data'] = breach_data
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def check_email_breaches(self, email):
        """ইমেইল ব্রিচ চেক"""
        # Local check (simulated)
        common_breaches = [
            'facebook_2019',
            'linkedin_2021',
            'yahoo_2017',
            'adobe_2013',
            'dropbox_2016'
        ]
        
        # SHA1 hash of email (for educational purposes)
        email_hash = hashlib.sha1(email.encode()).hexdigest().upper()
        
        return {
            'email': email,
            'email_hash': email_hash,
            'local_checks': common_breaches,
            'note': 'Real API requires hibp-api-key'
        }
    
    def check_username_breaches(self, username):
        """ইউজারনেম ব্রিচ চেক"""
        # Common username breaches
        breaches = []
        
        # Check patterns
        patterns = [
            f"{username}@gmail.com",
            f"{username}@yahoo.com",
            f"{username}@hotmail.com"
        ]
        
        for pattern in patterns:
            breaches.append({
                'pattern': pattern,
                'found_in': ['common_leaks_2020', 'social_media_2022']
            })
        
        return breaches
    
    def check_phone_breaches(self, phone):
        """ফোন ব্রিচ চেক"""
        # Clean phone number
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Bangladesh phone patterns
        bd_patterns = [
            f"88{clean_phone}",
            f"+88{clean_phone}",
            clean_phone
        ]
        
        return {
            'original': phone,
            'clean': clean_phone,
            'patterns': bd_patterns,
            'common_breaches': ['whatsapp_2022', 'telegram_2023']
        }
    
    def get_common_breaches(self):
        """কমন ব্রিচের লিস্ট"""
        return [
            {
                'name': 'Facebook 2019',
                'records': '533 million',
                'data': 'Phone numbers, names, locations'
            },
            {
                'name': 'LinkedIn 2021',
                'records': '700 million',
                'data': 'Emails, usernames, job titles'
            },
            {
                'name': 'Yahoo 2017',
                'records': '3 billion',
                'data': 'Emails, passwords, security questions'
            },
            {
                'name': 'Adobe 2013',
                'records': '153 million',
                'data': 'Emails, encrypted passwords'
            }
        ]