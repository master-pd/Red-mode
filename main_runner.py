# file: main_runner.py
import os
import sys
import importlib
import glob
import json
import time

class SmartRunner:
    """Smart Method Runner - Auto-discovers all methods"""
    
    def __init__(self):
        self.methods_dir = os.path.dirname(__file__)
        self.methods = []
        self.results = []
        
    def discover_methods(self):
        """অটো ডিসকভার মেথড"""
        print("🔍 Discovering methods...")
        
        # method_*.py ফাইল খোঁজা
        pattern = os.path.join(self.methods_dir, "method_*.py")
        method_files = glob.glob(pattern)
        
        for file_path in method_files:
            filename = os.path.basename(file_path)
            method_name = filename[:-3]  # .py remove
            
            # __init__ skip
            if method_name == "method___init__":
                continue
                
            self.methods.append(method_name)
            print(f"   ✅ Found: {method_name}")
            
        print(f"\n📊 Total methods found: {len(self.methods)}")
        return self.methods
    
    def load_method(self, method_name):
        """ডাইনামিক লোড মেথড"""
        try:
            module = importlib.import_module(method_name)
            
            # ক্লাস খোঁজা
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, '__call__') and not attr_name.startswith('_'):
                    # Check if it's a class
                    if hasattr(attr, '__name__'):
                        if 'Analyzer' in attr.__name__ or 'Scanner' in attr.__name__:
                            return attr
            
            # If no specific class found, use first class
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):  # It's a class
                    return attr
                    
        except Exception as e:
            print(f"   ❌ Error loading {method_name}: {e}")
            
        return None
    
    def run_method(self, method_class, method_name, **kwargs):
        """রান সিঙ্গেল মেথড"""
        try:
            print(f"\n🚀 Running {method_name}...")
            
            # Instantiate class
            instance = method_class()
            
            # Check for execute method
            if hasattr(instance, 'execute'):
                result = instance.execute(**kwargs)
            elif hasattr(instance, 'run'):
                result = instance.run(**kwargs)
            else:
                # Try calling directly
                result = instance(**kwargs)
                
            self.results.append({
                'method': method_name,
                'result': result,
                'timestamp': time.time()
            })
            
            print(f"   ✅ {method_name} completed")
            return result
            
        except Exception as e:
            print(f"   ❌ {method_name} failed: {e}")
            return None
    
    def run_all_methods(self, target=None, **kwargs):
        """রান অল মেথড"""
        print("\n" + "="*60)
        print("🤖 MAR-PD Smart Runner")
        print("="*60)
        
        # Discover methods
        self.discover_methods()
        
        print(f"\n🎯 Target: {target if target else 'Not specified'}")
        
        # Run each method
        for method_name in self.methods:
            method_class = self.load_method(method_name)
            
            if method_class:
                if target:
                    kwargs['target'] = target
                    
                self.run_method(method_class, method_name, **kwargs)
            else:
                print(f"   ⚠️ Skipping {method_name} (no class found)")
        
        # Save results
        self.save_results()
        
        print(f"\n✅ Completed! Total methods run: {len(self.results)}")
        return self.results
    
    def save_results(self, filename="runner_results.json"):
        """রেজাল্টস সেভ"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to {filename}")

# মেইন ফাংশন
if __name__ == "__main__":
    runner = SmartRunner()
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                 MAR-PD Smart Runner v3.0                 ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # টার্গেট ইনপুট
    target = input("Enter target (URL/ID/Username): ").strip()
    
    if target:
        runner.run_all_methods(target=target)
    else:
        runner.run_all_methods()