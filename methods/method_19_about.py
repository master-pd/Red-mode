# file: method_19_about.py
import re
import json
from collections import Counter

class AboutAnalyzer:
    """About Information Analyzer"""
    
    def __init__(self):
        self.name = "About Information Analyzer"
        
    def execute(self, html_content):
        """About তথ্য অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'about_data': self.extract_about_data(html_content),
                'contact_info': self.extract_contact_info(html_content),
                'basic_info': self.extract_basic_info(html_content),
                'work_education': self.extract_work_education(html_content),
                'places_info': self.extract_places_info(html_content),
                'family_relationship': self.extract_family_relationship(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_about_data(self, html):
        """About ডাটা এক্সট্র্যাক্ট"""
        about_data = {
            'about_sections': [],
            'about_text': '',
            'section_headings': []
        }
        
        # About section patterns
        patterns = [
            r'<div[^>]*id="pagelet_timeline_about"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*about[^"]*"[^>]*>(.*?)</div>',
            r'data-testid="about"[^>]*>(.*?)</div>',
            r'<h2[^>]*>About</h2>(.*?)</div>',
            r'<section[^>]*about[^>]*>(.*?)</section>'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            if matches:
                about_data['about_text'] = matches[0]
                break
        
        # Section headings in about
        heading_patterns = [
            r'<h3[^>]*>([^<]+)</h3>',
            r'<h4[^>]*>([^<]+)</h4>',
            r'<div[^>]*class="[^"]*section[^"]*"[^>]*>([^<]+)</div>',
            r'data-testid="section_title"[^>]*>([^<]+)<'
        ]
        
        headings = []
        for pattern in heading_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            headings.extend(matches)
        
        about_data['section_headings'] = list(set(headings))
        
        # Extract individual about sections
        about_sections = {}
        
        # Common about sections
        sections = {
            'overview': r'overview.*?>(.*?)</div>',
            'work': r'work.*?>(.*?)</div>',
            'education': r'education.*?>(.*?)</div>',
            'places': r'(?:places|lives|from).*?>(.*?)</div>',
            'contact': r'contact.*?>(.*?)</div>',
            'basic': r'basic.*?>(.*?)</div>',
            'family': r'family.*?>(.*?)</div>',
            'relationship': r'relationship.*?>(.*?)</div>'
        }
        
        for section_name, pattern in sections.items():
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                about_sections[section_name] = match.group(1).strip()
        
        about_data['about_sections'] = about_sections
        
        return about_data
    
    def extract_contact_info(self, html):
        """কন্টাক্ট ইনফো এক্সট্র্যাক্ট"""
        contact_info = {
            'phones': [],
            'emails': [],
            'websites': [],
            'social_links': []
        }
        
        # Phone numbers
        phone_patterns = [
            r'tel:(\+?[0-9\s\-\(\)]+)',
            r'phone.*?>([^<]+)<',
            r'mobile.*?>([^<]+)<',
            r'contact.*?>([^<]+)<',
            r'(\+?88)?01[3-9]\d{8}'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                phone = re.sub(r'[^\d\+]', '', str(match))
                if len(phone) >= 10 and phone not in contact_info['phones']:
                    contact_info['phones'].append(phone)
        
        # Emails
        email_patterns = [
            r'mailto:([^"\']+)',
            r'email.*?>([^<]+)<',
            r'contact.*?>([^<]+)<',
            r'[\w\.-]+@[\w\.-]+\.\w+'
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if '@' in match and '.' in match and match not in contact_info['emails']:
                    contact_info['emails'].append(match.strip())
        
        # Websites
        website_patterns = [
            r'website.*?href="([^"]+)"',
            r'website.*?>([^<]+)<',
            r'link.*?href="([^"]+)"',
            r'http[^"\']+'
        ]
        
        for pattern in website_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if 'http' in match.lower() and match not in contact_info['websites']:
                    contact_info['websites'].append(match.strip())
        
        # Social links
        social_patterns = [
            r'facebook\.com/[^"\'>]+',
            r'twitter\.com/[^"\'>]+',
            r'instagram\.com/[^"\'>]+',
            r'linkedin\.com/[^"\'>]+',
            r'youtube\.com/[^"\'>]+'
        ]
        
        for pattern in social_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            contact_info['social_links'].extend(matches)
        
        return contact_info
    
    def extract_basic_info(self, html):
        """ব্যাসিক ইনফো এক্সট্র্যাক্ট"""
        basic_info = {
            'full_name': '',
            'username': '',
            'gender': '',
            'birthday': '',
            'languages': [],
            'interested_in': '',
            'religious_views': '',
            'political_views': ''
        }
        
        # Full name
        name_patterns = [
            r'<title>([^<]+)</title>',
            r'property="og:title"[^>]*content="([^"]+)"',
            r'data-testid="profile_name"[^>]*>([^<]+)<'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                basic_info['full_name'] = match.group(1).strip()
                break
        
        # Username/Profile URL
        url_patterns = [
            r'facebook\.com/([^/?&#]+)',
            r'profile\.php\?id=(\d+)'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                basic_info['username'] = match.group(1)
                break
        
        # Gender
        gender_patterns = [
            r'gender.*?>([^<]+)<',
            r'sex.*?>([^<]+)<',
            r'female.*?>([^<]+)<',
            r'male.*?>([^<]+)<'
        ]
        
        for pattern in gender_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                basic_info['gender'] = match.group(1).strip()
                break
        
        # Birthday
        birthday_patterns = [
            r'birthday.*?>([^<]+)<',
            r'born.*?>([^<]+)<',
            r'birth.*?date.*?>([^<]+)<'
        ]
        
        for pattern in birthday_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                basic_info['birthday'] = match.group(1).strip()
                break
        
        # Languages
        language_pattern = r'language.*?>([^<]+)<'
        matches = re.findall(language_pattern, html, re.IGNORECASE)
        if matches:
            basic_info['languages'] = [lang.strip() for lang in matches]
        
        # Interested in
        interest_pattern = r'interested.*?>([^<]+)<'
        match = re.search(interest_pattern, html, re.IGNORECASE)
        if match:
            basic_info['interested_in'] = match.group(1).strip()
        
        # Religious views
        religion_pattern = r'religion.*?>([^<]+)<'
        match = re.search(religion_pattern, html, re.IGNORECASE)
        if match:
            basic_info['religious_views'] = match.group(1).strip()
        
        # Political views
        politics_pattern = r'politic.*?>([^<]+)<'
        match = re.search(politics_pattern, html, re.IGNORECASE)
        if match:
            basic_info['political_views'] = match.group(1).strip()
        
        return basic_info
    
    def extract_work_education(self, html):
        """কাজ এবং শিক্ষা তথ্য"""
        work_education = {
            'work_places': [],
            'education_places': [],
            'professional_skills': [],
            'college': '',
            'high_school': '',
            'current_job': '',
            'previous_jobs': []
        }
        
        # Work places
        work_patterns = [
            r'work.*?at ([^<]+)<',
            r'works? at ([^<]+)<',
            r'employed.*?>([^<]+)<',
            r'job.*?>([^<]+)<',
            r'company.*?>([^<]+)<'
        ]
        
        work_places = []
        for pattern in work_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            work_places.extend(matches)
        
        work_education['work_places'] = list(set(work_places))
        
        # Education places
        edu_patterns = [
            r'studied.*?at ([^<]+)<',
            r'education.*?>([^<]+)<',
            r'college.*?>([^<]+)<',
            r'university.*?>([^<]+)<',
            r'school.*?>([^<]+)<'
        ]
        
        edu_places = []
        for pattern in edu_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            edu_places.extend(matches)
        
        work_education['education_places'] = list(set(edu_places))
        
        # Professional skills
        skill_patterns = [
            r'skill.*?>([^<]+)<',
            r'expertise.*?>([^<]+)<',
            r'proficient.*?>([^<]+)<',
            r'experienced.*?>([^<]+)<'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            skills.extend(matches)
        
        work_education['professional_skills'] = list(set(skills))
        
        # Specific education levels
        for edu in work_education['education_places']:
            edu_lower = edu.lower()
            if any(word in edu_lower for word in ['college', 'university', 'institute']):
                work_education['college'] = edu
            elif any(word in edu_lower for word in ['school', 'academy', 'high']):
                work_education['high_school'] = edu
        
        # Current job (first work place or most recent)
        if work_education['work_places']:
            work_education['current_job'] = work_education['work_places'][0]
            if len(work_education['work_places']) > 1:
                work_education['previous_jobs'] = work_education['work_places'][1:]
        
        return work_education
    
    def extract_places_info(self, html):
        """স্থান সম্পর্কিত তথ্য"""
        places_info = {
            'current_city': '',
            'hometown': '',
            'previous_cities': [],
            'places_lived': [],
            'checkin_locations': []
        }
        
        # Current city
        current_patterns = [
            r'lives in ([^<]+)<',
            r'current.*?city.*?>([^<]+)<',
            r'location.*?>([^<]+)<',
            r'city.*?>([^<]+)<'
        ]
        
        for pattern in current_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                places_info['current_city'] = match.group(1).strip()
                break
        
        # Hometown
        hometown_patterns = [
            r'from ([^<]+)<',
            r'hometown.*?>([^<]+)<',
            r'born in ([^<]+)<'
        ]
        
        for pattern in hometown_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                places_info['hometown'] = match.group(1).strip()
                break
        
        # Places lived
        places_pattern = r'lived.*?>([^<]+)<'
        matches = re.findall(places_pattern, html, re.IGNORECASE)
        if matches:
            places_info['places_lived'] = [place.strip() for place in matches]
        
        # Check-in locations
        checkin_pattern = r'at ([^<]+)<'
        matches = re.findall(checkin_pattern, html, re.IGNORECASE)
        if matches:
            places_info['checkin_locations'] = list(set(matches))
        
        # Previous cities (from places lived)
        if places_info['places_lived']:
            places_info['previous_cities'] = [
                place for place in places_info['places_lived'] 
                if place != places_info['current_city'] and place != places_info['hometown']
            ]
        
        return places_info
    
    def extract_family_relationship(self, html):
        """পরিবার এবং সম্পর্ক তথ্য"""
        family_info = {
            'relationship_status': '',
            'partner': '',
            'family_members': [],
            'family_connections': [],
            'anniversary': ''
        }
        
        # Relationship status
        status_patterns = [
            r'relationship.*?>([^<]+)<',
            r'single.*?>([^<]+)<',
            r'married.*?>([^<]+)<',
            r'engaged.*?>([^<]+)<',
            r'dating.*?>([^<]+)<'
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                family_info['relationship_status'] = match.group(1).strip()
                break
        
        # Partner
        partner_patterns = [
            r'with ([^<]+)<',
            r'partner.*?>([^<]+)<',
            r'in a relationship with ([^<]+)<'
        ]
        
        for pattern in partner_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                family_info['partner'] = match.group(1).strip()
                break
        
        # Family members
        family_patterns = [
            r'family.*?>([^<]+)<',
            r'mother.*?>([^<]+)<',
            r'father.*?>([^<]+)<',
            r'sibling.*?>([^<]+)<',
            r'brother.*?>([^<]+)<',
            r'sister.*?>([^<]+)<',
            r'child.*?>([^<]+)<',
            r'son.*?>([^<]+)<',
            r'daughter.*?>([^<]+)<'
        ]
        
        family_members = []
        for pattern in family_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            family_members.extend(matches)
        
        family_info['family_members'] = list(set(family_members))
        
        # Family connections (how they're related)
        connection_pattern = r'([^<]+) (?:is|are) (?:his|her|their) ([^<]+)<'
        matches = re.findall(connection_pattern, html, re.IGNORECASE)
        if matches:
            family_info['family_connections'] = [f"{person} - {relation}" for person, relation in matches]
        
        # Anniversary
        anniversary_pattern = r'anniversary.*?>([^<]+)<'
        match = re.search(anniversary_pattern, html, re.IGNORECASE)
        if match:
            family_info['anniversary'] = match.group(1).strip()
        
        return family_info