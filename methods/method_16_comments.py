# file: method_16_comments.py
import re
import json
from collections import Counter
from datetime import datetime

class CommentsAnalyzer:
    """কমেন্টস অ্যানালাইজার"""
    
    def __init__(self):
        self.name = "Comments Analyzer"
        
    def execute(self, html_content):
        """কমেন্টস অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'comments_data': self.extract_comments_data(html_content),
                'comment_patterns': self.analyze_comment_patterns(html_content),
                'commenter_analysis': self.analyze_commenters(html_content),
                'engagement_analysis': self.analyze_comment_engagement(html_content)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def extract_comments_data(self, html):
        """কমেন্টস ডাটা এক্সট্র্যাক্ট"""
        comments_data = {
            'total_comments': 0,
            'comments_list': [],
            'commenters': [],
            'comment_dates': []
        }
        
        # Facebook comments patterns
        patterns = [
            # Comments count
            r'(\d+)\s*comments',
            r'comments.*?(\d+)',
            r'data-testid="UFI2CommentsCount/sentence"[^>]*>([^<]+)<',
            
            # Comment content
            r'data-testid="comment"[^>]*>([^<]+)</div>',
            r'class=["\'][^"\']*comment[^"\']*["\'][^>]*>([^<]+)<',
            r'role="comment"[^>]*>([^<]+)<',
            r'<span[^>]*>([^<]+)</span>.*?comment',
            
            # Commenter names
            r'data-testid="comment_author"[^>]*>([^<]+)</a>',
            r'comment.*?profile[^>]*>([^<]+)<',
            r'<a[^>]*>([^<]+)</a>.*?commented',
            
            # Comment dates
            r'data-utime=["\'](\d+)["\'].*?comment',
            r'comment.*?timestamp[^>]*>([^<]+)<',
            r'abbr[^>]*title=["\']([^"\']+)["\'].*?comment'
        ]
        
        # Extract comments count
        for pattern in patterns[:3]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    if isinstance(match, tuple):
                        match = match[0]
                    num = self.parse_count(match)
                    if num > comments_data['total_comments']:
                        comments_data['total_comments'] = num
                except:
                    pass
        
        # Extract comment content
        comment_contents = []
        for pattern in patterns[3:7]:
            matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match.strip()) > 5:
                    comment_contents.append(match.strip())
        
        comments_data['comments_list'] = comment_contents[:100]  # First 100 comments
        
        # Extract commenter names
        commenter_names = set()
        for pattern in patterns[7:10]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 2:
                    commenter_names.add(match.strip())
        
        comments_data['commenters'] = list(commenter_names)
        
        # Extract comment dates
        comment_dates = []
        for pattern in patterns[10:]:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if match:
                    comment_dates.append(match.strip())
        
        comments_data['comment_dates'] = comment_dates
        
        return comments_data
    
    def parse_count(self, text):
        """কাউন্ট টেক্সট পার্স"""
        text = str(text).lower().strip()
        
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        elif 'b' in text:
            return int(float(text.replace('b', '')) * 1000000000)
        else:
            # Remove commas and convert
            return int(text.replace(',', '').replace('.', ''))
    
    def analyze_comment_patterns(self, html):
        """কমেন্ট প্যাটার্ন অ্যানালাইসিস"""
        patterns = {
            'comment_length_stats': {},
            'comment_types': {},
            'reply_patterns': [],
            'thread_depth': 0
        }
        
        # Get comments
        comments = self.extract_comments_data(html)['comments_list']
        
        if comments:
            # Comment length analysis
            comment_lengths = [len(comment.split()) for comment in comments]
            patterns['comment_length_stats'] = {
                'total_comments': len(comments),
                'average_length': sum(comment_lengths) / len(comments),
                'min_length': min(comment_lengths),
                'max_length': max(comment_lengths),
                'short_comments': len([c for c in comment_lengths if c < 5]),
                'medium_comments': len([c for c in comment_lengths if 5 <= c <= 20]),
                'long_comments': len([c for c in comment_lengths if c > 20])
            }
            
            # Comment type analysis
            comment_types = {
                'question': 0,
                'answer': 0,
                'agreement': 0,
                'disagreement': 0,
                'emoticon': 0,
                'link': 0
            }
            
            for comment in comments:
                comment_lower = comment.lower()
                
                # Questions
                if '?' in comment:
                    comment_types['question'] += 1
                
                # Answers (often contain "because", "so", "therefore")
                if any(word in comment_lower for word in ['because', 'so', 'therefore', 'thus']):
                    comment_types['answer'] += 1
                
                # Agreement
                if any(word in comment_lower for word in ['yes', 'agree', 'true', 'correct', 'right']):
                    comment_types['agreement'] += 1
                
                # Disagreement
                if any(word in comment_lower for word in ['no', 'disagree', 'wrong', 'false', 'incorrect']):
                    comment_types['disagreement'] += 1
                
                # Emoticons/emojis
                if any(char in comment for char in ['😀', '😂', '😊', '😍', '😎', '😢', '😠']):
                    comment_types['emoticon'] += 1
                elif any(pattern in comment for pattern in [':)', ':(', ':D', ';)']):
                    comment_types['emoticon'] += 1
                
                # Links
                if 'http://' in comment_lower or 'https://' in comment_lower:
                    comment_types['link'] += 1
            
            patterns['comment_types'] = comment_types
            
            # Reply patterns (look for nested comments)
            reply_patterns = [
                r'reply to',
                r'replied to',
                r'in reply to',
                r'> >',  # Nested quotes
                r'@\w+'  # Mentions
            ]
            
            reply_counts = []
            for pattern in reply_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                reply_counts.append(len(matches))
            
            patterns['reply_patterns'] = {
                'total_reply_indicators': sum(reply_counts),
                'reply_types_found': [p for p, c in zip(reply_patterns, reply_counts) if c > 0]
            }
            
            # Thread depth (estimate from indentation)
            depth_patterns = [
                r'margin-left:\s*(\d+)px',
                r'padding-left:\s*(\d+)px',
                r'indent:\s*(\d+)'
            ]
            
            depths = []
            for pattern in depth_patterns:
                matches = re.findall(pattern, html)
                for match in matches:
                    try:
                        depth = int(match) // 20  # Approximate depth level
                        depths.append(depth)
                    except:
                        pass
            
            if depths:
                patterns['thread_depth'] = max(depths)
        
        return patterns
    
    def analyze_commenters(self, html):
        """কমেন্টার অ্যানালাইসিস"""
        commenter_analysis = {
            'top_commenters': [],
            'comment_frequency': {},
            'commenter_engagement': {}
        }
        
        # Extract commenter names and their comments
        commenter_patterns = [
            r'data-testid="comment_author"[^>]*>([^<]+)</a>',
            r'<a[^>]*>([^<]+)</a>.*?commented'
        ]
        
        all_commenters = []
        for pattern in commenter_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            all_commenters.extend(matches)
        
        if all_commenters:
            # Top commenters
            commenter_counts = Counter(all_commenters)
            commenter_analysis['top_commenters'] = commenter_counts.most_common(10)
            
            # Comment frequency analysis
            total_comments = len(all_commenters)
            unique_commenters = len(set(all_commenters))
            
            commenter_analysis['comment_frequency'] = {
                'total_comments': total_comments,
                'unique_commenters': unique_commenters,
                'avg_comments_per_user': total_comments / unique_commenters if unique_commenters > 0 else 0,
                'most_active_user': commenter_counts.most_common(1)[0] if commenter_counts else None
            }
        
        # Commenter engagement patterns
        engagement_patterns = {
            'multiple_comments': len([c for c in all_commenters if all_commenters.count(c) > 1]),
            'single_comment': len([c for c in all_commenters if all_commenters.count(c) == 1]),
            'conversation_starter': 0,
            'conversation_ender': 0
        }
        
        commenter_analysis['commenter_engagement'] = engagement_patterns
        
        return commenter_analysis
    
    def analyze_comment_engagement(self, html):
        """কমেন্ট এনগেজমেন্ট অ্যানালাইসিস"""
        engagement = {
            'likes_on_comments': 0,
            'replies_to_comments': 0,
            'comment_chains': [],
            'engagement_timing': {}
        }
        
        # Likes on comments
        like_patterns = [
            r'(\d+)\s*like.*?comment',
            r'comment.*?(\d+)\s*like',
            r'data-testid="UFI2CommentLikeCount"[^>]*>([^<]+)<'
        ]
        
        comment_likes = []
        for pattern in like_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    likes = self.parse_count(match)
                    comment_likes.append(likes)
                except:
                    pass
        
        if comment_likes:
            engagement['likes_on_comments'] = {
                'total_likes': sum(comment_likes),
                'average_likes': sum(comment_likes) / len(comment_likes),
                'max_likes': max(comment_likes),
                'comments_with_likes': len(comment_likes)
            }
        
        # Replies to comments
        reply_patterns = [
            r'(\d+)\s*reply',
            r'reply.*?(\d+)',
            r'data-testid="UFI2CommentReplyCount"[^>]*>([^<]+)<'
        ]
        
        comment_replies = []
        for pattern in reply_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                try:
                    replies = self.parse_count(match)
                    comment_replies.append(replies)
                except:
                    pass
        
        if comment_replies:
            engagement['replies_to_comments'] = {
                'total_replies': sum(comment_replies),
                'average_replies': sum(comment_replies) / len(comment_replies),
                'max_replies': max(comment_replies),
                'comments_with_replies': len(comment_replies)
            }
        
        # Comment chains (conversation threads)
        chain_patterns = [
            r'comment thread',
            r'conversation',
            r'thread.*?\d+\s*comments'
        ]
        
        chains_found = []
        for pattern in chain_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                chains_found.append(pattern)
        
        engagement['comment_chains'] = chains_found
        
        # Engagement timing (from comment dates)
        dates = self.extract_comments_data(html)['comment_dates']
        time_patterns = {'morning': 0, 'afternoon': 0, 'evening': 0, 'night': 0}
        
        for date_str in dates:
            if ':' in date_str:
                try:
                    hour_match = re.search(r'(\d{1,2}):\d{2}', date_str)
                    if hour_match:
                        hour = int(hour_match.group(1))
                        if 5 <= hour < 12:
                            time_patterns['morning'] += 1
                        elif 12 <= hour < 17:
                            time_patterns['afternoon'] += 1
                        elif 17 <= hour < 22:
                            time_patterns['evening'] += 1
                        else:
                            time_patterns['night'] += 1
                except:
                    pass
        
        engagement['engagement_timing'] = time_patterns
        
        return engagement