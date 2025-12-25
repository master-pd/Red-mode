# file: method_01_profile.py
import re
import json
from urllib.parse import urljoin

class ProfileAnalyzer:
    """প্রোফাইল এনালাইজার মেথড"""
    
    def __init__(self):
        self.name = "Profile HTML Analysis"
        self.version = "1.0"
        self.priority = 1
        
    def execute(self, html, url=None):
        """মেইন এক্সিকিউশন"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            # 1. ব্যাসিক ইনফো
            basic_info = self.extract_basic_info(html)
            
            # 2. কন্টাক্ট ইনফো
            contact_info = self.extract_contact_info(html)
            
            # 3. সোশ্যাল লিংক
            social_links = self.extract_social_links(html)
            
            # 4. মেটাডাটা
            metadata = self.extract_metadata(html)
            
            # 5. হিডেন ফিল্ড
            hidden_fields = self.find_hidden_fields(html)
            
            results['data'] = {
                'basic_info': basic_info,
                'contact_info': contact_info,
                'social_links': social_links,
                'metadata': metadata,
                'hidden_fields': hidden_fields
            }
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
            
        return results
    
    def extract_basic_info(self, html):
        """ব্যাসিক ইনফো এক্সট্র্যাক্ট"""
        info = {}
        
        # নাম
        name_patterns = [
            r'<title>([^<]+)</title>',
            r'property="og:title"\s+content="([^"]+)"',
            r'<h1[^>]*>([^<]+)</h1>',
            r'class=["\']profile_name["\'][^>]*>([^<]+)<',
            r'data-testid=["\']profile_name["\'][^>]*>([^<]+)<',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                info['name'] = match.group(1).strip()
                break
                
        # বায়ো/ডেসক্রিপশন
        bio_patterns = [
            r'<meta\s+property="og:description"\s+content="([^"]+)"',
            r'<meta\s+name="description"\s+content="([^"]+)"',
            r'<div[^>]*class=["\'][^"\']*bio[^"\']*["\'][^>]*>([^<]+)<',
            r'<div[^>]*class=["\'][^"\']*about[^"\']*["\'][^>]*>([^<]+)<',
        ]
        
        for pattern in bio_patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                info['bio'] = match.group(1).strip()
                break
                
        # লোকেশন
        location_patterns = [
            r'location["\'][^>]*>([^<]+)<',
            r'class=["\'][^"\']*location[^"\']*["\'][^>]*>([^<]+)<',
            r'data-testid=["\'][^"\']*location[^"\']*["\'][^>]*>([^<]+)<',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                info['location'] = match.group(1).strip()
                break
                
        return info
    
    def extract_contact_info(self, html):
        """কন্টাক্ট ইনফো এক্সট্র্যাক্ট"""
        contacts = {
            'phones': [],
            'emails': [],
            'websites': []
        }
        
        # ফোন নম্বর
        phone_patterns = [
            r'\b01[3-9]\d{8}\b',
            r'tel:([+0-9\s\-]+)',
            r'phone["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',
            r'mobile["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',
            r'contact["\']?\s*:\s*["\']?([+0-9\s\-]+)["\']?',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                phone = re.sub(r'[^\d\+]', '', str(match))
                if len(phone) >= 10 and phone not in contacts['phones']:
                    contacts['phones'].append(phone)
                    
        # ইমেইল
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        contacts['emails'] = list(set(emails))
        
        # ওয়েবসাইট
        website_patterns = [
            r'href=["\'](https?://[^"\']+)["\']',
            r'website["\']?\s*:\s*["\']?([^"\']+)["\']?',
            r'url["\']?\s*:\s*["\']?([^"\']+)["\']?',
        ]
        
        for pattern in website_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if 'http' in str(match).lower() and match not in contacts['websites']:
                    contacts['websites'].append(match)
                    
        return contacts
    
    def extract_social_links(self, html):
        """সোশ্যাল মিডিয়া লিংক"""
        social = {}
        
        patterns = {
            'facebook': r'facebook\.com/([^/"\s?&#]+)',
            'twitter': r'twitter\.com/([^/"\s?&#]+)',
            'instagram': r'instagram\.com/([^/"\s?&#]+)',
            'linkedin': r'linkedin\.com/(?:in/|company/)?([^/"\s?&#]+)',
            'youtube': r'youtube\.com/(?:channel/|user/|@)?([^/"\s?&#]+)',
            'whatsapp': r'wa\.me/(\d+)',
            'telegram': r't\.me/([^/"\s?&#]+)',
            'tiktok': r'tiktok\.com/@([^/"\s?&#]+)',
        }
        
        for platform, pattern in patterns.items():
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                social[platform] = list(set(matches))
                
        return social
    
    def extract_metadata(self, html):
        """মেটাডাটা এক্সট্র্যাক্ট"""
        metadata = {}
        
        # সব মেটা ট্যাগ
        meta_pattern = r'<meta\s+([^>]+)>'
        meta_tags = re.findall(meta_pattern, html, re.IGNORECASE)
        
        for tag in meta_tags:
            # নাম এবং কন্টেন্ট বের করা
            name_match = re.search(r'name=["\']([^"\']+)["\']', tag, re.IGNORECASE)
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag, re.IGNORECASE)
            property_match = re.search(r'property=["\']([^"\']+)["\']', tag, re.IGNORECASE)
            
            if name_match and content_match:
                name = name_match.group(1)
                content = content_match.group(1)
                metadata[name] = content
            elif property_match and content_match:
                prop = property_match.group(1)
                content = content_match.group(1)
                metadata[prop] = content
                
        return metadata
    
    def find_hidden_fields(self, html):
        """হিডেন ফর্ম ফিল্ড"""
        hidden = []
        
        # হিডেন ইনপুট ফিল্ড
        hidden_pattern = r'<input[^>]*type=["\']hidden["\'][^>]*>'
        hidden_fields = re.findall(hidden_pattern, html, re.IGNORECASE)
        
        for field in hidden_fields:
            # নাম এবং ভ্যালু বের করা
            name_match = re.search(r'name=["\']([^"\']+)["\']', field, re.IGNORECASE)
            value_match = re.search(r'value=["\']([^"\']+)["\']', field, re.IGNORECASE)
            
            if name_match:
                hidden.append({
                    'field': field,
                    'name': name_match.group(1) if name_match else None,
                    'value': value_match.group(1) if value_match else None
                })
                
        return hidden

# রান করার জন্য
if __name__ == "__main__":
    analyzer = ProfileAnalyzer()
    
    # টেস্ট HTML
    test_html = """
    <html>
    <title>John Doe Profile</title>
    <meta name="description" content="Contact: 01712345678">
    <meta property="og:phone" content="+8801712345678">
    <div class="bio">Email: johndoe@example.com</div>
    </html>
    """
    
    result = analyzer.execute(test_html)
    print(json.dumps(result, indent=2))