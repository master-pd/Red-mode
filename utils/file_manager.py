# file: utils/file_manager.py
import os
import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import zipfile

class FileManager:
    """ফাইল ম্যানেজমেন্ট ইউটিলিটি"""
    
    def __init__(self, base_directory="mar_pd_data"):
        self.base_dir = Path(base_directory)
        self.setup_directories()
        
    def setup_directories(self):
        """ডিরেক্টরি সেটআপ"""
        directories = [
            'scans',
            'exports',
            'logs',
            'cache',
            'reports',
            'backups',
            'config',
            'temp'
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Directories setup complete at: {self.base_dir}")
    
    def save_scan_result(self, data, filename=None, category="general"):
        """স্ক্যান রেজাল্ট সেভ"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_{timestamp}.json"
        
        # Ensure proper extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Determine save path
        save_dir = self.base_dir / "scans" / category
        save_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = save_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Scan result saved: {filepath}")
            return {
                'success': True,
                'filepath': str(filepath),
                'size': os.path.getsize(filepath),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error saving scan result: {e}")
            return {'success': False, 'error': str(e)}
    
    def load_scan_result(self, filename, category="general"):
        """স্ক্যান রেজাল্ট লোড"""
        filepath = self.base_dir / "scans" / category / filename
        
        if not filepath.exists():
            print(f"❌ File not found: {filepath}")
            return {'success': False, 'error': 'File not found'}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"✅ Scan result loaded: {filepath}")
            return {
                'success': True,
                'data': data,
                'filepath': str(filepath),
                'size': os.path.getsize(filepath),
                'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error loading scan result: {e}")
            return {'success': False, 'error': str(e)}
    
    def list_scan_results(self, category="general"):
        """স্ক্যান রেজাল্টস লিস্ট"""
        scan_dir = self.base_dir / "scans" / category
        
        if not scan_dir.exists():
            return {'success': False, 'error': 'Directory not found'}
        
        files = []
        for file_path in scan_dir.glob("*.json"):
            file_info = {
                'filename': file_path.name,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'created': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            }
            files.append(file_info)
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)
        
        return {
            'success': True,
            'category': category,
            'total_files': len(files),
            'files': files
        }
    
    def export_data(self, data, export_format='json', filename=None):
        """ডাটা এক্সপোর্ট"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}"
        
        export_dir = self.base_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        if export_format in ['json', 'all']:
            json_file = export_dir / f"{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            results['json'] = str(json_file)
        
        if export_format in ['txt', 'all']:
            txt_file = export_dir / f"{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                self.write_text_export(data, f)
            results['txt'] = str(txt_file)
        
        if export_format in ['csv', 'all']:
            csv_file = export_dir / f"{filename}.csv"
            self.write_csv_export(data, csv_file)
            results['csv'] = str(csv_file)
        
        # Create ZIP if multiple formats
        if export_format == 'all' and len(results) > 1:
            zip_file = export_dir / f"{filename}.zip"
            with zipfile.ZipFile(zip_file, 'w') as zipf:
                for format_name, filepath in results.items():
                    zipf.write(filepath, os.path.basename(filepath))
            results['zip'] = str(zip_file)
        
        print(f"✅ Export completed: {results}")
        return {'success': True, 'exports': results}
    
    def write_text_export(self, data, file_handle):
        """টেক্সট এক্সপোর্ট লিখুন"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    file_handle.write(f"\n{key}:\n")
                    file_handle.write("-" * 40 + "\n")
                    file_handle.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
                else:
                    file_handle.write(f"{key}: {value}\n")
        else:
            file_handle.write(str(data))
    
    def write_csv_export(self, data, filepath):
        """CSV এক্সপোর্ট লিখুন"""
        try:
            import pandas as pd
            
            # Flatten data for CSV
            flat_data = self.flatten_dict_for_csv(data)
            
            if flat_data:
                df = pd.DataFrame(flat_data)
                df.to_csv(filepath, index=False, encoding='utf-8')
            else:
                # Create simple CSV if data is not dict/list
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("data\n")
                    f.write(str(data))
                    
        except ImportError:
            # Fallback if pandas not available
            with open(filepath, 'w', encoding='utf-8') as f:
                if isinstance(data, dict):
                    headers = list(data.keys())
                    f.write(','.join(headers) + '\n')
                    values = [str(v) for v in data.values()]
                    f.write(','.join(values) + '\n')
                else:
                    f.write("value\n")
                    f.write(str(data) + "\n")
    
    def flatten_dict_for_csv(self, data, parent_key='', sep='_'):
        """CSV এর জন্য ডিকশনারি ফ্ল্যাটেন"""
        items = []
        
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(self.flatten_dict_for_csv(v, new_key, sep))
                elif isinstance(v, list):
                    # Handle lists
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            items.extend(self.flatten_dict_for_csv(item, f"{new_key}_{i}", sep))
                        else:
                            items.append({new_key: str(v)})
                    break
                else:
                    items.append({new_key: v})
        
        return items
    
    def create_backup(self, backup_name=None):
        """ব্যাকআপ তৈরি"""
        if backup_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
        
        backup_dir = self.base_dir / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        backup_file = backup_dir / f"{backup_name}.zip"
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup scans
                scans_dir = self.base_dir / "scans"
                if scans_dir.exists():
                    for root, dirs, files in os.walk(scans_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(self.base_dir)
                            zipf.write(file_path, arcname)
                
                # Backup config
                config_dir = self.base_dir / "config"
                if config_dir.exists():
                    for root, dirs, files in os.walk(config_dir):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(self.base_dir)
                            zipf.write(file_path, arcname)
                
                # Add backup info
                backup_info = {
                    'backup_name': backup_name,
                    'created': datetime.now().isoformat(),
                    'total_size': os.path.getsize(backup_file) if backup_file.exists() else 0,
                    'directories_backed_up': ['scans', 'config']
                }
                
                zipf.writestr('backup_info.json', json.dumps(backup_info, indent=2))
            
            print(f"✅ Backup created: {backup_file}")
            return {
                'success': True,
                'backup_file': str(backup_file),
                'size': os.path.getsize(backup_file),
                'info': backup_info
            }
            
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def restore_backup(self, backup_filename):
        """ব্যাকআপ রিস্টোর"""
        backup_dir = self.base_dir / "backups"
        backup_file = backup_dir / backup_filename
        
        if not backup_file.exists():
            return {'success': False, 'error': 'Backup file not found'}
        
        # Create restore directory
        restore_dir = self.base_dir / "restore" / datetime.now().strftime("%Y%m%d_%H%M%S")
        restore_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(restore_dir)
            
            # Read backup info
            backup_info_path = restore_dir / "backup_info.json"
            if backup_info_path.exists():
                with open(backup_info_path, 'r') as f:
                    backup_info = json.load(f)
            else:
                backup_info = {'unknown': 'No backup info found'}
            
            print(f"✅ Backup restored to: {restore_dir}")
            return {
                'success': True,
                'restore_location': str(restore_dir),
                'backup_info': backup_info,
                'files_restored': len(os.listdir(restore_dir))
            }
            
        except Exception as e:
            print(f"❌ Backup restore failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def cleanup_old_files(self, days_old=30, categories=None):
        """পুরানো ফাইল ক্লিনআপ"""
        if categories is None:
            categories = ['scans', 'cache', 'temp', 'exports']
        
        cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        cleanup_report = {}
        
        for category in categories:
            category_dir = self.base_dir / category
            
            if not category_dir.exists():
                continue
            
            deleted_files = []
            deleted_size = 0
            
            for file_path in category_dir.rglob("*"):
                if file_path.is_file():
                    file_age = os.path.getmtime(file_path)
                    
                    if file_age < cutoff_date:
                        try:
                            file_size = file_path.stat().st_size
                            file_path.unlink()
                            deleted_files.append(file_path.name)
                            deleted_size += file_size
                        except Exception as e:
                            print(f"❌ Error deleting {file_path}: {e}")
            
            cleanup_report[category] = {
                'deleted_files': len(deleted_files),
                'deleted_size': deleted_size,
                'file_list': deleted_files[:10]  # First 10 files
            }
        
        print(f"✅ Cleanup completed for files older than {days_old} days")
        return {'success': True, 'cleanup_report': cleanup_report}
    
    def calculate_directory_size(self, directory=None):
        """ডিরেক্টরি সাইজ ক্যালকুলেট"""
        if directory is None:
            directory = self.base_dir
        
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return {'success': False, 'error': 'Directory not found'}
        
        total_size = 0
        file_count = 0
        dir_count = 0
        
        for root, dirs, files in os.walk(dir_path):
            dir_count += len(dirs)
            for file in files:
                file_path = Path(root) / file
                try:
                    total_size += file_path.stat().st_size
                    file_count += 1
                except:
                    pass
        
        return {
            'success': True,
            'directory': str(dir_path),
            'total_size': total_size,
            'size_human': self.format_size(total_size),
            'file_count': file_count,
            'directory_count': dir_count
        }
    
    def format_size(self, size_bytes):
        """সাইজ ফরম্যাট"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def search_in_files(self, search_term, file_pattern="*.json", category="scans"):
        """ফাইলে সার্চ"""
        search_dir = self.base_dir / category
        
        if not search_dir.exists():
            return {'success': False, 'error': 'Directory not found'}
        
        results = []
        
        for file_path in search_dir.rglob(file_pattern):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if search_term.lower() in content.lower():
                    # Find context around search term
                    lines = content.split('\n')
                    matches = []
                    
                    for i, line in enumerate(lines):
                        if search_term.lower() in line.lower():
                            context_start = max(0, i - 2)
                            context_end = min(len(lines), i + 3)
                            context = '\n'.join(lines[context_start:context_end])
                            matches.append({
                                'line_number': i + 1,
                                'context': context
                            })
                    
                    results.append({
                        'file': str(file_path.relative_to(self.base_dir)),
                        'matches_found': len(matches),
                        'matches': matches[:3],  # First 3 matches
                        'file_size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                    
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        
        print(f"✅ Search completed. Found {len(results)} files containing '{search_term}'")
        return {
            'success': True,
            'search_term': search_term,
            'total_results': len(results),
            'results': results
        }
    
    def get_file_hash(self, filepath, algorithm='sha256'):
        """ফাইল হ্যাশ পান"""
        file_path = Path(filepath)
        
        if not file_path.exists():
            return {'success': False, 'error': 'File not found'}
        
        hash_func = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                # Read file in chunks for large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            
            file_hash = hash_func.hexdigest()
            
            return {
                'success': True,
                'file': str(file_path),
                'algorithm': algorithm,
                'hash': file_hash,
                'size': file_path.stat().st_size
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}