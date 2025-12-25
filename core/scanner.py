# file: core/scanner.py
import time
import json
from typing import List, Dict, Any
import concurrent.futures

class Scanner:
    """কোর স্ক্যানার ইঞ্জিন"""
    
    def __init__(self):
        self.methods = []
        self.results = {}
        self.scan_stats = {
            'total_methods': 0,
            'completed': 0,
            'failed': 0,
            'start_time': None,
            'end_time': None
        }
    
    def register_method(self, method):
        """মেথড রেজিস্টার"""
        self.methods.append(method)
        
    def scan(self, target, methods=None, max_workers=5):
        """মেইন স্ক্যান ফাংশন"""
        self.scan_stats['start_time'] = time.time()
        
        # যদি নির্দিষ্ট মেথড না থাকে, সব মেথড
        methods_to_run = methods or self.methods
        
        self.scan_stats['total_methods'] = len(methods_to_run)
        
        print(f"\n🎯 Target: {target}")
        print(f"📊 Methods to run: {len(methods_to_run)}")
        print("-" * 60)
        
        # প্যারালাল এক্সিকিউশন
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_method = {
                executor.submit(method.execute, target): method 
                for method in methods_to_run
            }
            
            for future in concurrent.futures.as_completed(future_to_method):
                method = future_to_method[future]
                
                try:
                    result = future.result()
                    
                    if result.get('success'):
                        self.scan_stats['completed'] += 1
                        self.results[method.name] = result['data']
                        print(f"✅ {method.name}: Success")
                    else:
                        self.scan_stats['failed'] += 1
                        print(f"❌ {method.name}: Failed")
                        
                except Exception as e:
                    self.scan_stats['failed'] += 1
                    print(f"💥 {method.name}: Error - {str(e)}")
        
        self.scan_stats['end_time'] = time.time()
        
        return self.results
    
    def get_stats(self):
        """স্ট্যাটস দেখান"""
        elapsed = self.scan_stats['end_time'] - self.scan_stats['start_time']
        
        stats = {
            'total_methods': self.scan_stats['total_methods'],
            'completed': self.scan_stats['completed'],
            'failed': self.scan_stats['failed'],
            'success_rate': f"{(self.scan_stats['completed'] / self.scan_stats['total_methods'] * 100):.2f}%",
            'elapsed_time': f"{elapsed:.2f} seconds",
            'methods_per_second': f"{self.scan_stats['completed'] / elapsed:.2f}"
        }
        
        return stats
    
    def save_scan_results(self, filename="scan_results.json"):
        """স্ক্যান রেজাল্টস সেভ"""
        output = {
            'stats': self.get_stats(),
            'results': self.results,
            'timestamp': time.time(),
            'scan_complete': True
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to {filename}")
        return filename