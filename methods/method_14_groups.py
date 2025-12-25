# file: method_14_groups.py
import re
import json
from collections import Counter

class GroupsAnalyzer:
    """গ্রুপস অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Groups Analyzer"
        
    def execute(self, html_content):
        """গ্রুপস অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'groups_data': self.extract_groups_data(html_content),
                'groups_analysis': self.analyze_groups(html_content),
                'group_types': self.categorize_groups(html_content),
                'membership_patterns': self.analyze_membership_patterns(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_groups_data(self, html):
        """গ্রুপস ডাটা এক্সট্র্যাক্ট"""
        groups_data = {
            'total_groups': 0,
            'groups_list': [],
            'group_urls': [],
            'group_ids': []
        }
        
        # Facebook groups patterns
        patterns = [
            # Groups count
            r'(\d+)\s*groups',
            r'groups.*?(\d+)',
            r'member of (\d+) groups',
            
            # Group names
            r'<a[^>]*href=["\']/groups/([^"\']+)["\'][^>]*>([^<]+)</a>',
            r'data-testid="group_list_item"[^>]*>([^<]+)</div>',
            r'class=["\'][^"\']*group[^"\']*["\'][^>]*>([^<]+)<',
            
            # Group URLs
            r'href=["\']/groups/(\d+)["\']',
            r'href=["\']/(group\.php\?id=\d+)',
            r'fb://group/(\d+)'
        ]
        
        # Extract groups count
        for pattern in patterns[:3]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if count > groups_data['total_groups']:
                        groups_data['total_groups'] = count
                except:
                    pass
        
        # Extract group names and URLs
        group_items = set()
        for pattern in patterns[3:6]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    group_id, group_name = match
                    group_items.add((group_id, group_name))
                elif len(match.strip()) > 2:
                    group_items.add(('unknown', match.strip()))
        
        for group_id, group_name in group_items:
            groups_data['groups_list'].append({
                'name': group_name,
                'id': group_id,
                'url': f"https://facebook.com/groups/{group_id}" if group_id != 'unknown' else 'unknown'
            })
        
        # Extract group IDs
        for pattern in patterns[6:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match.isdigit():
                    groups_data['group_ids'].append(match)
                    groups_data['group_urls'].append(f"https://facebook.com/groups/{match}")
        
        return groups_data
    
    def analyze_groups(self, html):
        """গ্রুপস ডিটেইলড অ্যানালাইসিস"""
        analysis = {
            'group_categories': [],
            'group_sizes': [],
            'activity_levels': [],
            'privacy_settings': []
        }
        
        # Group size indicators
        size_patterns = [
            (r'(\d+[,]?\d*)\s*members', 'members_count'),
            (r'members.*?(\d+[,]?\d*)', 'members_count'),
            (r'small group', 'small'),
            (r'large group', 'large'),
            (r'(\d+)k members', 'thousands')
        ]
        
        for pattern, size_type in size_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match.isdigit() or (isinstance(match, str) and match.replace(',', '').isdigit()):
                    analysis['group_sizes'].append({
                        'size': match,
                        'type': size_type
                    })
        
        # Activity level indicators
        activity_patterns = [
            (r'active group', 'high'),
            (r'new post', 'active'),
            (r'recent activity', 'recent'),
            (r'daily posts', 'very_active'),
            (r'weekly posts', 'active'),
            (r'quiet group', 'low')
        ]
        
        for pattern, activity_level in activity_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                analysis['activity_levels'].append(activity_level)
        
        # Privacy settings
        privacy_patterns = [
            (r'public group', 'public'),
            (r'private group', 'private'),
            (r'closed group', 'closed'),
            (r'secret group', 'secret'),
            (r'visible to everyone', 'public'),
            (r'hidden group', 'hidden')
        ]
        
        for pattern, privacy_type in privacy_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                analysis['privacy_settings'].append(privacy_type)
        
        return analysis
    
    def categorize_groups(self, html):
        """গ্রুপস ক্যাটেগোরাইজ"""
        categories = {
            'educational': 0,
            'professional': 0,
            'hobby': 0,
            'local': 0,
            'buy_sell': 0,
            'entertainment': 0,
            'support': 0,
            'other': 0
        }
        
        # Educational groups
        edu_keywords = ['university', 'college', 'school', 'learn', 'study', 'education', 'student', 'alumni']
        for keyword in edu_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['educational'] += 1
        
        # Professional groups
        prof_keywords = ['job', 'career', 'business', 'professional', 'network', 'industry', 'work']
        for keyword in prof_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['professional'] += 1
        
        # Hobby groups
        hobby_keywords = ['hobby', 'game', 'sports', 'music', 'art', 'photography', 'food', 'travel']
        for keyword in hobby_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['hobby'] += 1
        
        # Local groups
        local_keywords = ['local', 'community', 'neighborhood', 'city', 'area', 'town', 'village']
        for keyword in local_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['local'] += 1
        
        # Buy/sell groups
        buy_sell_keywords = ['buy', 'sell', 'market', 'sale', 'trade', 'exchange', 'commerce']
        for keyword in buy_sell_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['buy_sell'] += 1
        
        # Entertainment groups
        ent_keywords = ['movie', 'tv', 'celebrity', 'fan', 'fun', 'entertainment', 'comedy']
        for keyword in ent_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['entertainment'] += 1
        
        # Support groups
        support_keywords = ['support', 'help', 'therapy', 'mental', 'health', 'recovery', 'counseling']
        for keyword in support_keywords:
            if re.search(rf'\b{keyword}\b', html, re.IGNORECASE):
                categories['support'] += 1
        
        return categories
    
    def analyze_membership_patterns(self, html):
        """মেম্বারশিপ প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'group_overlap': 'unknown',
            'active_participation': 'unknown',
            'admin_roles': [],
            'membership_duration': 'unknown'
        }
        
        # Admin/moderator roles
        role_patterns = [
            (r'group admin', 'admin'),
            (r'group moderator', 'moderator'),
            (r'created this group', 'creator'),
            (r'group founder', 'founder')
        ]
        
        for pattern, role in role_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                patterns['admin_roles'].append(role)
        
        # Active participation indicators
        activity_indicators = [
            r'frequent poster',
            r'active member',
            r'regular contributor',
            r'recent post',
            r'commented on'
        ]
        
        active_count = 0
        for indicator in activity_indicators:
            if re.search(indicator, html, re.IGNORECASE):
                active_count += 1
        
        if active_count > 3:
            patterns['active_participation'] = 'high'
        elif active_count > 1:
            patterns['active_participation'] = 'medium'
        elif active_count > 0:
            patterns['active_participation'] = 'low'
        
        # Membership duration clues
        duration_patterns = [
            (r'member since \d{4}', 'long_term'),
            (r'joined \d+ years ago', 'long_term'),
            (r'new member', 'recent'),
            (r'joined recently', 'recent'),
            (r'joined \d+ months ago', 'medium_term')
        ]
        
        for pattern, duration in duration_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                patterns['membership_duration'] = duration
                break
        
        return patterns