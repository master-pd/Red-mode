# file: method_15_posts.py
import re
import json
from datetime import datetime
from collections import Counter

class PostsAnalyzer:
    """পোস্টস অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Posts Analyzer"
        
    def execute(self, html_content):
        """পোস্টস অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'posts_data': self.extract_posts_data(html_content),
                'post_patterns': self.analyze_post_patterns(html_content),
                'engagement_metrics': self.extract_engagement_metrics(html_content),
                'content_analysis': self.analyze_content(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_posts_data(self, html):
        """পোস্টস ডাটা এক্সট্র্যাক্ট"""
        posts_data = {
            'total_posts': 0,
            'posts_list': [],
            'post_dates': [],
            'post_types': []
        }
        
        # Facebook post patterns
        patterns = [
            # Post count
            r'(\d+)\s*posts',
            r'posts.*?(\d+)',
            
            # Post content
            r'data-testid="post_message"[^>]*>([^<]+)</div>',
            r'class=["\'][^"\']*userContent[^"\']*["\'][^>]*>([^<]+)<',
            r'<p[^>]*>([^<]+)</p>',
            
            # Post dates
            r'data-utime=["\'](\d+)["\']',
            r'abbr[^>]*title=["\']([^"\']+)["\']',
            r'timestamp[^>]*>([^<]+)<',
            
            # Post types
            r'data-testid=["\'][^"\']*(story|post|feed)[^"\']*["\']',
            r'role=["\']article["\']'
        ]
        
        # Extract post count
        for pattern in patterns[:2]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if count > posts_data['total_posts']:
                        posts_data['total_posts'] = count
                except:
                    pass
        
        # Extract post content
        post_contents = []
        for pattern in patterns[2:5]:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match.strip()) > 10:  # Minimum length
                    post_contents.append(match.strip())
        
        posts_data['posts_list'] = post_contents[:50]  # First 50 posts
        
        # Extract post dates
        for pattern in patterns[5:8]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match.isdigit():
                    # Unix timestamp
                    try:
                        dt = datetime.fromtimestamp(int(match))
                        posts_data['post_dates'].append(dt.strftime("%Y-%m-%d %H:%M:%S"))
                    except:
                        pass
                elif len(match.strip()) > 5:
                    posts_data['post_dates'].append(match.strip())
        
        # Extract post types
        post_type_indicators = {
            'status': ['updated', 'wrote', 'is feeling', 'added'],
            'photo': ['photo', 'picture', 'image', 'uploaded'],
            'video': ['video', 'watch', 'shared a video'],
            'link': ['shared a link', 'http://', 'https://'],
            'event': ['event', 'going to', 'interested in'],
            'checkin': ['at ', 'checked in', 'location']
        }
        
        for post in post_contents:
            for post_type, indicators in post_type_indicators.items():
                if any(indicator in post.lower() for indicator in indicators):
                    posts_data['post_types'].append(post_type)
                    break
        
        return posts_data
    
    def analyze_post_patterns(self, html):
        """পোস্ট প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'posting_frequency': 'unknown',
            'post_length_pattern': {},
            'time_patterns': [],
            'content_patterns': []
        }
        
        # Extract all post text
        all_posts_text = ' '.join(self.extract_posts_data(html)['posts_list'])
        
        # Post length analysis
        post_lengths = [len(post.split()) for post in self.extract_posts_data(html)['posts_list']]
        if post_lengths:
            patterns['post_length_pattern'] = {
                'average_length': sum(post_lengths) / len(post_lengths),
                'min_length': min(post_lengths),
                'max_length': max(post_lengths),
                'short_posts': len([p for p in post_lengths if p < 10]),
                'medium_posts': len([p for p in post_lengths if 10 <= p <= 50]),
                'long_posts': len([p for p in post_lengths if p > 50])
            }
        
        # Time patterns from dates
        dates = self.extract_posts_data(html)['post_dates']
        time_patterns = []
        
        for date_str in dates:
            if ':' in date_str:
                try:
                    # Extract hour
                    hour_match = re.search(r'(\d{1,2}):\d{2}', date_str)
                    if hour_match:
                        hour = int(hour_match.group(1))
                        if 5 <= hour < 12:
                            time_patterns.append('morning')
                        elif 12 <= hour < 17:
                            time_patterns.append('afternoon')
                        elif 17 <= hour < 22:
                            time_patterns.append('evening')
                        else:
                            time_patterns.append('night')
                except:
                    pass
        
        if time_patterns:
            time_counts = Counter(time_patterns)
            patterns['time_patterns'] = time_counts.most_common()
        
        # Content patterns
        content_keywords = {
            'questions': ['?', 'how', 'what', 'why', 'when', 'where', 'who'],
            'exclamations': ['!', 'wow', 'amazing', 'awesome'],
            'emotional': ['happy', 'sad', 'angry', 'excited', 'love', 'hate'],
            'sharing': ['shared', 'check this', 'look at', 'watch this'],
            'personal': ['I ', 'my ', 'me ', 'mine']
        }
        
        content_patterns = []
        for pattern_type, keywords in content_keywords.items():
            count = sum(1 for keyword in keywords if keyword.lower() in all_posts_text.lower())
            if count > 0:
                content_patterns.append((pattern_type, count))
        
        patterns['content_patterns'] = content_patterns
        
        return patterns
    
    def extract_engagement_metrics(self, html):
        """এনগেজমেন্ট মেট্রিক্স"""
        engagement = {
            'likes_count': 0,
            'comments_count': 0,
            'shares_count': 0,
            'reactions': {}
        }
        
        # Likes patterns
        like_patterns = [
            r'(\d+)\s*likes',
            r'likes.*?(\d+)',
            r'data-testid="UFI2ReactionsCount/sentence"[^>]*>([^<]+)<',
            r'(\d+)\s*people like this'
        ]
        
        for pattern in like_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    # Extract number from text like "1.2K" or "1,234"
                    if 'k' in match.lower():
                        num = float(match.lower().replace('k', '')) * 1000
                    elif 'm' in match.lower():
                        num = float(match.lower().replace('m', '')) * 1000000
                    else:
                        num = int(match.replace(',', ''))
                    
                    if num > engagement['likes_count']:
                        engagement['likes_count'] = num
                except:
                    pass
        
        # Comments patterns
        comment_patterns = [
            r'(\d+)\s*comments',
            r'comments.*?(\d+)',
            r'data-testid="UFI2CommentsCount/sentence"[^>]*>([^<]+)<'
        ]
        
        for pattern in comment_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    num = self.parse_count(match)
                    if num > engagement['comments_count']:
                        engagement['comments_count'] = num
                except:
                    pass
        
        # Shares patterns
        share_patterns = [
            r'(\d+)\s*shares',
            r'shares.*?(\d+)',
            r'shared (\d+) times'
        ]
        
        for pattern in share_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    num = self.parse_count(match)
                    if num > engagement['shares_count']:
                        engagement['shares_count'] = num
                except:
                    pass
        
        # Reactions analysis
        reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
        for reaction in reaction_types:
            pattern = rf'data-testid="{reaction}"'
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                engagement['reactions'][reaction] = len(matches)
        
        return engagement
    
    def parse_count(self, text):
        """টেক্সট থেকে নাম্বার পার্স"""
        text = str(text).lower().strip()
        
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        else:
            return int(text.replace(',', ''))
    
    def analyze_content(self, html):
        """কনটেন্ট অ্যানালাইসিস"""
        content_analysis = {
            'topics': [],
            'sentiment': 'neutral',
            'language_use': {},
            'hashtag_analysis': []
        }
        
        # Extract all text from posts
        all_text = ' '.join(self.extract_posts_data(html)['posts_list']).lower()
        
        # Topic analysis (common words)
        words = re.findall(r'\b\w{4,}\b', all_text)
        word_counts = Counter(words)
        
        # Common topics
        topics_keywords = {
            'technology': ['phone', 'computer', 'internet', 'tech', 'app', 'software'],
            'food': ['food', 'eat', 'restaurant', 'cook', 'recipe', 'meal'],
            'travel': ['travel', 'trip', 'vacation', 'hotel', 'flight', 'beach'],
            'sports': ['game', 'sport', 'team', 'player', 'score', 'win'],
            'music': ['song', 'music', 'band', 'concert', 'album', 'listen'],
            'family': ['family', 'mother', 'father', 'child', 'parent', 'kids']
        }
        
        topics_found = []
        for topic, keywords in topics_keywords.items():
            keyword_count = sum(1 for keyword in keywords if keyword in all_text)
            if keyword_count > 0:
                topics_found.append((topic, keyword_count))
        
        content_analysis['topics'] = sorted(topics_found, key=lambda x: x[1], reverse=True)
        
        # Basic sentiment analysis
        positive_words = ['happy', 'good', 'great', 'awesome', 'love', 'excited', 'best', 'perfect']
        negative_words = ['sad', 'bad', 'hate', 'angry', 'terrible', 'worst', 'problem', 'issue']
        
        positive_count = sum(1 for word in positive_words if word in all_text)
        negative_count = sum(1 for word in negative_words if word in all_text)
        
        if positive_count > negative_count * 2:
            content_analysis['sentiment'] = 'positive'
        elif negative_count > positive_count * 2:
            content_analysis['sentiment'] = 'negative'
        else:
            content_analysis['sentiment'] = 'neutral'
        
        # Language use analysis
        content_analysis['language_use'] = {
            'word_count': len(all_text.split()),
            'unique_words': len(set(all_text.split())),
            'avg_word_length': sum(len(word) for word in all_text.split()) / max(1, len(all_text.split()))
        }
        
        # Hashtag analysis
        hashtags = re.findall(r'#(\w+)', html, re.IGNORECASE)
        hashtag_counts = Counter(hashtags)
        content_analysis['hashtag_analysis'] = hashtag_counts.most_common(10)
        
        return content_analysis