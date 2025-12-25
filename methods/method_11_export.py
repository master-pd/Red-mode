# file: method_11_export.py
import json
import csv
import pandas as pd
from datetime import datetime
import zipfile
import os

class DataExporter:
    """ডাটা এক্সপোর্ট মেথড"""
    
    def __init__(self):
        self.name = "Data Export Methods"
        
    def execute(self, data, export_format='json'):
        """ডাটা এক্সপোর্ট"""
        results = {
            'method': self.name,
            'success': False,
            'data': {},
            'errors': []
        }
        
        try:
            exports = {}
            
            if 'json' in export_format.lower():
                exports['json'] = self.export_json(data)
            
            if 'csv' in export_format.lower():
                exports['csv'] = self.export_csv(data)
            
            if 'excel' in export_format.lower():
                exports['excel'] = self.export_excel(data)
            
            if 'zip' in export_format.lower():
                exports['zip'] = self.export_zip(data)
            
            results['data'] = exports
            results['success'] = True
            
        except Exception as e:
            results['errors'].append(str(e))
        
        return results
    
    def export_json(self, data):
        """JSON এক্সপোর্ট"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            'filename': filename,
            'size': os.path.getsize(filename),
            'format': 'JSON'
        }
    
    def export_csv(self, data):
        """CSV এক্সপোর্ট"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.csv"
        
        # Flatten data for CSV
        flat_data = self.flatten_data(data)
        
        if flat_data:
            df = pd.DataFrame(flat_data)
            df.to_csv(filename, index=False, encoding='utf-8')
        
        return {
            'filename': filename,
            'size': os.path.getsize(filename) if os.path.exists(filename) else 0,
            'format': 'CSV',
            'rows': len(flat_data) if flat_data else 0
        }
    
    def flatten_data(self, data, parent_key='', sep='_'):
        """ডাটা flatten করা"""
        items = []
        
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(self.flatten_data(v, new_key, sep))
                elif isinstance(v, list):
                    # প্রতিটি আইটেম আলাদা row
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            items.extend(self.flatten_data(item, f"{new_key}_{i}", sep))
                        else:
                            items.append({new_key: str(v)})
                    break
                else:
                    items.append({new_key: v})
        
        return items
    
    def export_excel(self, data):
        """Excel এক্সপোর্ট"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.xlsx"
        
        # Multiple sheets for different data types
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Contacts sheet
            if 'contacts' in str(data):
                contacts_df = self.extract_contacts_df(data)
                if not contacts_df.empty:
                    contacts_df.to_excel(writer, sheet_name='Contacts', index=False)
            
            # Social media sheet
            if 'social' in str(data):
                social_df = self.extract_social_df(data)
                if not social_df.empty:
                    social_df.to_excel(writer, sheet_name='Social Media', index=False)
            
            # Raw data sheet
            raw_df = pd.DataFrame([data])
            raw_df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        return {
            'filename': filename,
            'size': os.path.getsize(filename),
            'format': 'Excel',
            'sheets': len(writer.sheets) if 'writer' in locals() else 0
        }
    
    def extract_contacts_df(self, data):
        """কন্টাক্টস DataFrame তৈরি"""
        contacts = []
        
        # Recursively find contact data
        if isinstance(data, dict):
            if 'email' in data or 'phone' in data:
                contacts.append({
                    'email': data.get('email', ''),
                    'phone': data.get('phone', ''),
                    'source': data.get('source', '')
                })
            
            for value in data.values():
                if isinstance(value, (dict, list)):
                    contacts.extend(self.extract_contacts_df(value))
        
        return pd.DataFrame(contacts)
    
    def extract_social_df(self, data):
        """সোশ্যাল মিডিয়া DataFrame তৈরি"""
        social_data = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if 'social' in key.lower() or 'facebook' in key.lower() or 'twitter' in key.lower():
                    if isinstance(value, dict):
                        for platform, links in value.items():
                            if isinstance(links, list):
                                for link in links:
                                    social_data.append({
                                        'platform': platform,
                                        'url': link
                                    })
        
        return pd.DataFrame(social_data)
    
    def export_zip(self, data):
        """ZIP আর্কাইভ এক্সপোর্ট"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"export_{timestamp}.zip"
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add JSON export
            json_file = self.export_json(data)['filename']
            zipf.write(json_file, os.path.basename(json_file))
            
            # Add CSV export
            csv_file = self.export_csv(data)['filename']
            zipf.write(csv_file, os.path.basename(csv_file))
            
            # Add readme
            readme_content = f"""
MAR-PD Export Archive
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Contains: JSON and CSV exports of scan data
Ethical Use Only!
"""
            zipf.writestr('README.txt', readme_content)
        
        # Clean up individual files
        if os.path.exists(json_file):
            os.remove(json_file)
        if os.path.exists(csv_file):
            os.remove(csv_file)
        
        return {
            'filename': zip_filename,
            'size': os.path.getsize(zip_filename),
            'format': 'ZIP',
            'contains': ['JSON', 'CSV', 'README']
        }