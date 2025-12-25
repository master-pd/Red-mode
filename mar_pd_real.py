# file: mar_pd_real.py
import os
import sys
import json
import requests
import hashlib
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, quote
import random

class MARPD_Core:
    """Real MAR-PD Core Engine"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.proxies = None
        self.timeout = 30
        self.results = {}
        
    def extract_phones_from_html(self, html):
        """HTML থেকে ফোন নম্বর বের করে"""
        patterns = [
            r'\b01[3-9]\d{8}\b',  # bd number 
            r'\b8801[3-9]\d{8}\b',  # 880 required 
            r'\+\d{1,3}[-.\s]?\d{1,14}',  # national 
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
            r'tel:([+0-9\s\-]+)',  # tel: url
            r'phone["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',  # JSON phone 
            r'contact["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',
            r'mobile["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',
            r'phone.*?(\d{10,15})',
        ]
        
        phones = set()
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # ক্লিন করা
                phone = re.sub(r'[^\d\+]', '', str(match))
                if len(phone) >= 10:
                    phones.add(phone)
                    
        return list(phones)
    
    def extract_emails_from_html(self, html):
        """HTML থেকে ইমেইল বের করে"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        
        # অতিরিক্ত প্যাটার্ন
        extra_patterns = [
            r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'email["\']?\s*:\s*["\']?([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})["\']?',
            r'contact["\']?\s*:\s*["\']?([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})["\']?',
        ]
        
        all_emails = set(emails)
        for pattern in extra_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            all_emails.update(matches)
            
        return list(all_emails)
    
    def extract_names_from_html(self, html):
        """HTML থেকে নাম বের করে"""
        # মেটাডাটা থেকে নাম
        patterns = [
            r'<meta\s+property="og:title"\s+content="([^"]+)"',
            r'<meta\s+name="title"\s+content="([^"]+)"',
            r'<title>([^<]+)</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'class="profile_name"[^>]*>([^<]+)<',
            r'data-testid="profile_name"[^>]*>([^<]+)<',
            r'fb://profile/(\d+)',
            r'facebook\.com/([^/?&#]+)',
        ]
        
        names = []
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match and len(match) > 2:
                    names.append(match.strip())
                    
        return names
    
    def extract_json_ld(self, html):
        """JSON-LD ডাটা এক্সট্র্যাক্ট"""
        pattern = r'<script type="application/ld\+json">(.*?)</script>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        json_data = []
        for match in matches:
            try:
                data = json.loads(match)
                json_data.append(data)
            except:
                continue
                
        return json_data
    
    def smart_parse_profile(self, url):
        """স্মার্ট প্রোফাইল পার্সার"""
        try:
            print(f"[+] স্ক্যান করছি: {url}")
            
            # HTTP রিকুয়েস্ট
            response = self.session.get(url, timeout=self.timeout, proxies=self.proxies)
            
            if response.status_code != 200:
                print(f"[-] HTTP Error: {response.status_code}")
                return None
                
            html = response.text
            
            # সব ডাটা এক্সট্র্যাক্ট
            result = {
                'url': url,
                'phones': self.extract_phones_from_html(html),
                'emails': self.extract_emails_from_html(html),
                'names': self.extract_names_from_html(html),
                'json_ld': self.extract_json_ld(html),
                'title': self.extract_title(html),
                'meta_description': self.extract_meta_description(html),
                'meta_keywords': self.extract_meta_keywords(html),
                'social_links': self.extract_social_links(html),
                'raw_html': html[:5000],  # প্রথম 5000 ক্যারেক্টার
            }
            
            return result
            
        except Exception as e:
            print(f"[-] Error: {str(e)}")
            return None
    
    def extract_title(self, html):
        """টাইটেল এক্সট্র্যাক্ট"""
        match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        return match.group(1) if match else None
    
    def extract_meta_description(self, html):
        """মেটা ডেসক্রিপশন"""
        pattern = r'<meta\s+name="description"\s+content="([^"]+)"'
        match = re.search(pattern, html, re.IGNORECASE)
        return match.group(1) if match else None
    
    def extract_meta_keywords(self, html):
        """মেটা কিওয়ার্ড"""
        pattern = r'<meta\s+name="keywords"\s+content="([^"]+)"'
        match = re.search(pattern, html, re.IGNORECASE)
        return match.group(1) if match else None
    
    def extract_social_links(self, html):
        """সোশ্যাল মিডিয়া লিংক"""
        patterns = {
            'facebook': r'facebook\.com/([^/"\s]+)',
            'twitter': r'twitter\.com/([^/"\s]+)',
            'instagram': r'instagram\.com/([^/"\s]+)',
            'linkedin': r'linkedin\.com/(?:in/|company/)?([^/"\s]+)',
            'youtube': r'youtube\.com/(?:channel/|user/|@)?([^/"\s]+)',
            'tiktok': r'tiktok\.com/@([^/"\s]+)',
            'whatsapp': r'wa\.me/(\d+)',
            'telegram': r't\.me/([^/"\s]+)',
        }
        
        social_links = {}
        for platform, pattern in patterns.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                social_links[platform] = list(set(matches))
                
        return social_links
    
    def save_results(self, results, filename="results.json"):
        """রেজাল্টস সেভ করা"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[+] results loading : {filename}")
        
    def multi_scan(self, urls):
        """একাধিক URL স্ক্যান"""
        all_results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.smart_parse_profile, url): url for url in urls}
            
            for future in futures:
                url = futures[future]
                try:
                    result = future.result(timeout=60)
                    if result:
                        all_results.append(result)
                        print(f"[✓] complete: {url}")
                except Exception as e:
                    print(f"[✗] faild: {url} - {str(e)}")
                    
        return all_results

# মেইন ফাংশন
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║                    MAR-PD v3.0                           ║
║                   Scanner Engine                         ║
╚══════════════════════════════════════════════════════════╝
""")
    
    scanner = MARPD_Core()
    
    while True:
        print("\n" + "="*60)
        print("1. Single URL scan")
        print("2. Multiple URLs scan (in file)")
        print("3. Custom pattrn search")
        print("4. show results")
        print("5. exit")
        print("="*60)
        
        choice = input("\nselect (1-5): ").strip()
        
        if choice == "1":
            url = input("URL please : ").strip()
            if url:
                result = scanner.smart_parse_profile(url)
                if result:
                    scanner.save_results(result)
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    
        elif choice == "2":
            filename = input("upload your url file (URL list): ").strip()
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                    
                results = scanner.multi_scan(urls)
                scanner.save_results(results, "multi_scan_results.json")
                
        elif choice == "3":
            pattern = input(" need pattern search (regex): ").strip()
            text = input("text: ").strip()
            if pattern and text:
                matches = re.findall(pattern, text, re.IGNORECASE)
                print(f"found : {len(matches)}")
                for match in matches:
                    print(f"  → {match}")
                    
        elif choice == "4":
            filename = input("reults file : ").strip()
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    
        elif choice == "5":
            print("program is closed ...")
            break
            
        else:
            print("invalid option !")