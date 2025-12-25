# file: method_02_graphql.py
import json
import requests
import re

class GraphQLScanner:
    """Facebook GraphQL Scanner"""
    
    def __init__(self):
        self.name = "GraphQL API Scanner"
        self.base_url = "https://graph.facebook.com"
        
    def execute(self, user_id=None, access_token=None):
        """GraphQL API স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            # পাবলিক GraphQL queries
            queries = self.get_public_queries()
            
            data = {}
            
            # প্রতিটি query চেষ্টা করা
            for query_name, query in queries.items():
                try:
                    response = self.make_graphql_request(query, user_id, access_token)
                    if response:
                        data[query_name] = response
                except:
                    continue
            
            if data:
                results['data'] = data
                results['success'] = True
                
        except Exception as e:
            results['errors'].append(str(e))
            
        return results
    
    def get_public_queries(self):
        """পাবলিকলি অ্যাভেইলেবল GraphQL queries"""
        queries = {
            'public_profile': """
                query {
                    user(id: "%s") {
                        id
                        name
                        profile_picture {
                            uri
                        }
                    }
                }
            """,
            'friends_count': """
                query {
                    user(id: "%s") {
                        friends {
                            total_count
                        }
                    }
                }
            """
        }
        return queries
    
    def make_graphql_request(self, query, user_id, token=None):
        """GraphQL রিকুয়েস্ট"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        
        if token:
            headers['Authorization'] = f'Bearer {token}'
            
        payload = {
            'query': query % user_id if user_id else query
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/graphql",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
            
        return None