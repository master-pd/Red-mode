# file: method_07_cache.py
import os
import json
import sqlite3
import re
from pathlib import Path
import browser_cookie3

class CacheScanner:
    """Browser Cache and Cookie Scanner"""
    
    def __init__(self):
        self.name = "Cache and Cookie Scanner"
        self.supported_browsers = ['chrome', 'firefox', 'edge', 'brave', 'opera']
        
    def execute(self, browser_name=None):
        """Cache এবং Cookie স্ক্যান"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            cache_data = {}
            
            # নির্দিষ্ট ব্রাউজার বা সব ব্রাউজার স্ক্যান
            if browser_name:
                browsers_to_scan = [browser_name]
            else:
                browsers_to_scan = self.supported_browsers
            
            for browser in browsers_to_scan:
                try:
                    browser_data = self.scan_browser(browser)
                    if browser_data:
                        cache_data[browser] = browser_data
                except Exception as e:
                    results['errors'].append(f"{browser}: {str(e)}")
            
            # লোকাল ফাইল ক্যাশে চেক
            cache_data['local_cache'] = self.scan_local_cache()
            
            results['data'] = cache_data
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def scan_browser(self, browser_name):
        """ব্রাউজার স্ক্যান"""
        browser_data = {
            'cookies': [],
            'cache_info': {},
            'facebook_data': []
        }
        
        try:
            # Cookies extract
            cookies = self.get_browser_cookies(browser_name)
            if cookies:
                browser_data['cookies'] = self.filter_facebook_cookies(cookies)
            
            # Cache directory check
            cache_dir = self.get_browser_cache_dir(browser_name)
            if cache_dir and os.path.exists(cache_dir):
                browser_data['cache_info'] = {
                    'path': cache_dir,
                    'size': self.get_directory_size(cache_dir),
                    'files': len(list(Path(cache_dir).rglob('*')))
                }
                
                # Facebook related files
                fb_files = self.find_facebook_files(cache_dir)
                browser_data['facebook_data'] = fb_files
                
        except Exception as e:
            browser_data['error'] = str(e)
        
        return browser_data
    
    def get_browser_cookies(self, browser_name):
        """ব্রাউজার কুকি সংগ্রহ"""
        try:
            if browser_name == 'chrome':
                return browser_cookie3.chrome()
            elif browser_name == 'firefox':
                return browser_cookie3.firefox()
            elif browser_name == 'edge':
                return browser_cookie3.edge()
            elif browser_name == 'brave':
                return browser_cookie3.brave()
            elif browser_name == 'opera':
                return browser_cookie3.opera()
        except:
            return None
        
        return None
    
    def filter_facebook_cookies(self, cookies):
        """ফেসবুক কুকি ফিল্টার"""
        fb_cookies = []
        
        for cookie in cookies:
            if 'facebook' in cookie.domain.lower():
                fb_cookies.append({
                    'name': cookie.name,
                    'value': cookie.value[:50] + '...' if len(cookie.value) > 50 else cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'expires': str(cookie.expires) if cookie.expires else 'Session',
                    'secure': cookie.secure,
                    'http_only': cookie.http_only
                })
        
        return fb_cookies
    
    def get_browser_cache_dir(self, browser_name):
        """ব্রাউজার ক্যাশে ডিরেক্টরি"""
        home = str(Path.home())
        
        paths = {
            'chrome': {
                'linux': f'{home}/.config/google-chrome/Default/Cache',
                'mac': f'{home}/Library/Application Support/Google/Chrome/Default/Cache',
                'windows': f'{home}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'
            },
            'firefox': {
                'linux': f'{home}/.mozilla/firefox/*.default/cache2',
                'mac': f'{home}/Library/Caches/Firefox/Profiles/*.default',
                'windows': f'{home}\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\*.default\\cache2'
            }
        }
        
        import platform
        system = platform.system().lower()
        
        if browser_name in paths and system in paths[browser_name]:
            return paths[browser_name][system]
        
        return None
    
    def get_directory_size(self, path):
        """ডিরেক্টরি সাইজ"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_directory_size(entry.path)
        except:
            pass
        return total
    
    def find_facebook_files(self, cache_dir):
        """ফেসবুক ফাইল খোঁজা"""
        fb_files = []
        patterns = ['facebook', 'fb.com', 'fbcdn']
        
        try:
            for file_path in Path(cache_dir).rglob('*'):
                if file_path.is_file():
                    filename = file_path.name.lower()
                    if any(pattern in filename for pattern in patterns):
                        try:
                            fb_files.append({
                                'file': str(file_path),
                                'size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime
                            })
                        except:
                            pass
        except:
            pass
        
        return fb_files[:20]  # প্রথম ২০টা ফাইল
    
    def scan_local_cache(self):
        """লোকাল ক্যাশে স্ক্যান"""
        local_cache = {
            'temp_files': [],
            'recent_files': [],
            'browser_data': []
        }
        
        import tempfile
        temp_dir = tempfile.gettempdir()
        
        # টেম্প ফাইল লিস্ট
        try:
            for entry in os.scandir(temp_dir):
                if entry.is_file():
                    local_cache['temp_files'].append({
                        'name': entry.name,
                        'size': entry.stat().st_size
                    })
        except:
            pass
        
        # Recent files (শেষ ২৪ ঘণ্টা)
        import time
        day_ago = time.time() - 86400
        
        try:
            for entry in os.scandir(temp_dir):
                if entry.is_file() and entry.stat().st_mtime > day_ago:
                    local_cache['recent_files'].append({
                        'name': entry.name,
                        'size': entry.stat().st_size,
                        'modified': time.ctime(entry.stat().st_mtime)
                    })
        except:
            pass
        
        return local_cache