# file: method_18_photos.py
import re
import json
from collections import Counter
from urllib.parse import urljoin

class PhotosAnalyzer:
    """ফটোস অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Photos Analyzer"
        
    def execute(self, html_content, base_url=None):
        """ফটোস অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'photos_data': self.extract_photos_data(html_content, base_url),
                'photo_metadata': self.extract_photo_metadata(html_content),
                'albums_analysis': self.analyze_albums(html_content, base_url),
                'photo_patterns': self.analyze_photo_patterns(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_photos_data(self, html, base_url=None):
        """ফটোস ডাটা এক্সট্র্যাক্ট"""
        photos_data = {
            'total_photos': 0,
            'photo_urls': [],
            'photo_captions': [],
            'photo_dates': [],
            'album_links': []
        }
        
        # Facebook photos patterns
        patterns = [
            # Photos count
            r'(\d+[,]?\d*)\s*photos',
            r'photos.*?(\d+[,]?\d*)',
            r'(\d+)\s*images',
            r'picture.*?count.*?(\d+)',
            
            # Photo URLs
            r'src=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp))["\']',
            r'data-src=["\']([^"\']+\.(?:jpg|jpeg|png|gif))["\']',
            r'background-image:\s*url\(["\']?([^"\'\)]+\.(?:jpg|jpeg|png))["\']?\)',
            r'<img[^>]+srcset=["\']([^"\']+\.(?:jpg|jpeg|png)[^"\']*)["\']',
            
            # Photo captions
            r'alt=["\']([^"\']+)["\']',
            r'aria-label=["\']([^"\']+)["\']',
            r'data-testid="media_caption"[^>]*>([^<]+)<',
            r'photo.*?caption[^>]*>([^<]+)<',
            
            # Photo dates
            r'photo.*?date[^>]*>([^<]+)<',
            r'uploaded.*?on ([^<]+)',
            r'taken.*?([^<]+)',
            r'date.*?photo[^>]*>([^<]+)<',
            
            # Album links
            r'href=["\']/(photos/[^"\']+)["\']',
            r'href=["\']/(albums/[^"\']+)["\']',
            r'album.*?href=["\']([^"\']+)["\']'
        ]
        
        # Extract photos count
        for pattern in patterns[:4]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = self.parse_count(match)
                    if count > photos_data['total_photos']:
                        photos_data['total_photos'] = count
                except:
                    pass
        
        # Extract photo URLs
        photo_urls = set()
        for pattern in patterns[4:8]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                
                if match and any(ext in match.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    # Make absolute URL if base_url provided
                    if base_url and not match.startswith(('http://', 'https://')):
                        match = urljoin(base_url, match)
                    photo_urls.add(match)
        
        photos_data['photo_urls'] = list(photo_urls)[:50]  # First 50 photos
        
        # Extract photo captions
        captions = []
        for pattern in patterns[8:12]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 3:
                    captions.append(match.strip())
        
        photos_data['photo_captions'] = captions[:50]  # First 50 captions
        
        # Extract photo dates
        dates = []
        for pattern in patterns[12:16]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            dates.extend(matches)
        
        photos_data['photo_dates'] = dates[:20]
        
        # Extract album links
        album_links = set()
        for pattern in patterns[16:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match:
                    if base_url and not match.startswith(('http://', 'https://')):
                        match = urljoin(base_url, match)
                    album_links.add(match)
        
        photos_data['album_links'] = list(album_links)
        
        return photos_data
    
    def parse_count(self, text):
        """কাউন্ট পার্স"""
        text = str(text).lower().strip()
        
        if 'k' in text:
            return int(float(text.replace('k', '').replace(',', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '').replace(',', '')) * 1000000)
        else:
            return int(text.replace(',', ''))
    
    def extract_photo_metadata(self, html):
        """ফটো মেটাডাটা এক্সট্র্যাক্ট"""
        metadata = {
            'exif_data': {},
            'location_data': [],
            'tagged_people': [],
            'photo_sizes': []
        }
        
        # EXIF data patterns
        exif_patterns = [
            r'camera.*?([^<]+)<',
            r'lens.*?([^<]+)<',
            r'aperture.*?([^<]+)<',
            r'shutter.*?([^<]+)<',
            r'iso.*?([^<]+)<',
            r'focal.*?([^<]+)<'
        ]
        
        for pattern in exif_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                key = pattern.split('.*?')[0]
                metadata['exif_data'][key] = matches[0].strip()
        
        # Location data
        location_patterns = [
            r'location.*?>([^<]+)<',
            r'taken at ([^<]+)',
            r'<a[^>]*>([^<]+)</a>.*?map',
            r'map.*?>([^<]+)<'
        ]
        
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            locations.extend(matches)
        
        metadata['location_data'] = list(set(locations))
        
        # Tagged people
        tag_patterns = [
            r'tagged.*?>([^<]+)<',
            r'with ([^<]+)',
            r'<a[^>]*>([^<]+)</a>.*?tagged',
            r'photo.*?of ([^<]+)'
        ]
        
        tagged = []
        for pattern in tag_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            tagged.extend(matches)
        
        metadata['tagged_people'] = list(set(tagged))
        
        # Photo size information
        size_patterns = [
            r'(\d+)\s*×\s*(\d+)',  # Dimensions like 1920×1080
            r'(\d+)\s*x\s*(\d+)',
            r'width.*?(\d+).*?height.*?(\d+)',
            r'size.*?(\d+)\s*KB',
            r'size.*?(\d+)\s*MB'
        ]
        
        sizes = []
        for pattern in size_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    sizes.append(f"{match[0]}x{match[1]}")
                else:
                    sizes.append(str(match))
        
        metadata['photo_sizes'] = sizes
        
        return metadata
    
    def analyze_albums(self, html, base_url=None):
        """অ্যালবাম অ্যানালাইসিস"""
        albums_analysis = {
            'total_albums': 0,
            'album_titles': [],
            'album_photo_counts': [],
            'album_dates': [],
            'album_themes': {}
        }
        
        # Album patterns
        album_patterns = [
            # Album count
            r'(\d+)\s*albums',
            r'albums.*?(\d+)',
            
            # Album titles
            r'album.*?title[^>]*>([^<]+)<',
            r'<a[^>]*>([^<]+)</a>.*?album',
            r'data-testid="album_title"[^>]*>([^<]+)<',
            
            # Album photo counts
            r'album.*?(\d+)\s*photos',
            r'(\d+)\s*photos.*?album',
            r'photos.*?album[^>]*>(\d+)<',
            
            # Album dates
            r'album.*?created.*?([^<]+)',
            r'album.*?date[^>]*>([^<]+)<',
            r'updated.*?album[^>]*>([^<]+)<'
        ]
        
        # Extract album count
        for pattern in album_patterns[:2]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if count > albums_analysis['total_albums']:
                        albums_analysis['total_albums'] = count
                except:
                    pass
        
        # Extract album titles
        titles = []
        for pattern in album_patterns[2:5]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            titles.extend(matches)
        
        albums_analysis['album_titles'] = list(set(titles))[:20]
        
        # Extract album photo counts
        photo_counts = []
        for pattern in album_patterns[5:8]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    photo_counts.append(int(match))
                except:
                    pass
        
        albums_analysis['album_photo_counts'] = photo_counts
        
        # Extract album dates
        dates = []
        for pattern in album_patterns[8:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            dates.extend(matches)
        
        albums_analysis['album_dates'] = dates
        
        # Analyze album themes from titles
        themes = {
            'profile_photos': 0,
            'cover_photos': 0,
            'mobile_uploads': 0,
            'timeline_photos': 0,
            'family': 0,
            'friends': 0,
            'travel': 0,
            'events': 0,
            'other': 0
        }
        
        for title in albums_analysis['album_titles']:
            title_lower = title.lower()
            
            if any(word in title_lower for word in ['profile', 'dp', 'display']):
                themes['profile_photos'] += 1
            elif any(word in title_lower for word in ['cover', 'header', 'banner']):
                themes['cover_photos'] += 1
            elif any(word in title_lower for word in ['mobile', 'phone', 'android', 'iphone']):
                themes['mobile_uploads'] += 1
            elif any(word in title_lower for word in ['timeline', 'wall', 'posts']):
                themes['timeline_photos'] += 1
            elif any(word in title_lower for word in ['family', 'parents', 'siblings', 'kids']):
                themes['family'] += 1
            elif any(word in title_lower for word in ['friends', 'buddies', 'mates', 'crew']):
                themes['friends'] += 1
            elif any(word in title_lower for word in ['travel', 'trip', 'vacation', 'holiday']):
                themes['travel'] += 1
            elif any(word in title_lower for word in ['event', 'party', 'wedding', 'birthday']):
                themes['events'] += 1
            else:
                themes['other'] += 1
        
        albums_analysis['album_themes'] = {k: v for k, v in themes.items() if v > 0}
        
        return albums_analysis
    
    def analyze_photo_patterns(self, html):
        """ফটো প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'upload_frequency': 'unknown',
            'photo_types': {},
            'tagging_patterns': {},
            'engagement_on_photos': {}
        }
        
        # Upload frequency indicators
        frequency_patterns = [
            (r'daily.*?photos', 'daily'),
            (r'weekly.*?uploads', 'weekly'),
            (r'regular.*?uploader', 'regular'),
            (r'frequent.*?photos', 'frequent'),
            (r'rare.*?photos', 'rare'),
            (r'new.*?upload', 'recent')
        ]
        
        for pattern, frequency in frequency_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                patterns['upload_frequency'] = frequency
                break
        
        # Photo type analysis
        photo_types = {
            'selfie': 0,
            'group_photo': 0,
            'landscape': 0,
            'food': 0,
            'event': 0,
            'screenshot': 0
        }
        
        # Analyze from captions and metadata
        captions = self.extract_photos_data(html)['photo_captions']
        metadata = self.extract_photo_metadata(html)
        
        for caption in captions:
            caption_lower = caption.lower()
            
            if any(word in caption_lower for word in ['selfie', 'self', 'me ', 'myself']):
                photo_types['selfie'] += 1
            elif any(word in caption_lower for word in ['group', 'friends', 'team', 'together']):
                photo_types['group_photo'] += 1
            elif any(word in caption_lower for word in ['view', 'scenery', 'landscape', 'nature']):
                photo_types['landscape'] += 1
            elif any(word in caption_lower for word in ['food', 'meal', 'dish', 'restaurant']):
                photo_types['food'] += 1
            elif any(word in caption_lower for word in ['event', 'party', 'celebration', 'wedding']):
                photo_types['event'] += 1
            elif any(word in caption_lower for word in ['screenshot', 'screen shot', 'capture']):
                photo_types['screenshot'] += 1
        
        patterns['photo_types'] = {k: v for k, v in photo_types.items() if v > 0}
        
        # Tagging patterns
        tagged_people = metadata['tagged_people']
        if tagged_people:
            patterns['tagging_patterns'] = {
                'total_tagged': len(tagged_people),
                'unique_people': len(set(tagged_people)),
                'frequently_tagged': Counter(tagged_people).most_common(5)
            }
        
        # Engagement on photos (likes, comments)
        engagement_patterns = [
            (r'photo.*?(\d+)\s*likes', 'likes'),
            (r'(\d+)\s*likes.*?photo', 'likes'),
            (r'photo.*?(\d+)\s*comments', 'comments'),
            (r'(\d+)\s*comments.*?photo', 'comments'),
            (r'photo.*?(\d+)\s*shares', 'shares')
        ]
        
        engagement_counts = {'likes': 0, 'comments': 0, 'shares': 0}
        for pattern, eng_type in engagement_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if count > engagement_counts[eng_type]:
                        engagement_counts[eng_type] = count
                except:
                    pass
        
        patterns['engagement_on_photos'] = engagement_counts
        
        return patterns