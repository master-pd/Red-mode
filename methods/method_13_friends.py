# file: method_13_friends.py
import re
import json
from collections import Counter

class FriendsAnalyzer:
    """ফ্রেন্ডস লিস্ট অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Friends List Analyzer"
        
    def execute(self, html_content):
        """ফ্রেন্ডস লিস্ট অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'friends_data': self.extract_friends_data(html_content),
                'mutual_friends': self.find_mutual_friends(html_content),
                'friends_patterns': self.analyze_friends_patterns(html_content),
                'network_analysis': self.analyze_friends_network(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_friends_data(self, html):
        """ফ্রেন্ডস ডাটা এক্সট্র্যাক্ট"""
        friends_data = {
            'total_friends': 0,
            'friends_list': [],
            'friends_urls': []
        }
        
        # Facebook friends patterns
        patterns = [
            # Friends count
            r'(\d+[,]?\d*)\s*friends',
            r'friends.*?(\d+[,]?\d*)',
            
            # Friends list items
            r'<a[^>]*href=["\']/[^"\']+["\'][^>]*>([^<]+)</a>.*?friends',
            r'data-testid="friend_list_item"[^>]*>([^<]+)</div>',
            r'class=["\'][^"\']*friend[^"\']*["\'][^>]*>([^<]+)<',
            
            # Friend profile URLs
            r'href=["\']/([^"\']+)\?.*?fref=fr_tab',
            r'href=["\']/(profile\.php\?id=\d+)',
            r'href=["\']/([^"\']+)\?.*?friend'
        ]
        
        # Extract friends count
        for pattern in patterns[:2]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match.replace(',', ''))
                    if count > friends_data['total_friends']:
                        friends_data['total_friends'] = count
                except:
                    pass
        
        # Extract friend names
        friend_names = set()
        for pattern in patterns[2:5]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 2:
                    friend_names.add(match.strip())
        
        friends_data['friends_list'] = list(friend_names)
        
        # Extract friend URLs
        friend_urls = set()
        for pattern in patterns[5:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match and 'facebook.com' not in match:
                    friend_urls.add(f"https://facebook.com/{match}")
        
        friends_data['friends_urls'] = list(friend_urls)
        
        return friends_data
    
    def find_mutual_friends(self, html):
        """মিউচুয়াল ফ্রেন্ডস খোঁজা"""
        mutual_data = {
            'mutual_friends_count': 0,
            'mutual_friends_list': [],
            'mutual_friends_texts': []
        }
        
        # Mutual friends patterns
        patterns = [
            r'(\d+)\s*mutual friends',
            r'mutual friends.*?(\d+)',
            r'(\d+)\s*friends in common',
            r'<div[^>]*>(\d+) mutual friend',
            r'has (\d+) mutual friend'
        ]
        
        # Extract mutual friends count
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if count > mutual_data['mutual_friends_count']:
                        mutual_data['mutual_friends_count'] = count
                except:
                    pass
        
        # Find mutual friends names in text
        text_patterns = [
            r'mutual friends?[^<]*<[^>]*>([^<]+)<',
            r'friend in common[^<]*<[^>]*>([^<]+)<',
            r'knows ([^<,]+)'
        ]
        
        for pattern in text_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            mutual_data['mutual_friends_texts'].extend(matches)
        
        return mutual_data
    
    def analyze_friends_patterns(self, html):
        """ফ্রেন্ডস প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'common_first_names': [],
            'common_last_names': [],
            'name_patterns': [],
            'geographic_patterns': []
        }
        
        # Extract all names from friends list
        all_names = []
        name_pattern = r'<a[^>]*>([A-Z][a-z]+ [A-Z][a-z]+)</a>'
        matches = re.findall(name_pattern, html)
        all_names.extend(matches)
        
        if all_names:
            # Analyze first names
            first_names = [name.split()[0] for name in all_names if ' ' in name]
            first_name_counts = Counter(first_names)
            patterns['common_first_names'] = first_name_counts.most_common(10)
            
            # Analyze last names
            last_names = [name.split()[-1] for name in all_names if ' ' in name]
            last_name_counts = Counter(last_names)
            patterns['common_last_names'] = last_name_counts.most_common(10)
            
            # Name patterns
            patterns['name_patterns'] = {
                'two_part_names': len([n for n in all_names if len(n.split()) == 2]),
                'three_part_names': len([n for n in all_names if len(n.split()) == 3]),
                'with_middle_initial': len([n for n in all_names if re.search(r'[A-Z]\.', n)])
            }
        
        # Geographic patterns (from location mentions)
        location_patterns = [
            r'from ([^<,]+)',
            r'lives in ([^<,]+)',
            r'in ([^<,]+)'
        ]
        
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            locations.extend(matches)
        
        if locations:
            location_counts = Counter(locations)
            patterns['geographic_patterns'] = location_counts.most_common(10)
        
        return patterns
    
    def analyze_friends_network(self, html):
        """ফ্রেন্ডস নেটওয়ার্ক অ্যানালাইসিস"""
        network_analysis = {
            'network_size': 'small',
            'connectivity_pattern': 'unknown',
            'community_clusters': []
        }
        
        # Extract friend connections data
        connection_patterns = [
            r'(\d+)\s*friends of friends',
            r'connected to (\d+) people',
            r'network of (\d+)'
        ]
        
        connection_counts = []
        for pattern in connection_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    connection_counts.append(int(match))
                except:
                    pass
        
        if connection_counts:
            max_connections = max(connection_counts)
            
            # Determine network size
            if max_connections > 1000:
                network_analysis['network_size'] = 'large'
            elif max_connections > 500:
                network_analysis['network_size'] = 'medium'
            else:
                network_analysis['network_size'] = 'small'
        
        # Look for community/cluster indicators
        cluster_patterns = [
            r'close friends',
            r'family',
            r'work',
            r'school',
            r'hometown'
        ]
        
        clusters_found = []
        for pattern in cluster_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                clusters_found.append(pattern)
        
        network_analysis['community_clusters'] = clusters_found
        
        return network_analysis