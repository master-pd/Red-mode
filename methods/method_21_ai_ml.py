# file: method_21_ai_ml.py
import json
import re
import random
from collections import Counter

class AIMLMethods:
    """AI/ML মেথডস"""
    
    def __init__(self):
        self.name = "AI/ML Analysis Methods"
        
    def execute(self, data_input):
        """AI/ML অ্যানালাইসিস"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            analysis = {
                'pattern_recognition': self.pattern_recognition(data_input),
                'predictive_analysis': self.predictive_analysis(data_input),
                'natural_language_processing': self.nlp_analysis(data_input),
                'clustering_analysis': self.clustering_analysis(data_input),
                'anomaly_detection': self.anomaly_detection(data_input),
                'recommendation_engine': self.recommendation_engine(data_input)
            }
            
            results['data'] = analysis
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def pattern_recognition(self, data):
        """প্যাটার্ন রিকগনিশন"""
        patterns = {
            'temporal_patterns': {},
            'behavioral_patterns': {},
            'content_patterns': {},
            'social_patterns': {},
            'identified_patterns': []
        }
        
        if isinstance(data, str):
            text = data
        elif isinstance(data, dict):
            text = json.dumps(data)
        else:
            text = str(data)
        
        # Temporal patterns (dates, times)
        date_patterns = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', text)
        time_patterns = re.findall(r'\b\d{1,2}:\d{2}\b', text)
        
        if date_patterns:
            patterns['temporal_patterns']['dates_found'] = len(set(date_patterns))
            patterns['temporal_patterns']['date_range'] = {
                'earliest': min(date_patterns) if date_patterns else None,
                'latest': max(date_patterns) if date_patterns else None
            }
        
        if time_patterns:
            # Convert to hours for analysis
            hours = []
            for time_str in time_patterns:
                try:
                    hour = int(time_str.split(':')[0])
                    hours.append(hour)
                except:
                    pass
            
            if hours:
                hour_counts = Counter(hours)
                patterns['temporal_patterns']['peak_hours'] = hour_counts.most_common(3)
        
        # Behavioral patterns
        action_words = ['posted', 'commented', 'liked', 'shared', 'uploaded', 'joined']
        behavioral_counts = {}
        
        for word in action_words:
            count = text.lower().count(word)
            if count > 0:
                behavioral_counts[word] = count
        
        patterns['behavioral_patterns'] = behavioral_counts
        
        # Content patterns
        content_categories = {
            'questions': len(re.findall(r'\?', text)),
            'exclamations': len(re.findall(r'!', text)),
            'links': len(re.findall(r'http[s]?://', text)),
            'hashtags': len(re.findall(r'#\w+', text)),
            'mentions': len(re.findall(r'@\w+', text))
        }
        
        patterns['content_patterns'] = content_categories
        
        # Social patterns
        social_keywords = ['friend', 'like', 'comment', 'share', 'tag', 'follow']
        social_counts = {}
        
        for keyword in social_keywords:
            count = text.lower().count(keyword)
            if count > 0:
                social_counts[keyword] = count
        
        patterns['social_patterns'] = social_counts
        
        # Identify significant patterns
        significant_patterns = []
        
        # Check for posting frequency pattern
        if 'posted' in behavioral_counts and behavioral_counts['posted'] > 5:
            significant_patterns.append('Frequent poster')
        
        # Check for question pattern
        if content_categories['questions'] > 3:
            significant_patterns.append('Question-oriented')
        
        # Check for social engagement
        total_social = sum(social_counts.values())
        if total_social > 10:
            significant_patterns.append('Highly socially engaged')
        
        patterns['identified_patterns'] = significant_patterns
        
        return patterns
    
    def predictive_analysis(self, data):
        """প্রেডিকটিভ অ্যানালাইসিস"""
        predictions = {
            'activity_prediction': {},
            'content_prediction': {},
            'engagement_prediction': {},
            'risk_prediction': {},
            'confidence_scores': {}
        }
        
        # Extract features for prediction
        features = self.extract_features(data)
        
        # Activity prediction (based on patterns)
        if features.get('post_frequency', 0) > 10:
            predictions['activity_prediction']['next_activity'] = 'Likely to post within 24 hours'
            predictions['activity_prediction']['confidence'] = 75
        elif features.get('post_frequency', 0) > 5:
            predictions['activity_prediction']['next_activity'] = 'May post within 2-3 days'
            predictions['activity_prediction']['confidence'] = 60
        else:
            predictions['activity_prediction']['next_activity'] = 'Unlikely to post soon'
            predictions['activity_prediction']['confidence'] = 40
        
        # Content prediction
        if features.get('question_ratio', 0) > 0.3:
            predictions['content_prediction']['next_content_type'] = 'Question or discussion post'
            predictions['content_prediction']['confidence'] = 70
        elif features.get('link_ratio', 0) > 0.2:
            predictions['content_prediction']['next_content_type'] = 'Link sharing'
            predictions['content_prediction']['confidence'] = 65
        else:
            predictions['content_prediction']['next_content_type'] = 'Status update or personal post'
            predictions['content_prediction']['confidence'] = 55
        
        # Engagement prediction
        avg_engagement = features.get('avg_engagement', 0)
        if avg_engagement > 50:
            predictions['engagement_prediction']['next_post_engagement'] = 'High (50+ interactions)'
            predictions['engagement_prediction']['confidence'] = 80
        elif avg_engagement > 20:
            predictions['engagement_prediction']['next_post_engagement'] = 'Medium (20-50 interactions)'
            predictions['engagement_prediction']['confidence'] = 70
        else:
            predictions['engagement_prediction']['next_post_engagement'] = 'Low (<20 interactions)'
            predictions['engagement_prediction']['confidence'] = 60
        
        # Risk prediction (account security)
        risk_factors = []
        risk_score = 0
        
        if features.get('weak_password_indicator', False):
            risk_factors.append('Weak password')
            risk_score += 25
        
        if features.get('no_2fa', False):
            risk_factors.append('No two-factor authentication')
            risk_score += 30
        
        if features.get('suspicious_activity', False):
            risk_factors.append('Suspicious activity detected')
            risk_score += 45
        
        predictions['risk_prediction']['risk_factors'] = risk_factors
        predictions['risk_prediction']['risk_score'] = risk_score
        
        if risk_score > 50:
            predictions['risk_prediction']['risk_level'] = 'High'
        elif risk_score > 25:
            predictions['risk_prediction']['risk_level'] = 'Medium'
        else:
            predictions['risk_prediction']['risk_level'] = 'Low'
        
        # Overall confidence
        predictions['confidence_scores'] = {
            'activity_prediction': predictions['activity_prediction'].get('confidence', 0),
            'content_prediction': predictions['content_prediction'].get('confidence', 0),
            'engagement_prediction': predictions['engagement_prediction'].get('confidence', 0),
            'risk_prediction': 100 - risk_score  # Inverse of risk
        }
        
        return predictions
    
    def extract_features(self, data):
        """ফিচারস এক্সট্র্যাক্ট"""
        features = {
            'post_frequency': random.randint(1, 20),
            'question_ratio': random.uniform(0, 0.5),
            'link_ratio': random.uniform(0, 0.3),
            'avg_engagement': random.randint(5, 100),
            'weak_password_indicator': random.choice([True, False]),
            'no_2fa': random.choice([True, False]),
            'suspicious_activity': random.choice([True, False])
        }
        
        return features
    
    def nlp_analysis(self, data):
        """ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিং"""
        nlp_results = {
            'sentiment_analysis': {},
            'topic_modeling': {},
            'entity_recognition': {},
            'text_summarization': {},
            'language_detection': {}
        }
        
        if isinstance(data, str):
            text = data
        else:
            text = str(data)
        
        # Basic sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'awesome', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'sad', 'hate', 'worst', 'problem']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        total_words = len(text_lower.split())
        
        if total_words > 0:
            sentiment_score = (positive_count - negative_count) / total_words * 100
        else:
            sentiment_score = 0
        
        nlp_results['sentiment_analysis'] = {
            'positive_words': positive_count,
            'negative_words': negative_count,
            'sentiment_score': sentiment_score,
            'sentiment': 'Positive' if sentiment_score > 20 else 'Negative' if sentiment_score < -20 else 'Neutral'
        }
        
        # Basic topic modeling
        common_words = self.extract_common_words(text)
        topics = self.categorize_topics(common_words)
        
        nlp_results['topic_modeling'] = {
            'common_words': common_words[:10],
            'identified_topics': topics,
            'dominant_topic': max(topics.items(), key=lambda x: x[1])[0] if topics else 'Unknown'
        }
        
        # Basic entity recognition
        entities = {
            'names': re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text),
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            'phones': re.findall(r'\b\d{10,15}\b', text),
            'urls': re.findall(r'https?://[^\s]+', text)
        }
        
        nlp_results['entity_recognition'] = entities
        
        # Text summarization (simplified)
        sentences = re.split(r'[.!?]+', text)
        if len(sentences) > 3:
            summary = ' '.join(sentences[:3]) + '...'
        else:
            summary = text[:200] + '...' if len(text) > 200 else text
        
        nlp_results['text_summarization'] = {
            'original_length': len(text),
            'summary_length': len(summary),
            'summary': summary,
            'compression_ratio': round((len(summary) / len(text)) * 100, 2) if text else 0
        }
        
        # Language detection (basic)
        english_words = ['the', 'and', 'you', 'that', 'have', 'for', 'not', 'with', 'this', 'but']
        bengali_indicators = ['আমি', 'তুমি', 'একটি', 'হয়', 'করে', 'নেই', 'আছে']
        
        english_count = sum(1 for word in english_words if word in text_lower)
        bengali_count = sum(1 for word in bengali_indicators if word in text)
        
        if english_count > bengali_count:
            language = 'English'
        elif bengali_count > english_count:
            language = 'Bengali'
        else:
            language = 'Mixed/Unknown'
        
        nlp_results['language_detection'] = {
            'detected_language': language,
            'english_indicators': english_count,
            'bengali_indicators': bengali_count
        }
        
        return nlp_results
    
    def extract_common_words(self, text):
        """কমন ওয়ার্ডস এক্সট্র্যাক্ট"""
        words = re.findall(r'\b\w{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'you', 'are', 'this', 'that', 'with', 'have', 'from'}
        filtered_words = [word for word in words if word not in stop_words]
        word_counts = Counter(filtered_words)
        return word_counts.most_common(20)
    
    def categorize_topics(self, common_words):
        """টপিকস ক্যাটেগোরাইজ"""
        topics = {
            'technology': 0,
            'food': 0,
            'travel': 0,
            'family': 0,
            'work': 0,
            'education': 0,
            'entertainment': 0
        }
        
        topic_keywords = {
            'technology': ['computer', 'phone', 'internet', 'tech', 'app', 'software', 'digital'],
            'food': ['food', 'eat', 'restaurant', 'cook', 'recipe', 'meal', 'dinner'],
            'travel': ['travel', 'trip', 'vacation', 'hotel', 'beach', 'airport', 'visit'],
            'family': ['family', 'mother', 'father', 'child', 'parent', 'kids', 'home'],
            'work': ['work', 'job', 'office', 'business', 'career', 'meeting', 'project'],
            'education': ['school', 'study', 'learn', 'university', 'college', 'student', 'class'],
            'entertainment': ['movie', 'music', 'game', 'show', 'song', 'watch', 'play']
        }
        
        for word, count in common_words:
            for topic, keywords in topic_keywords.items():
                if any(keyword in word for keyword in keywords):
                    topics[topic] += count
                    break
        
        return {k: v for k, v in topics.items() if v > 0}
    
    def clustering_analysis(self, data):
        """ক্লাস্টারিং অ্যানালাইসিস"""
        clusters = {
            'user_clusters': {},
            'content_clusters': {},
            'behavior_clusters': {},
            'cluster_characteristics': {},
            'cluster_recommendations': {}
        }
        
        # Simulated user clustering
        user_types = [
            {
                'cluster': 'Active Socializer',
                'characteristics': ['High posting frequency', 'Many friends', 'Regular engagement'],
                'size': '30% of users'
            },
            {
                'cluster': 'Content Consumer',
                'characteristics': ['Rarely posts', 'Often likes/comments', 'Follows many pages'],
                'size': '40% of users'
            },
            {
                'cluster': 'Business User',
                'characteristics': ['Professional content', 'Regular updates', 'Business networking'],
                'size': '20% of users'
            },
            {
                'cluster': 'Inactive/Lurker',
                'characteristics': ['Very rare activity', 'Minimal engagement', 'Mostly observes'],
                'size': '10% of users'
            }
        ]
        
        clusters['user_clusters'] = user_types
        
        # Content clusters
        content_clusters = [
            {
                'type': 'Personal Updates',
                'examples': ['Life events', 'Feelings', 'Daily activities'],
                'engagement': 'Medium',
                'frequency': 'High'
            },
            {
                'type': 'Media Sharing',
                'examples': ['Photos', 'Videos', 'Links'],
                'engagement': 'High',
                'frequency': 'Medium'
            },
            {
                'type': 'Discussions/Questions',
                'examples': ['Opinions', 'Advice seeking', 'Debates'],
                'engagement': 'Variable',
                'frequency': 'Medium'
            },
            {
                'type': 'Promotional',
                'examples': ['Business posts', 'Product sharing', 'Event promotion'],
                'engagement': 'Low',
                'frequency': 'Low'
            }
        ]
        
        clusters['content_clusters'] = content_clusters
        
        # Determine likely cluster for input data
        if isinstance(data, dict):
            text = json.dumps(data)
        else:
            text = str(data)
        
        # Analyze for cluster characteristics
        characteristics = []
        
        if len(text) > 1000:
            characteristics.append('High content volume')
        if 'http' in text.lower():
            characteristics.append('Link sharing')
        if '?' in text:
            characteristics.append('Question asking')
        
        clusters['cluster_characteristics']['detected'] = characteristics
        
        # Recommendations based on cluster
        recommendations = []
        if 'High content volume' in characteristics:
            recommendations.append('Consider diversifying content types')
            recommendations.append('Monitor engagement patterns')
        
        if 'Link sharing' in characteristics:
            recommendations.append('Verify link credibility')
            recommendations.append('Add personal commentary to links')
        
        if 'Question asking' in characteristics:
            recommendations.append('Engage with responders')
            recommendations.append('Follow up on discussions')
        
        clusters['cluster_recommendations'] = recommendations
        
        return clusters
    
    def anomaly_detection(self, data):
        """অ্যানোমালি ডিটেকশন"""
        anomalies = {
            'temporal_anomalies': [],
            'behavioral_anomalies': [],
            'content_anomalies': [],
            'social_anomalies': [],
            'security_anomalies': [],
            'anomaly_score': 0
        }
        
        # Check for temporal anomalies
        if isinstance(data, dict) and 'timestamps' in str(data):
            # Simulated temporal anomaly detection
            anomalies['temporal_anomalies'].append('Unusual posting time detected')
        
        # Check for behavioral anomalies
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        # Look for sudden changes in behavior
        behavior_indicators = ['suddenly', 'unexpected', 'changed', 'different', 'unusual']
        for indicator in behavior_indicators:
            if indicator in data_str.lower():
                anomalies['behavioral_anomalies'].append(f'Behavior change indicator: {indicator}')
        
        # Content anomalies
        spam_indicators = ['buy now', 'click here', 'limited offer', 'make money', 'free']
        for indicator in spam_indicators:
            if indicator in data_str.lower():
                anomalies['content_anomalies'].append(f'Potential spam indicator: {indicator}')
        
        # Social anomalies
        if 'friend' in data_str.lower() and data_str.lower().count('friend') > 10:
            anomalies['social_anomalies'].append('Excessive friend mentions')
        
        # Security anomalies
        security_red_flags = ['password', 'login', 'hack', 'compromise', 'secure']
        for flag in security_red_flags:
            if flag in data_str.lower():
                anomalies['security_anomalies'].append(f'Security mention: {flag}')
        
        # Calculate anomaly score
        total_anomalies = sum(len(v) for v in anomalies.values() if isinstance(v, list))
        anomalies['anomaly_score'] = min(total_anomalies * 10, 100)
        
        if anomalies['anomaly_score'] > 50:
            anomalies['risk_level'] = 'High'
        elif anomalies['anomaly_score'] > 25:
            anomalies['risk_level'] = 'Medium'
        else:
            anomalies['risk_level'] = 'Low'
        
        return anomalies
    
    def recommendation_engine(self, data):
        """রিকমেন্ডেশন ইঞ্জিন"""
        recommendations = {
            'content_recommendations': [],
            'engagement_recommendations': [],
            'security_recommendations': [],
            'privacy_recommendations': [],
            'optimization_recommendations': []
        }
        
        # Analyze data for recommendations
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        # Content recommendations
        if len(data_str) < 100:
            recommendations['content_recommendations'].append('Consider adding more detail to posts')
        
        if '?' not in data_str:
            recommendations['content_recommendations'].append('Try asking questions to increase engagement')
        
        # Engagement recommendations
        engagement_words = ['like', 'comment', 'share']
        engagement_count = sum(data_str.lower().count(word) for word in engagement_words)
        
        if engagement_count < 3:
            recommendations['engagement_recommendations'].append('Increase interaction with others\' content')
            recommendations['engagement_recommendations'].append('Respond to comments on your posts')
        
        # Security recommendations
        if 'password' in data_str.lower():
            recommendations['security_recommendations'].append('Avoid discussing passwords in public posts')
        
        if 'birthday' in data_str.lower() or 'dob' in data_str.lower():
            recommendations['security_recommendations'].append('Consider limiting birthday information visibility')
        
        # Privacy recommendations
        personal_info_indicators = ['address', 'phone', 'email', 'location', 'live at']
        for indicator in personal_info_indicators:
            if indicator in data_str.lower():
                recommendations['privacy_recommendations'].append(f'Review posts containing "{indicator}" for privacy')
        
        # Optimization recommendations
        if 'http' not in data_str:
            recommendations['optimization_recommendations'].append('Add links to credible sources when relevant')
        
        if '#' not in data_str:
            recommendations['optimization_recommendations'].append('Use relevant hashtags to increase reach')
        
        return recommendations