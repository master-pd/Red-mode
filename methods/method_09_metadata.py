# file: method_09_metadata.py
import re
import json
from datetime import datetime

class MetadataExtractor:
    """Metadata Extractor"""
    
    def __init__(self):
        self.name = "Metadata Extractor"
        
    def execute(self, html_content):
        """মেটাডাটা এক্সট্র্যাক্ট"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            metadata = {
                'basic_metadata': self.extract_basic_metadata(html_content),
                'opengraph_metadata': self.extract_opengraph_metadata(html_content),
                'twitter_metadata': self.extract_twitter_metadata(html_content),
                'facebook_metadata': self.extract_facebook_metadata(html_content),
                'seo_metadata': self.extract_seo_metadata(html_content),
                'structured_data': self.extract_structured_data(html_content)
            }
            
            results['data'] = metadata
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_basic_metadata(self, html):
        """ব্যাসিক মেটাডাটা"""
        metadata = {}
        
        # মেটা ট্যাগ
        meta_pattern = r'<meta\s+([^>]+)>'
        meta_tags = re.findall(meta_pattern, html, re.IGNORECASE)
        
        for tag in meta_tags:
            # নাম এবং কন্টেন্ট
            name_match = re.search(r'name=["\']([^"\']+)["\']', tag)
            content_match = re.search(r'content=["\']([^"\']+)["\']', tag)
            
            if name_match and content_match:
                name = name_match.group(1).lower()
                content = content_match.group(1)
                
                # শুধু গুরুত্বপূর্ণ মেটাডাটা
                important_meta = ['description', 'keywords', 'author', 'viewport', 
                                 'robots', 'generator', 'theme-color']
                
                if any(meta in name for meta in important_meta):
                    metadata[name] = content
        
        return metadata
    
    def extract_opengraph_metadata(self, html):
        """OpenGraph মেটাডাটা"""
        og_metadata = {}
        
        og_pattern = r'<meta\s+property="og:([^"]+)"\s+content="([^"]+)"'
        matches = re.findall(og_pattern, html, re.IGNORECASE)
        
        for match in matches:
            property_name, content = match
            og_metadata[property_name] = content
        
        return og_metadata
    
    def extract_twitter_metadata(self, html):
        """Twitter Card মেটাডাটা"""
        twitter_metadata = {}
        
        twitter_pattern = r'<meta\s+(?:name|property)="twitter:([^"]+)"\s+content="([^"]+)"'
        matches = re.findall(twitter_pattern, html, re.IGNORECASE)
        
        for match in matches:
            property_name, content = match
            twitter_metadata[property_name] = content
        
        return twitter_metadata
    
    def extract_facebook_metadata(self, html):
        """ফেসবুক স্পেসিফিক মেটাডাটা"""
        fb_metadata = {}
        
        fb_patterns = [
            (r'fb:app_id["\'][^>]*content=["\']([^"\']+)["\']', 'app_id'),
            (r'fb:pages["\'][^>]*content=["\']([^"\']+)["\']', 'pages'),
            (r'fb:admins["\'][^>]*content=["\']([^"\']+)["\']', 'admins'),
            (r'data-app-id=["\']([^"\']+)["\']', 'data_app_id')
        ]
        
        for pattern, key in fb_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                fb_metadata[key] = match.group(1)
        
        return fb_metadata
    
    def extract_seo_metadata(self, html):
        """SEO রিলেটেড মেটাডাটা"""
        seo_data = {}
        
        # Title
        title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            seo_data['title'] = title_match.group(1).strip()
        
        # Description
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
        if desc_match:
            seo_data['description'] = desc_match.group(1).strip()
        
        # Keywords
        keywords_match = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', html, re.IGNORECASE)
        if keywords_match:
            seo_data['keywords'] = keywords_match.group(1).strip()
        
        # Canonical URL
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html, re.IGNORECASE)
        if canonical_match:
            seo_data['canonical_url'] = canonical_match.group(1)
        
        # H1 tags
        h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        if h1_matches:
            seo_data['h1_tags'] = [h1.strip() for h1 in h1_matches]
        
        # Word count
        text_content = re.sub(r'<[^>]+>', ' ', html)
        words = text_content.split()
        seo_data['word_count'] = len(words)
        
        return seo_data
    
    def extract_structured_data(self, html):
        """Structured Data (JSON-LD, Microdata)"""
        structured = {
            'json_ld': [],
            'microdata': [],
            'rdfa': []
        }
        
        # JSON-LD
        jsonld_pattern = r'<script\s+type="application/ld\+json">(.*?)</script>'
        jsonld_matches = re.findall(jsonld_pattern, html, re.DOTALL | re.IGNORECASE)
        
        for match in jsonld_matches:
            try:
                data = json.loads(match.strip())
                structured['json_ld'].append(data)
            except:
                pass
        
        # Microdata
        microdata_pattern = r'itemtype="([^"]+)"'
        microdata_matches = re.findall(microdata_pattern, html, re.IGNORECASE)
        structured['microdata'] = list(set(microdata_matches))
        
        # RDFa
        rdfa_pattern = r'typeof="([^"]+)"'
        rdfa_matches = re.findall(rdfa_pattern, html, re.IGNORECASE)
        structured['rdfa'] = list(set(rdfa_matches))
        
        return structured