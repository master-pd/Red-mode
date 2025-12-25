# file: method_10_backup.py
import requests
import re
from urllib.parse import urljoin, urlparse
import concurrent.futures

class BackupScanner:
    """Backup File Scanner"""
    
    def __init__(self):
        self.name = "Backup File Scanner"
        self.common_backups = [
            # Common backup patterns
            'backup', 'backup.zip', 'backup.tar', 'backup.tar.gz',
            'backup.rar', 'backup.7z', 'backup.bak',
            'database', 'database.sql', 'database.sql.gz',
            'db', 'db.sql', 'db.sql.gz', 'db.backup',
            'www', 'www.zip', 'www.tar', 'www.tar.gz',
            'site', 'site.zip', 'site.tar', 'site.tar.gz',
            'web', 'web.zip', 'web.tar', 'web.tar.gz',
            'admin', 'admin.zip', 'admin.tar', 'admin.tar.gz',
            
            # Facebook specific
            'facebook_backup', 'fb_backup', 'profile_backup',
            'data_export', 'facebook_export', 'fb_export',
            'user_data', 'user_backup',
            
            # Common extensions
            '.zip', '.tar', '.tar.gz', '.rar', '.7z',
            '.bak', '.backup', '.old', '.tmp',
            '.sql', '.sql.gz', '.db', '.mdb',
            '.json', '.xml', '.csv'
        ]
        
    def execute(self, base_url):
        """Backup ফাইল স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            # URL পরিষ্কার করা
            parsed = urlparse(base_url)
            base_domain = f"{parsed.scheme}://{parsed.netloc}"
            
            # সম্ভাব্য backup পাথ তৈরি
            backup_urls = self.generate_backup_urls(base_domain, parsed.path)
            
            # Parallel checking
            found_backups = self.check_urls_parallel(backup_urls)
            
            results['data'] = {
                'base_url': base_url,
                'backup_urls_generated': len(backup_urls),
                'found_backups': found_backups,
                'tested_urls': backup_urls[:50]  # প্রথম ৫০টা URL
            }
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def generate_backup_urls(self, base_domain, path):
        """Backup URLs জেনারেট"""
        backup_urls = []
        
        # Path থেকে ডিরেক্টরি বের করা
        directories = []
        parts = path.strip('/').split('/')
        
        for i in range(len(parts)):
            dir_path = '/' + '/'.join(parts[:i+1])
            directories.append(dir_path)
        
        # প্রতিটি ডিরেক্টরির জন্য backup URLs
        for directory in directories:
            for backup in self.common_backups:
                # Full path backup
                backup_urls.append(urljoin(base_domain, f"{directory}/{backup}"))
                # Directory backup
                backup_urls.append(urljoin(base_domain, f"{directory}.{backup}"))
                # With version
                backup_urls.append(urljoin(base_domain, f"{directory}_backup.{backup}"))
        
        # Root directory backups
        for backup in self.common_backups:
            backup_urls.append(urljoin(base_domain, backup))
            backup_urls.append(urljoin(base_domain, f"www/{backup}"))
            backup_urls.append(urljoin(base_domain, f"public/{backup}"))
            backup_urls.append(urljoin(base_domain, f"html/{backup}"))
        
        # Facebook specific backups
        fb_backups = [
            'facebook_export.zip', 'fb_data.zip', 'user_backup.zip',
            'profile_data.zip', 'timeline_backup.zip'
        ]
        
        for fb_backup in fb_backups:
            backup_urls.append(urljoin(base_domain, fb_backup))
        
        return list(set(backup_urls))  # Remove duplicates
    
    def check_urls_parallel(self, urls, max_workers=10):
        """Parallel URL checking"""
        found = []
        
        def check_url(url):
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    # Content type check
                    content_type = response.headers.get('content-type', '')
                    content_length = response.headers.get('content-length', '0')
                    
                    # যদি ফাইল বড় হয় (likely backup)
                    if int(content_length) > 1000:
                        return {
                            'url': url,
                            'status': response.status_code,
                            'content_type': content_type,
                            'size': content_length
                        }
            except:
                pass
            return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(check_url, url): url for url in urls[:100]}  # প্রথম ১০০টা চেক
            
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                if result:
                    found.append(result)
        
        return found
    
    def check_backup_patterns(self, html_content):
        """HTML থেকে backup লিংক খোঁজা"""
        patterns = [
            r'href=["\'][^"\']*\.(zip|tar|gz|rar|7z|bak|sql)["\']',
            r'href=["\'][^"\']*backup[^"\']*["\']',
            r'href=["\'][^"\']*download[^"\']*["\']',
            r'href=["\'][^"\']*export[^"\']*["\']',
            r'data-file=["\'][^"\']*\.(zip|tar|gz|rar|7z)["\']',
            r'backup.*?href=["\']([^"\']+)["\']',
            r'download.*?href=["\']([^"\']+)["\']'
        ]
        
        found_links = []
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match and 'http' in match:
                    found_links.append(match)
        
        return list(set(found_links))