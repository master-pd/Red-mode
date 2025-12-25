# file: core/analyzer.py
import json
import re
from collections import Counter
from datetime import datetime

class Analyzer:
    """ডাটা অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Data Analyzer"
        
    def analyze_results(self, scan_results):
        """স্ক্যান রেজাল্টস অ্যানালাইসিস"""
        analysis = {
            'summary': self.create_summary(scan_results),
            'contact_info': self.analyze_contacts(scan_results),
            'patterns': self.find_patterns(scan_results),
            'correlations': self.find_correlations(scan_results),
            'risk_assessment': self.assess_risks(scan_results),
            'timeline': self.create_timeline(scan_results)
        }
        
        return analysis
    
    def create_summary(self, results):
        """সারাংশ তৈরি"""
        summary = {
            'total_methods_run': len(results),
            'successful_methods': sum(1 for r in results.values() if r.get('success')),
            'data_points_found': 0,
            'unique_emails': set(),
            'unique_phones': set(),
            'unique_names': set()
        }
        
        # সব ডাটা পয়েন্ট সংগ্রহ
        for method_data in results.values():
            if isinstance(method_data, dict):
                self.extract_data_points(method_data, summary)
        
        summary['unique_emails'] = len(summary['unique_emails'])
        summary['unique_phones'] = len(summary['unique_phones'])
        summary['unique_names'] = len(summary['unique_names'])
        
        return summary
    
    def extract_data_points(self, data, summary):
        """ডাটা পয়েন্ট এক্সট্র্যাক্ট"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['emails', 'email', 'contact_email']:
                    if isinstance(value, list):
                        summary['unique_emails'].update(value)
                    elif isinstance(value, str):
                        summary['unique_emails'].add(value)
                
                elif key in ['phones', 'phone', 'mobile', 'contact_phone']:
                    if isinstance(value, list):
                        summary['unique_phones'].update(value)
                    elif isinstance(value, str):
                        summary['unique_phones'].add(value)
                
                elif key in ['names', 'name', 'full_name', 'username']:
                    if isinstance(value, list):
                        summary['unique_names'].update(value)
                    elif isinstance(value, str):
                        summary['unique_names'].add(value)
                
                elif isinstance(value, (dict, list)):
                    self.extract_data_points(value, summary)
        
        elif isinstance(data, list):
            for item in data:
                self.extract_data_points(item, summary)
    
    def analyze_contacts(self, results):
        """কন্টাক্ট ইনফো অ্যানালাইসিস"""
        contacts = {
            'email_analysis': {},
            'phone_analysis': {},
            'social_media': {}
        }
        
        all_emails = []
        all_phones = []
        all_social = []
        
        # সব কন্টাক্ট সংগ্রহ
        for method_data in results.values():
            if isinstance(method_data, dict):
                contacts_data = self.extract_contacts(method_data)
                all_emails.extend(contacts_data['emails'])
                all_phones.extend(contacts_data['phones'])
                all_social.extend(contacts_data['social'])
        
        # ইমেইল অ্যানালাইসিস
        if all_emails:
            contacts['email_analysis'] = {
                'total': len(all_emails),
                'unique': len(set(all_emails)),
                'providers': self.analyze_email_providers(all_emails),
                'patterns': self.analyze_email_patterns(all_emails)
            }
        
        # ফোন অ্যানালাইসিস
        if all_phones:
            contacts['phone_analysis'] = {
                'total': len(all_phones),
                'unique': len(set(all_phones)),
                'countries': self.analyze_phone_countries(all_phones),
                'carriers': self.analyze_phone_carriers(all_phones)
            }
        
        # সোশ্যাল মিডিয়া
        if all_social:
            contacts['social_media'] = {
                'platforms': Counter([s.split('/')[0] for s in all_social]),
                'links': list(set(all_social))
            }
        
        return contacts
    
    def extract_contacts(self, data):
        """কন্টাক্ট ডাটা এক্সট্র্যাক্ট"""
        contacts = {
            'emails': [],
            'phones': [],
            'social': []
        }
        
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'emails' and isinstance(value, list):
                    contacts['emails'].extend(value)
                elif key == 'phones' and isinstance(value, list):
                    contacts['phones'].extend(value)
                elif key == 'social_links' and isinstance(value, dict):
                    for platform, links in value.items():
                        contacts['social'].extend(links)
                elif isinstance(value, (dict, list)):
                    sub_contacts = self.extract_contacts(value)
                    contacts['emails'].extend(sub_contacts['emails'])
                    contacts['phones'].extend(sub_contacts['phones'])
                    contacts['social'].extend(sub_contacts['social'])
        
        return contacts
    
    def analyze_email_providers(self, emails):
        """ইমেইল প্রোভাইডার অ্যানালাইসিস"""
        providers = {}
        
        for email in emails:
            if '@' in email:
                provider = email.split('@')[1].lower()
                providers[provider] = providers.get(provider, 0) + 1
        
        return dict(sorted(providers.items(), key=lambda x: x[1], reverse=True))
    
    def analyze_email_patterns(self, emails):
        """ইমেইল প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'name_based': 0,
            'random': 0,
            'number_suffix': 0,
            'dot_separated': 0
        }
        
        for email in emails:
            if '@' in email:
                username = email.split('@')[0]
                
                # নাম বেসড
                if any(char.isalpha() for char in username):
                    patterns['name_based'] += 1
                
                # র্যান্ডম
                if re.match(r'^[a-z0-9]{8,}$', username):
                    patterns['random'] += 1
                
                # নাম্বার suffix
                if re.match(r'^[a-z]+[0-9]+$', username):
                    patterns['number_suffix'] += 1
                
                # ডট separated
                if '.' in username:
                    patterns['dot_separated'] += 1
        
        return patterns
    
    def analyze_phone_countries(self, phones):
        """ফোন নম্বর দেশ অনুযায়ী"""
        countries = {}
        
        for phone in phones:
            # বাংলাদেশী ফোন
            if phone.startswith('01') or '8801' in phone:
                countries['Bangladesh'] = countries.get('Bangladesh', 0) + 1
            # US ফোন
            elif phone.startswith('+1') or phone.startswith('1'):
                countries['USA'] = countries.get('USA', 0) + 1
            # UK ফোন
            elif phone.startswith('+44'):
                countries['UK'] = countries.get('UK', 0) + 1
            # ভারত
            elif phone.startswith('+91'):
                countries['India'] = countries.get('India', 0) + 1
        
        return countries
    
    def analyze_phone_carriers(self, phones):
        """ফোন ক্যারিয়ার অ্যানালাইসিস (বাংলাদেশ)"""
        bd_carriers = {
            'Grameenphone': ['013', '017'],
            'Robi': ['016', '018'],
            'Banglalink': ['014', '019'],
            'Teletalk': ['015'],
            'Airtel': ['016']
        }
        
        carriers = {}
        
        for phone in phones:
            phone_str = str(phone)
            for carrier, prefixes in bd_carriers.items():
                for prefix in prefixes:
                    if phone_str.startswith(prefix) or phone_str.endswith(prefix):
                        carriers[carrier] = carriers.get(carrier, 0) + 1
                        break
        
        return carriers
    
    def find_patterns(self, results):
        """ডাটা প্যাটার্ন খোঁজা"""
        patterns = {
            'repeated_data': [],
            'data_clusters': [],
            'time_patterns': [],
            'location_patterns': []
        }
        
        # সব টেক্সট ডাটা সংগ্রহ
        all_text = self.extract_all_text(results)
        
        # প্যাটার্ন খোঁজা
        patterns['repeated_data'] = self.find_repeated_data(all_text)
        
        return patterns
    
    def extract_all_text(self, data):
        """সব টেক্সট ডাটা সংগ্রহ"""
        texts = []
        
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, str):
                    texts.append(value)
                elif isinstance(value, (dict, list)):
                    texts.extend(self.extract_all_text(value))
        elif isinstance(data, list):
            for item in data:
                texts.extend(self.extract_all_text(item))
        
        return texts
    
    def find_repeated_data(self, texts):
        """রিপিটেড ডাটা খোঁজা"""
        # Common phrases or patterns
        common_phrases = []
        
        # শব্দ frequency
        all_words = []
        for text in texts:
            if isinstance(text, str):
                words = re.findall(r'\b\w{3,}\b', text.lower())
                all_words.extend(words)
        
        word_counts = Counter(all_words)
        
        # Common words (non-stop words)
        stop_words = {'the', 'and', 'for', 'you', 'are', 'this', 'that', 'with'}
        common_words = [(word, count) for word, count in word_counts.items() 
                       if count > 3 and word not in stop_words]
        
        return sorted(common_words, key=lambda x: x[1], reverse=True)[:10]
    
    def find_correlations(self, results):
        """ডাটা correlations খোঁজা"""
        correlations = {
            'email_phone_pairs': [],
            'name_email_matches': [],
            'social_media_correlations': []
        }
        
        return correlations
    
    def assess_risks(self, results):
        """রিস্ক অ্যাসেসমেন্ট"""
        risks = {
            'privacy_exposure': 'low',
            'data_breach_risk': 'low',
            'social_engineering_risk': 'medium',
            'recommendations': []
        }
        
        # Check for sensitive data
        sensitive_patterns = [
            r'\b\d{16}\b',  # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'password\s*[:=]\s*\S+',  # Password
            r'token\s*[:=]\s*\S+',  # Token
            r'secret\s*[:=]\s*\S+'  # Secret
        ]
        
        all_text = ' '.join(self.extract_all_text(results))
        
        for pattern in sensitive_patterns:
            if re.search(pattern, all_text, re.IGNORECASE):
                risks['privacy_exposure'] = 'high'
                risks['recommendations'].append('Sensitive data found!')
                break
        
        return risks
    
    def create_timeline(self, results):
        """টাইমলাইন তৈরি"""
        timeline = []
        
        # Extract dates from data
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{2}/\d{2}/\d{4}\b',
            r'\b\d{2}-\d{2}-\d{4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        ]
        
        for method_name, method_data in results.items():
            if isinstance(method_data, dict):
                text_data = json.dumps(method_data)
                
                for pattern in date_patterns:
                    dates = re.findall(pattern, text_data, re.IGNORECASE)
                    for date_str in dates:
                        try:
                            # Try to parse date
                            timeline.append({
                                'method': method_name,
                                'date': date_str,
                                'type': 'data_point'
                            })
                        except:
                            pass
        
        return timeline