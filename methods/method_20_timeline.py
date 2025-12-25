# file: method_20_timeline.py
import re
import json
from datetime import datetime
from collections import Counter

class TimelineAnalyzer:
    """টাইমলাইন অ্যানালাইসিস"""
    
    def __init__(self):
        self.name = "Timeline Analyzer"
        
    def execute(self, html_content):
        """টাইমলাইন অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'timeline_structure': self.analyze_timeline_structure(html_content),
                'timeline_content': self.extract_timeline_content(html_content),
                'timeline_patterns': self.analyze_timeline_patterns(html_content),
                'key_life_events': self.extract_life_events(html_content),
                'timeline_stats': self.calculate_timeline_stats(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def analyze_timeline_structure(self, html):
        """টাইমলাইন স্ট্রাকচার অ্যানালাইসিস"""
        structure = {
            'timeline_sections': [],
            'timeline_years': [],
            'timeline_milestones': [],
            'section_headers': [],
            'timeline_organization': 'unknown'
        }
        
        # Timeline section headers
        header_patterns = [
            r'<h2[^>]*>([^<]+)</h2>',
            r'<h3[^>]*>([^<]+)</h3>',
            r'data-testid="timeline_section"[^>]*>([^<]+)<',
            r'class="[^"]*timeline[^"]*"[^>]*>([^<]+)<'
        ]
        
        headers = []
        for pattern in header_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            headers.extend(matches)
        
        structure['section_headers'] = list(set(headers))
        
        # Timeline years
        year_pattern = r'<div[^>]*>(\d{4})</div>'
        years = re.findall(year_pattern, html)
        structure['timeline_years'] = sorted(list(set(years)), reverse=True)
        
        # Timeline milestones (significant events)
        milestone_patterns = [
            r'milestone.*?>([^<]+)<',
            r'important.*?>([^<]+)<',
            r'significant.*?>([^<]+)<',
            r'event.*?>([^<]+)<',
            r'achievement.*?>([^<]+)<'
        ]
        
        milestones = []
        for pattern in milestone_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            milestones.extend(matches)
        
        structure['timeline_milestones'] = milestones
        
        # Timeline sections based on content
        sections = {
            'about': r'about',
            'posts': r'posts|updates|status',
            'photos': r'photos|images|pictures',
            'friends': r'friends|connections',
            'events': r'events|occasions',
            'places': r'places|locations|travel'
        }
        
        detected_sections = []
        for section, pattern in sections.items():
            if re.search(pattern, html, re.IGNORECASE):
                detected_sections.append(section)
        
        structure['timeline_sections'] = detected_sections
        
        # Timeline organization type
        org_patterns = [
            (r'chronological', 'chronological'),
            (r'reverse.*?chronological', 'reverse_chronological'),
            (r'grouped.*?year', 'year_grouped'),
            (r'sectioned', 'sectioned'),
            (r'thematic', 'thematic')
        ]
        
        for pattern, org_type in org_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                structure['timeline_organization'] = org_type
                break
        
        return structure
    
    def extract_timeline_content(self, html):
        """টাইমলাইন কনটেন্ট এক্সট্র্যাক্ট"""
        content = {
            'timeline_posts': [],
            'timeline_photos': [],
            'timeline_videos': [],
            'timeline_links': [],
            'timeline_events': [],
            'timeline_checkins': []
        }
        
        # Timeline posts
        post_patterns = [
            r'data-testid="post_message"[^>]*>([^<]+)</div>',
            r'class="[^"]*userContent[^"]*"[^>]*>([^<]+)<',
            r'timeline.*?>([^<]+)<'
        ]
        
        posts = []
        for pattern in post_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match.strip()) > 10:
                    posts.append(match.strip())
        
        content['timeline_posts'] = posts[:50]  # First 50 posts
        
        # Timeline photos
        photo_patterns = [
            r'src="([^"]+\.(?:jpg|jpeg|png|gif))"',
            r'data-src="([^"]+\.(?:jpg|jpeg|png))"',
            r'background-image: url\(["\']?([^"\'\)]+\.(?:jpg|jpeg|png))["\']?\)'
        ]
        
        photos = set()
        for pattern in photo_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if 'http' in match:
                    photos.add(match)
        
        content['timeline_photos'] = list(photos)[:30]  # First 30 photos
        
        # Timeline videos
        video_patterns = [
            r'src="([^"]+\.(?:mp4|webm|ogg))"',
            r'video.*?src="([^"]+)"',
            r'data-video="([^"]+)"'
        ]
        
        videos = []
        for pattern in video_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            videos.extend(matches)
        
        content['timeline_videos'] = videos[:10]
        
        # Timeline links
        link_patterns = [
            r'href="(https?://[^"]+)"',
            r'link.*?href="([^"]+)"',
            r'url.*?href="([^"]+)"'
        ]
        
        links = []
        for pattern in link_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            links.extend(matches)
        
        content['timeline_links'] = links[:20]
        
        # Timeline events
        event_patterns = [
            r'event.*?>([^<]+)<',
            r'attending.*?>([^<]+)<',
            r'going to ([^<]+)<'
        ]
        
        events = []
        for pattern in event_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            events.extend(matches)
        
        content['timeline_events'] = list(set(events))
        
        # Timeline check-ins
        checkin_patterns = [
            r'at ([^<]+)<',
            r'checked in at ([^<]+)<',
            r'location.*?>([^<]+)<'
        ]
        
        checkins = []
        for pattern in checkin_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            checkins.extend(matches)
        
        content['timeline_checkins'] = list(set(checkins))
        
        return content
    
    def analyze_timeline_patterns(self, html):
        """টাইমলাইন প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'posting_frequency': {},
            'content_type_distribution': {},
            'activity_patterns': {},
            'engagement_trends': {},
            'temporal_patterns': {}
        }
        
        # Posting frequency analysis
        date_pattern = r'data-utime="(\d+)"'
        timestamps = re.findall(date_pattern, html)
        
        if timestamps:
            # Convert to datetime and analyze
            dates = [datetime.fromtimestamp(int(ts)) for ts in timestamps if ts.isdigit()]
            
            if dates:
                # Group by year-month
                year_month_counts = Counter([d.strftime('%Y-%m') for d in dates])
                
                patterns['posting_frequency'] = {
                    'total_posts': len(dates),
                    'unique_months': len(year_month_counts),
                    'average_posts_per_month': len(dates) / max(1, len(year_month_counts)),
                    'most_active_month': year_month_counts.most_common(1)[0] if year_month_counts else None,
                    'year_month_distribution': dict(year_month_counts.most_common(12))
                }
        
        # Content type distribution
        content_types = {
            'text_posts': len(re.findall(r'post_message', html, re.IGNORECASE)),
            'photos': len(re.findall(r'\.(?:jpg|jpeg|png|gif)', html, re.IGNORECASE)),
            'videos': len(re.findall(r'\.(?:mp4|webm|ogg)', html, re.IGNORECASE)),
            'links': len(re.findall(r'http://|https://', html)),
            'events': len(re.findall(r'event', html, re.IGNORECASE)),
            'checkins': len(re.findall(r'at\s+[^<]+<', html, re.IGNORECASE))
        }
        
        total_content = sum(content_types.values())
        if total_content > 0:
            patterns['content_type_distribution'] = {
                'total_items': total_content,
                'percentages': {k: round((v/total_content)*100, 2) for k, v in content_types.items() if v > 0},
                'most_common_type': max(content_types.items(), key=lambda x: x[1])[0] if content_types else None
            }
        
        # Activity patterns (time of day)
        time_patterns = [
            r'(\d{1,2}):\d{2}\s*(?:AM|PM)',
            r'(\d{1,2}):\d{2}',
            r'at (\d{1,2}) o\'clock'
        ]
        
        hours = []
        for pattern in time_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    hour = int(match)
                    if 0 <= hour <= 23:
                        hours.append(hour)
                except:
                    pass
        
        if hours:
            hour_counts = Counter(hours)
            
            # Categorize into time slots
            time_slots = {
                'morning': sum(1 for h in hours if 5 <= h < 12),
                'afternoon': sum(1 for h in hours if 12 <= h < 17),
                'evening': sum(1 for h in hours if 17 <= h < 22),
                'night': sum(1 for h in hours if h >= 22 or h < 5)
            }
            
            patterns['temporal_patterns'] = {
                'total_times': len(hours),
                'hour_distribution': dict(hour_counts),
                'time_slot_distribution': time_slots,
                'most_active_hour': hour_counts.most_common(1)[0] if hour_counts else None,
                'most_active_time_slot': max(time_slots.items(), key=lambda x: x[1])[0] if time_slots else None
            }
        
        # Engagement trends
        engagement_patterns = {
            'likes': len(re.findall(r'like', html, re.IGNORECASE)),
            'comments': len(re.findall(r'comment', html, re.IGNORECASE)),
            'shares': len(re.findall(r'share', html, re.IGNORECASE)),
            'reactions': len(re.findall(r'reaction', html, re.IGNORECASE))
        }
        
        total_engagement = sum(engagement_patterns.values())
        if total_engagement > 0:
            patterns['engagement_trends'] = {
                'total_engagement': total_engagement,
                'engagement_types': engagement_patterns,
                'engagement_ratios': {k: round((v/total_engagement)*100, 2) for k, v in engagement_patterns.items()}
            }
        
        return patterns
    
    def extract_life_events(self, html):
        """জীবনের গুরুত্বপূর্ণ ঘটনা এক্সট্র্যাক্ট"""
        life_events = {
            'education_events': [],
            'work_events': [],
            'relationship_events': [],
            'family_events': [],
            'travel_events': [],
            'achievement_events': []
        }
        
        # Education events
        edu_patterns = [
            r'graduated.*?>([^<]+)<',
            r'started.*?school.*?>([^<]+)<',
            r'college.*?>([^<]+)<',
            r'university.*?>([^<]+)<',
            r'degree.*?>([^<]+)<'
        ]
        
        edu_events = []
        for pattern in edu_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            edu_events.extend(matches)
        
        life_events['education_events'] = list(set(edu_events))
        
        # Work events
        work_patterns = [
            r'started.*?work.*?>([^<]+)<',
            r'got.*?job.*?>([^<]+)<',
            r'promotion.*?>([^<]+)<',
            r'company.*?>([^<]+)<',
            r'career.*?>([^<]+)<'
        ]
        
        work_events = []
        for pattern in work_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            work_events.extend(matches)
        
        life_events['work_events'] = list(set(work_events))
        
        # Relationship events
        relationship_patterns = [
            r'married.*?>([^<]+)<',
            r'engagement.*?>([^<]+)<',
            r'anniversary.*?>([^<]+)<',
            r'relationship.*?>([^<]+)<',
            r'dating.*?>([^<]+)<'
        ]
        
        relationship_events = []
        for pattern in relationship_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            relationship_events.extend(matches)
        
        life_events['relationship_events'] = list(set(relationship_events))
        
        # Family events
        family_patterns = [
            r'born.*?>([^<]+)<',
            r'birth.*?>([^<]+)<',
            r'family.*?>([^<]+)<',
            r'child.*?>([^<]+)<',
            r'parent.*?>([^<]+)<'
        ]
        
        family_events = []
        for pattern in family_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            family_events.extend(matches)
        
        life_events['family_events'] = list(set(family_events))
        
        # Travel events
        travel_patterns = [
            r'travel.*?>([^<]+)<',
            r'visited.*?>([^<]+)<',
            r'trip.*?>([^<]+)<',
            r'vacation.*?>([^<]+)<',
            r'holiday.*?>([^<]+)<'
        ]
        
        travel_events = []
        for pattern in travel_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            travel_events.extend(matches)
        
        life_events['travel_events'] = list(set(travel_events))
        
        # Achievement events
        achievement_patterns = [
            r'achievement.*?>([^<]+)<',
            r'award.*?>([^<]+)<',
            r'certificate.*?>([^<]+)<',
            r'won.*?>([^<]+)<',
            r'accomplishment.*?>([^<]+)<'
        ]
        
        achievement_events = []
        for pattern in achievement_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            achievement_events.extend(matches)
        
        life_events['achievement_events'] = list(set(achievement_events))
        
        return life_events
    
    def calculate_timeline_stats(self, html):
        """টাইমলাইন স্ট্যাটিসটিক্স"""
        stats = {
            'timeline_coverage': {},
            'activity_level': 'unknown',
            'content_density': 'unknown',
            'timeline_consistency': 'unknown',
            'key_metrics': {}
        }
        
        # Timeline coverage (years covered)
        year_pattern = r'(\d{4})'
        years = re.findall(year_pattern, html)
        
        if years:
            years_int = [int(y) for y in years if y.isdigit()]
            if years_int:
                min_year = min(years_int)
                max_year = max(years_int)
                coverage_years = max_year - min_year + 1
                
                stats['timeline_coverage'] = {
                    'min_year': min_year,
                    'max_year': max_year,
                    'coverage_years': coverage_years,
                    'years_found': len(set(years_int))
                }
        
        # Activity level based on content density
        content_indicators = [
            'post_message',
            'userContent',
            'photo',
            'video',
            'event'
        ]
        
        content_count = 0
        for indicator in content_indicators:
            content_count += len(re.findall(indicator, html, re.IGNORECASE))
        
        # Determine activity level
        if content_count > 100:
            stats['activity_level'] = 'very_high'
        elif content_count > 50:
            stats['activity_level'] = 'high'
        elif content_count > 20:
            stats['activity_level'] = 'medium'
        elif content_count > 5:
            stats['activity_level'] = 'low'
        else:
            stats['activity_level'] = 'very_low'
        
        # Content density (posts per year)
        if 'timeline_coverage' in stats and stats['timeline_coverage'].get('coverage_years', 0) > 0:
            years_covered = stats['timeline_coverage']['coverage_years']
            density = content_count / years_covered
            
            if density > 50:
                stats['content_density'] = 'very_dense'
            elif density > 20:
                stats['content_density'] = 'dense'
            elif density > 10:
                stats['content_density'] = 'moderate'
            elif density > 5:
                stats['content_density'] = 'sparse'
            else:
                stats['content_density'] = 'very_sparse'
        
        # Timeline consistency (regular posting)
        consistency_indicators = [
            (r'regular.*?poster', 'very_consistent'),
            (r'consistent.*?activity', 'consistent'),
            (r'occasional.*?posts', 'occasional'),
            (r'irregular', 'irregular'),
            (r'inactive', 'inactive')
        ]
        
        for pattern, consistency in consistency_indicators:
            if re.search(pattern, html, re.IGNORECASE):
                stats['timeline_consistency'] = consistency
                break
        
        # Key metrics
        stats['key_metrics'] = {
            'total_posts_estimated': content_count,
            'photos_count': len(re.findall(r'\.(?:jpg|jpeg|png|gif)', html, re.IGNORECASE)),
            'videos_count': len(re.findall(r'\.(?:mp4|webm|ogg)', html, re.IGNORECASE)),
            'events_count': len(re.findall(r'event', html, re.IGNORECASE)),
            'checkins_count': len(re.findall(r'at\s+[^<]+<', html, re.IGNORECASE)),
            'life_events_count': sum(len(events) for events in self.extract_life_events(html).values())
        }
        
        return stats