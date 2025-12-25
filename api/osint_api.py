# file: api/osint_api.py
import requests
import json
import re
from typing import Dict, List, Optional

class OSINTAPI:
    """OSINT API Integration"""
    
    def __init__(self, api_keys=None):
        self.api_keys = api_keys or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # API endpoints
        self.apis = {
            'hunter': 'https://api.hunter.io/v2',
            'phonebook': 'https://phonebook.cz/api/v1',
            'shodan': 'https://api.shodan.io',
            'censys': 'https://search.censys.io/api/v2',
            'fullcontact': 'https://api.fullcontact.com/v3'
        }
    
    def hunter_email_finder(self, domain, api_key=None):
        """Hunter.io Email Finder"""
        key = api_key or self.api_keys.get('hunter')
        if not key:
            return {'error': 'Hunter.io API key required'}
        
        params = {
            'domain': domain,
            'api_key': key,
            'limit': 100
        }
        
        try:
            response = self.session.get(
                f"{self.apis['hunter']}/domain-search",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'domain': domain,
                    'total_emails': data.get('data', {}).get('total', 0),
                    'emails': data.get('data', {}).get('emails', [])[:20],
                    'pattern': data.get('data', {}).get('pattern', '')
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def phonebook_search(self, query, search_type='email', api_key=None):
        """Phonebook.cz Search"""
        key = api_key or self.api_keys.get('phonebook')
        
        params = {
            'query': query,
            'type': search_type
        }
        
        if key:
            params['api_key'] = key
        
        try:
            response = self.session.get(
                f"{self.apis['phonebook']}/search",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'query': query,
                    'type': search_type,
                    'total_results': len(data.get('results', [])),
                    'results': data.get('results', [])[:20],
                    'has_more': data.get('has_more', False)
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def shodan_host_search(self, ip_or_domain, api_key=None):
        """Shodan Host Search"""
        key = api_key or self.api_keys.get('shodan')
        if not key:
            return {'error': 'Shodan API key required'}
        
        params = {'key': key}
        
        try:
            response = self.session.get(
                f"{self.apis['shodan']}/shodan/host/{ip_or_domain}",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'target': ip_or_domain,
                    'ip': data.get('ip_str', ''),
                    'ports': data.get('ports', []),
                    'vulns': data.get('vulns', []),
                    'domains': data.get('domains', []),
                    'hostnames': data.get('hostnames', []),
                    'os': data.get('os', ''),
                    'data': data.get('data', [])[:5]
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def censys_search(self, query, search_type='websites', api_key=None):
        """Censys Search"""
        key = api_key or self.api_keys.get('censys')
        if not key:
            return {'error': 'Censys API key required'}
        
        headers = {
            'Authorization': f'Basic {key}',
            'Accept': 'application/json'
        }
        
        params = {
            'q': query,
            'per_page': 50
        }
        
        try:
            response = self.session.get(
                f"{self.apis['censys']}/{search_type}/search",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'query': query,
                    'type': search_type,
                    'total_results': data.get('result', {}).get('total', 0),
                    'hits': data.get('result', {}).get('hits', [])[:10],
                    'query_time': data.get('result', {}).get('took', 0)
                }
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def fullcontact_person_enrich(self, email, api_key=None):
        """FullContact Person Enrichment"""
        key = api_key or self.api_keys.get('fullcontact')
        if not key:
            return {'error': 'FullContact API key required'}
        
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        
        payload = {'email': email}
        
        try:
            response = self.session.post(
                f"{self.apis['fullcontact']}/person.enrich",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'email': email,
                    'full_name': data.get('fullName', ''),
                    'age_range': data.get('ageRange', ''),
                    'gender': data.get('gender', ''),
                    'location': data.get('location', ''),
                    'title': data.get('title', ''),
                    'organizations': data.get('organizations', []),
                    'photos': data.get('photos', [])[:5],
                    'social_profiles': data.get('socialProfiles', [])[:10]
                }
            elif response.status_code == 202:
                return {'status': 'processing', 'email': email, 'message': 'Data is being processed'}
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'response': response.text[:200]
                }
                
        except Exception as e:
            return {'error': str(e)}
    
    def sherlock_username_search(self, username):
        """Sherlock-style Username Search"""
        # Common social media platforms
        platforms = [
            {
                'name': 'Facebook',
                'url': f'https://www.facebook.com/{username}',
                'check_url': f'https://www.facebook.com/{username}'
            },
            {
                'name': 'Twitter',
                'url': f'https://twitter.com/{username}',
                'check_url': f'https://twitter.com/{username}'
            },
            {
                'name': 'Instagram',
                'url': f'https://www.instagram.com/{username}',
                'check_url': f'https://www.instagram.com/{username}/?__a=1'
            },
            {
                'name': 'LinkedIn',
                'url': f'https://www.linkedin.com/in/{username}',
                'check_url': f'https://www.linkedin.com/in/{username}'
            },
            {
                'name': 'GitHub',
                'url': f'https://github.com/{username}',
                'check_url': f'https://api.github.com/users/{username}'
            },
            {
                'name': 'YouTube',
                'url': f'https://www.youtube.com/@{username}',
                'check_url': f'https://www.youtube.com/@{username}'
            },
            {
                'name': 'TikTok',
                'url': f'https://www.tiktok.com/@{username}',
                'check_url': f'https://www.tiktok.com/@{username}'
            },
            {
                'name': 'Pinterest',
                'url': f'https://www.pinterest.com/{username}',
                'check_url': f'https://www.pinterest.com/{username}'
            }
        ]
        
        results = []
        
        for platform in platforms:
            try:
                response = self.session.get(
                    platform['check_url'],
                    timeout=10,
                    allow_redirects=True
                )
                
                exists = False
                if response.status_code == 200:
                    # Basic check for existence
                    if response.url != 'https://www.facebook.com/' and 'login' not in response.url:
                        exists = True
                
                results.append({
                    'platform': platform['name'],
                    'url': platform['url'],
                    'exists': exists,
                    'status_code': response.status_code,
                    'final_url': response.url
                })
                
            except Exception as e:
                results.append({
                    'platform': platform['name'],
                    'url': platform['url'],
                    'exists': False,
                    'error': str(e)
                })
        
        return {
            'username': username,
            'total_platforms': len(platforms),
            'found_on': len([r for r in results if r.get('exists', False)]),
            'results': results
        }
    
    def epieos_tool_check(self, email):
        """Epieos Tool Check (Simulated)"""
        # Note: Epieos.com is a real OSINT tool, but this is a simulation
        simulated_results = {
            'email': email,
            'checks_performed': [
                'Google Account Check',
                'Microsoft Account Check',
                'Social Media Presence',
                'Data Breach Check',
                'Professional Networks'
            ],
            'findings': {
                'google_account': True,
                'microsoft_account': False,
                'social_media_presence': True,
                'data_breaches': 2,
                'professional_networks': ['LinkedIn', 'GitHub']
            },
            'associated_accounts': [
                f'{email.split("@")[0]}@gmail.com',
                f'{email.split("@")[0]}@yahoo.com'
            ],
            'note': 'Simulated results for educational purposes. Real Epieos.com requires manual checking.'
        }
        
        return simulated_results
    
    def maigret_social_search(self, username):
        """Maigret-style Social Media Search"""
        # Extended list of social media platforms
        social_platforms = [
            # Social Networks
            ('Facebook', f'https://facebook.com/{username}'),
            ('Twitter', f'https://twitter.com/{username}'),
            ('Instagram', f'https://instagram.com/{username}'),
            ('LinkedIn', f'https://linkedin.com/in/{username}'),
            
            # Media Sharing
            ('YouTube', f'https://youtube.com/@{username}'),
            ('TikTok', f'https://tiktok.com/@{username}'),
            ('Pinterest', f'https://pinterest.com/{username}'),
            ('Flickr', f'https://flickr.com/people/{username}'),
            
            # Professional
            ('GitHub', f'https://github.com/{username}'),
            ('GitLab', f'https://gitlab.com/{username}'),
            ('StackOverflow', f'https://stackoverflow.com/users/{username}'),
            
            # Blogs & Forums
            ('WordPress', f'https://{username}.wordpress.com'),
            ('Blogger', f'https://{username}.blogspot.com'),
            ('Medium', f'https://medium.com/@{username}'),
            ('Reddit', f'https://reddit.com/user/{username}'),
            
            # Other
            ('Telegram', f'https://t.me/{username}'),
            ('Keybase', f'https://keybase.io/{username}'),
            ('About.me', f'https://about.me/{username}'),
            ('DeviantArt', f'https://deviantart.com/{username}')
        ]
        
        results = []
        
        for platform_name, url in social_platforms[:10]:  # Check first 10
            try:
                response = self.session.head(url, timeout=5, allow_redirects=True)
                
                exists = False
                reason = ''
                
                if response.status_code == 200:
                    exists = True
                    reason = 'HTTP 200 OK'
                elif response.status_code == 404:
                    exists = False
                    reason = 'HTTP 404 Not Found'
                else:
                    # Might exist but have different response
                    exists = True if response.status_code != 404 else False
                    reason = f'HTTP {response.status_code}'
                
                results.append({
                    'platform': platform_name,
                    'url': url,
                    'exists': exists,
                    'status_code': response.status_code,
                    'reason': reason,
                    'response_time': response.elapsed.total_seconds()
                })
                
            except Exception as e:
                results.append({
                    'platform': platform_name,
                    'url': url,
                    'exists': False,
                    'error': str(e)[:100]
                })
        
        # Analyze results
        found_platforms = [r['platform'] for r in results if r.get('exists', False)]
        not_found = [r['platform'] for r in results if not r.get('exists', False)]
        
        return {
            'username': username,
            'total_checked': len(social_platforms[:10]),
            'found_on': len(found_platforms),
            'found_platforms': found_platforms,
            'not_found_platforms': not_found,
            'detailed_results': results,
            'profile_confidence': f'{len(found_platforms)/10*100:.1f}%'
        }
    
    def generate_osint_report(self, target, target_type='email'):
        """OSINT রিপোর্ট জেনারেট"""
        report = {
            'target': target,
            'target_type': target_type,
            'execution_time': '',
            'findings': {},
            'summary': {},
            'recommendations': []
        }
        
        findings = {}
        
        if target_type == 'email':
            # Email-based OSINT
            findings['email_analysis'] = self.hunter_email_finder(target.split('@')[1])
            findings['breach_check'] = {'simulated': True, 'breaches_found': 2}
            findings['person_enrichment'] = self.fullcontact_person_enrich(target)
            
            # Username extraction
            username = target.split('@')[0]
            findings['username_search'] = self.sherlock_username_search(username)
            findings['social_search'] = self.maigret_social_search(username)
        
        elif target_type == 'username':
            # Username-based OSINT
            findings['social_search'] = self.maigret_social_search(target)
            findings['username_search'] = self.sherlock_username_search(target)
        
        elif target_type == 'domain':
            # Domain-based OSINT
            findings['email_finder'] = self.hunter_email_finder(target)
            findings['shodan_search'] = self.shodan_host_search(target)
        
        elif target_type == 'phone':
            # Phone-based OSINT
            findings['phonebook_search'] = self.phonebook_search(target, 'phone')
        
        # Summary
        total_findings = 0
        for key, value in findings.items():
            if value and not isinstance(value, dict) or 'error' not in value:
                total_findings += 1
        
        report['findings'] = findings
        report['summary'] = {
            'total_checks_performed': len(findings),
            'successful_checks': total_findings,
            'confidence_level': f'{(total_findings/len(findings))*100:.1f}%' if findings else '0%'
        }
        
        # Recommendations
        if target_type == 'email':
            report['recommendations'] = [
                'Verify email deliverability',
                'Check for data breaches',
                'Look for associated social media accounts',
                'Search for leaked credentials'
            ]
        elif target_type == 'username':
            report['recommendations'] = [
                'Check all major social media platforms',
                'Look for professional profiles',
                'Search for content posted by this username',
                'Check for associated email addresses'
            ]
        
        return report