# file: method_17_likes.py
import re
import json
from collections import Counter

class LikesAnalyzer:
    """লাইকস অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Likes Analyzer"
        
    def execute(self, html_content):
        """লাইকস অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'likes_data': self.extract_likes_data(html_content),
                'likes_patterns': self.analyze_likes_patterns(html_content),
                'reactions_analysis': self.analyze_reactions(html_content),
                'engagement_rate': self.calculate_engagement_rate(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_likes_data(self, html):
        """লাইকস ডাটা এক্সট্র্যাক্ট"""
        likes_data = {
            'total_likes': 0,
            'likes_details': [],
            'liked_pages': [],
            'recent_likes': []
        }
        
        # Facebook likes patterns
        patterns = [
            # Total likes count
            r'(\d+[,]?\d*)\s*likes',
            r'likes.*?(\d+[,]?\d*)',
            r'(\d+)\s*people like this',
            r'data-testid="page_likes"[^>]*>([^<]+)<',
            
            # Page likes
            r'likes.*?<a[^>]*>([^<]+)</a>',
            r'page.*?liked[^>]*>([^<]+)<',
            r'data-testid="page_like_item"[^>]*>([^<]+)<',
            
            # Reaction details
            r'data-testid="(\w+)_reaction"[^>]*>',
            r'reaction.*?type="(\w+)"',
            
            # Like timestamps
            r'liked.*?on ([^<]+)<',
            r'timestamp.*?like[^>]*>([^<]+)<'
        ]
        
        # Extract total likes
        for pattern in patterns[:4]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    if isinstance(match, tuple):
                        match = match[0]
                    likes = self.parse_like_count(match)
                    if likes > likes_data['total_likes']:
                        likes_data['total_likes'] = likes
                except:
                    pass
        
        # Extract liked pages
        page_names = set()
        for pattern in patterns[4:7]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 2:
                    page_names.add(match.strip())
        
        likes_data['liked_pages'] = list(page_names)
        
        # Extract reaction types
        reactions = []
        for pattern in patterns[7:9]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            reactions.extend(matches)
        
        likes_data['reactions_details'] = Counter(reactions)
        
        # Extract like timestamps
        timestamps = []
        for pattern in patterns[9:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            timestamps.extend(matches)
        
        likes_data['recent_likes'] = timestamps[:10]  # Last 10 likes
        
        return likes_data
    
    def parse_like_count(self, text):
        """লাইক কাউন্ট পার্স"""
        text = str(text).lower().strip()
        
        if 'k' in text:
            return int(float(text.replace('k', '').replace(',', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '').replace(',', '')) * 1000000)
        elif 'b' in text:
            return int(float(text.replace('b', '').replace(',', '')) * 1000000000)
        else:
            return int(text.replace(',', ''))
    
    def analyze_likes_patterns(self, html):
        """লাইক প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'like_distribution': {},
            'like_frequency': 'unknown',
            'page_categories': {},
            'temporal_patterns': []
        }
        
        # Get liked pages
        liked_pages = self.extract_likes_data(html)['liked_pages']
        
        if liked_pages:
            # Categorize liked pages
            categories = {
                'entertainment': ['movie', 'tv', 'music', 'celebrity', 'show', 'film'],
                'sports': ['sports', 'team', 'player', 'game', 'league', 'tournament'],
                'technology': ['tech', 'gadget', 'app', 'software', 'computer', 'mobile'],
                'food': ['food', 'restaurant', 'recipe', 'cooking', 'chef', 'cuisine'],
                'shopping': ['shop', 'store', 'brand', 'fashion', 'clothing', 'buy'],
                'education': ['school', 'university', 'college', 'learn', 'course', 'education'],
                'news': ['news', 'media', 'newspaper', 'channel', 'journal', 'report']
            }
            
            category_counts = {cat: 0 for cat in categories.keys()}
            
            for page in liked_pages:
                page_lower = page.lower()
                for category, keywords in categories.items():
                    if any(keyword in page_lower for keyword in keywords):
                        category_counts[category] += 1
                        break
            
            patterns['page_categories'] = {k: v for k, v in category_counts.items() if v > 0}
            
            # Like distribution analysis
            total_pages = len(liked_pages)
            patterns['like_distribution'] = {
                'total_liked_pages': total_pages,
                'unique_categories': len([c for c in category_counts.values() if c > 0]),
                'most_liked_category': max(category_counts.items(), key=lambda x: x[1]) if any(category_counts.values()) else ('none', 0)
            }
        
        # Like frequency estimation
        like_frequency_patterns = [
            (r'frequent.*?likes', 'high'),
            (r'regular.*?liker', 'high'),
            (r'occasional.*?likes', 'medium'),
            (r'rare.*?likes', 'low'),
            (r'new.*?liker', 'recent')
        ]
        
        for pattern, frequency in like_frequency_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                patterns['like_frequency'] = frequency
                break
        
        # Temporal patterns from timestamps
        timestamps = self.extract_likes_data(html)['recent_likes']
        
        if timestamps:
            # Extract day parts from timestamps
            day_parts = []
            for ts in timestamps:
                if 'am' in ts.lower():
                    day_parts.append('morning')
                elif 'pm' in ts.lower():
                    hour_match = re.search(r'(\d+)\s*pm', ts.lower())
                    if hour_match:
                        hour = int(hour_match.group(1))
                        if hour < 6:
                            day_parts.append('afternoon')
                        else:
                            day_parts.append('evening')
                elif ':' in ts:
                    hour_match = re.search(r'(\d+):', ts)
                    if hour_match:
                        hour = int(hour_match.group(1))
                        if 5 <= hour < 12:
                            day_parts.append('morning')
                        elif 12 <= hour < 17:
                            day_parts.append('afternoon')
                        elif 17 <= hour < 22:
                            day_parts.append('evening')
                        else:
                            day_parts.append('night')
            
            if day_parts:
                day_part_counts = Counter(day_parts)
                patterns['temporal_patterns'] = day_part_counts.most_common()
        
        return patterns
    
    def analyze_reactions(self, html):
        """রিঅ্যাকশন্স অ্যানালাইসিস"""
        reactions_analysis = {
            'reaction_types': {},
            'reaction_distribution': {},
            'most_common_reaction': 'unknown',
            'reaction_patterns': []
        }
        
        # Standard Facebook reactions
        standard_reactions = ['like', 'love', 'wow', 'haha', 'sad', 'angry', 'care']
        
        # Count each reaction type
        reaction_counts = {}
        for reaction in standard_reactions:
            patterns = [
                rf'data-testid="{reaction}_reaction"',
                rf'reaction.*?{reaction}',
                rf'aria-label.*?{reaction}'
            ]
            
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                count += len(matches)
            
            if count > 0:
                reaction_counts[reaction] = count
        
        reactions_analysis['reaction_types'] = reaction_counts
        
        if reaction_counts:
            # Reaction distribution
            total_reactions = sum(reaction_counts.values())
            reactions_analysis['reaction_distribution'] = {
                'total_reactions': total_reactions,
                'reaction_percentages': {k: (v/total_reactions)*100 for k, v in reaction_counts.items()},
                'most_common_reaction': max(reaction_counts.items(), key=lambda x: x[1])[0] if reaction_counts else 'none'
            }
            
            # Reaction patterns
            patterns_detected = []
            
            # Emotional pattern
            emotional_reactions = ['love', 'haha', 'sad', 'angry', 'wow']
            emotional_count = sum(reaction_counts.get(r, 0) for r in emotional_reactions)
            if emotional_count > reaction_counts.get('like', 0):
                patterns_detected.append('emotional_engagement')
            
            # Positive pattern
            positive_reactions = ['like', 'love', 'haha', 'wow', 'care']
            positive_count = sum(reaction_counts.get(r, 0) for r in positive_reactions)
            negative_reactions = ['sad', 'angry']
            negative_count = sum(reaction_counts.get(r, 0) for r in negative_reactions)
            
            if positive_count > negative_count * 3:
                patterns_detected.append('highly_positive')
            elif negative_count > positive_count:
                patterns_detected.append('negative_trend')
            
            reactions_analysis['reaction_patterns'] = patterns_detected
        
        return reactions_analysis
    
    def calculate_engagement_rate(self, html):
        """এনগেজমেন্ট রেট ক্যালকুলেশন"""
        engagement = {
            'estimated_rate': 0,
            'engagement_level': 'low',
            'factors_considered': [],
            'comparison_metrics': {}
        }
        
        # Extract various metrics
        total_likes = self.extract_likes_data(html)['total_likes']
        
        # Try to estimate followers/viewers
        follower_patterns = [
            r'(\d+[,]?\d*)\s*followers',
            r'(\d+[,]?\d*)\s*people.*?follow',
            r'followers.*?(\d+[,]?\d*)'
        ]
        
        estimated_followers = 0
        for pattern in follower_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    followers = self.parse_like_count(match)
                    if followers > estimated_followers:
                        estimated_followers = followers
                except:
                    pass
        
        # Calculate engagement rate if we have both metrics
        if estimated_followers > 0 and total_likes > 0:
            engagement_rate = (total_likes / estimated_followers) * 100
            engagement['estimated_rate'] = round(engagement_rate, 2)
            
            # Determine engagement level
            if engagement_rate > 10:
                engagement['engagement_level'] = 'very_high'
            elif engagement_rate > 5:
                engagement['engagement_level'] = 'high'
            elif engagement_rate > 2:
                engagement['engagement_level'] = 'medium'
            elif engagement_rate > 0.5:
                engagement['engagement_level'] = 'low'
            else:
                engagement['engagement_level'] = 'very_low'
            
            engagement['factors_considered'].append('likes_vs_followers')
        
        # Look for other engagement indicators
        other_indicators = [
            (r'high.*?engagement', 'high_engagement_mentioned'),
            (r'viral.*?post', 'viral_content'),
            (r'trending', 'trending'),
            (r'popular.*?post', 'popular_content')
        ]
        
        for pattern, indicator in other_indicators:
            if re.search(pattern, html, re.IGNORECASE):
                engagement['factors_considered'].append(indicator)
        
        # Comparison metrics
        engagement['comparison_metrics'] = {
            'total_likes': total_likes,
            'estimated_followers': estimated_followers,
            'liked_pages_count': len(self.extract_likes_data(html)['liked_pages']),
            'reaction_types_count': len(self.extract_likes_data(html)['reactions_details'])
        }
        
        return engagement