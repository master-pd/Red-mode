# file: api/breach_api.py
import requests
import hashlib
import json
import time
from typing import Dict, List, Optional

class BreachAPI:
    """ব্রিচ ডাটা API"""
    
    def __init__(self, api_key=None):
        self.haveibeenpwned_api = "https://haveibeenpwned.com/api/v3"
        self.dehashed_api = "https://api.dehashed.com"
        self.breachdirectory_api = "https://breachdirectory.p.rapidapi.com/"
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MAR-PD-Breach-Scanner/1.0'
        })
    
    def set_api_key(self, api_key):
        """API key সেট"""
        self.api_key = api_key
        
    def check_email_breach(self, email):
        """ইমেইল ব্রিচ চেক"""
        if not self.api_key:
            return {'error': 'API key required for HIBP'}
        
        headers = {
            'hibp-api-key': self.api_key,
            'User-Agent': 'MAR-PD-Scanner'
        }
        
        try:
            response = self.session.get(
                f"{self.haveibeenpwned_api}/breachedaccount/{email}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    'email': email,
                    'breached': True,
                    'breach_count': len(breaches),
                    'breaches': breaches[:10]  # First 10 breaches
                }
            elif response.status_code == 404:
                return {
                    'email': email,
                    'breached': False,
                    'message': 'No breaches found'
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_password_breach(self, password):
        """পাসওয়ার্ড ব্রিচ চেক"""
        # SHA1 hash of password
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]
        
        try:
            response = self.session.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                timeout=30
            )
            
            if response.status_code == 200:
                hashes = response.text.split('\n')
                for line in hashes:
                    hash_suffix, count = line.split(':')
                    if hash_suffix == suffix:
                        return {
                            'password': '***' + password[-3:] if len(password) > 3 else '***',
                            'breached': True,
                            'breach_count': int(count.strip()),
                            'hash': sha1_hash
                        }
                
                return {
                    'password': '***' + password[-3:] if len(password) > 3 else '***',
                    'breached': False,
                    'message': 'Password not found in breaches'
                }
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_username_breach(self, username):
        """ইউজারনেম ব্রিচ চেক"""
        # Check common breach databases
        common_breaches = [
            {
                'name': 'Facebook 2019',
                'records': '533 million',
                'contains': ['phone numbers', 'names', 'locations']
            },
            {
                'name': 'LinkedIn 2021',
                'records': '700 million',
                'contains': ['emails', 'usernames', 'job titles']
            },
            {
                'name': 'Twitter 2022',
                'records': '5.4 million',
                'contains': ['emails', 'usernames']
            }
        ]
        
        # Simulate check (in real implementation, would query actual APIs)
        simulated_results = []
        
        # Check if username appears in common patterns
        username_lower = username.lower()
        common_patterns = [
            f"{username_lower}@gmail.com",
            f"{username_lower}@yahoo.com",
            f"{username_lower}@hotmail.com",
            f"{username_lower}123",
            f"{username_lower}2020"
        ]
        
        for breach in common_breaches:
            # In real implementation, would check against actual data
            # This is simulated for educational purposes
            simulated_results.append({
                'breach_name': breach['name'],
                'records': breach['records'],
                'data_types': breach['contains'],
                'username_found': True  # Simulated
            })
        
        return {
            'username': username,
            'simulated_check': True,
            'breaches_found': simulated_results,
            'common_patterns': common_patterns,
            'note': 'Simulated results for educational purposes'
        }
    
    def check_phone_breach(self, phone_number):
        """ফোন নম্বর ব্রিচ চেক"""
        # Clean phone number
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        # Bangladesh phone format
        bd_formats = []
        if len(clean_phone) == 11 and clean_phone.startswith('01'):
            bd_formats = [
                clean_phone,  # 01712345678
                f"88{clean_phone}",  # 8801712345678
                f"+88{clean_phone}"  # +8801712345678
            ]
        
        # Common phone breaches
        common_breaches = [
            {
                'name': 'WhatsApp 2022',
                'records': '487 million',
                'contains': ['phone numbers', 'account data']
            },
            {
                'name': 'Facebook 2019',
                'records': '533 million',
                'contains': ['phone numbers', 'names']
            },
            {
                'name': 'Truecaller 2019',
                'records': '47 million',
                'contains': ['phone numbers', 'names', 'locations']
            }
        ]
        
        simulated_results = []
        for breach in common_breaches:
            simulated_results.append({
                'breach_name': breach['name'],
                'records': breach['records'],
                'data_types': breach['contains'],
                'phone_found': len(bd_formats) > 0  # Simulated
            })
        
        return {
            'original_phone': phone_number,
            'clean_phone': clean_phone,
            'bd_formats': bd_formats,
            'simulated_check': True,
            'breaches_found': simulated_results,
            'note': 'Simulated results for educational purposes'
        }
    
    def search_dehashed(self, query, search_type='email'):
        """Dehashed API সার্চ"""
        if not self.api_key:
            return {'error': 'Dehashed API key required'}
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {self.api_key}'
        }
        
        params = {
            'query': f'{search_type}:"{query}"',
            'size': 100
        }
        
        try:
            response = self.session.get(
                f"{self.dehashed_api}/search",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'query': query,
                    'type': search_type,
                    'total': data.get('total', 0),
                    'entries': data.get('entries', [])[:10],
                    'balance': data.get('balance', 0)
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def check_multiple_emails(self, emails):
        """একাধিক ইমেইল ব্রিচ চেক"""
        results = []
        
        for email in emails[:10]:  # Limit to 10 emails
            result = self.check_email_breach(email)
            results.append({
                'email': email,
                'result': result
            })
            time.sleep(1)  # Rate limiting
        
        summary = {
            'total_emails': len(emails),
            'checked': len(results),
            'breached_count': sum(1 for r in results if r['result'].get('breached', False)),
            'results': results
        }
        
        return summary
    
    def get_breach_statistics(self):
        """ব্রিচ স্ট্যাটিসটিক্স"""
        stats = {
            'total_breaches': 0,
            'total_records': 0,
            'latest_breaches': [],
            'common_data_types': []
        }
        
        # Latest known breaches (simulated)
        latest_breaches = [
            {
                'name': 'Facebook 2019',
                'date': 'April 2019',
                'records': '533 million',
                'data': 'Phone numbers, names, locations'
            },
            {
                'name': 'LinkedIn 2021',
                'date': 'June 2021',
                'records': '700 million',
                'data': 'Emails, usernames, job titles'
            },
            {
                'name': 'Twitter 2022',
                'date': 'July 2022',
                'records': '5.4 million',
                'data': 'Emails, usernames'
            },
            {
                'name': 'WhatsApp 2022',
                'date': 'November 2022',
                'records': '487 million',
                'data': 'Phone numbers, account data'
            }
        ]
        
        stats['latest_breaches'] = latest_breaches
        stats['total_breaches'] = len(latest_breaches)
        
        # Common data types in breaches
        common_data_types = [
            {'type': 'Email addresses', 'percentage': 95},
            {'type': 'Passwords', 'percentage': 85},
            {'type': 'Phone numbers', 'percentage': 60},
            {'type': 'Names', 'percentage': 75},
            {'type': 'Physical addresses', 'percentage': 40},
            {'type': 'Credit card info', 'percentage': 25}
        ]
        
        stats['common_data_types'] = common_data_types
        
        return stats
    
    def generate_breach_report(self, email):
        """ব্রিচ রিপোর্ট জেনারেট"""
        email_result = self.check_email_breach(email)
        password_result = self.check_password_breach("dummy_password")  # Placeholder
        
        report = {
            'email': email,
            'email_breach_status': email_result,
            'password_security': password_result,
            'recommendations': [],
            'security_score': 0
        }
        
        # Generate recommendations
        if email_result.get('breached', False):
            report['recommendations'].append('Change password for breached accounts')
            report['recommendations'].append('Enable two-factor authentication')
            report['recommendations'].append('Use unique passwords for each site')
            report['security_score'] = 30
        else:
            report['recommendations'].append('Monitor accounts regularly')
            report['recommendations'].append('Use strong, unique passwords')
            report['security_score'] = 80
        
        if password_result.get('breached', False):
            report['recommendations'].append('Immediately change this password')
            report['security_score'] = max(0, report['security_score'] - 40)
        
        return report