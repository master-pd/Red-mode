# file: utils/logger.py
import logging
import sys
import os
import json
from datetime import datetime
from pathlib import Path

class AdvancedLogger:
    """অ্যাডভান্সড লগার সিস্টেম"""
    
    def __init__(self, log_dir="logs", app_name="MAR-PD"):
        self.app_name = app_name
        self.log_dir = Path(log_dir)
        self.setup_logging()
        self.session_id = self.generate_session_id()
        
    def generate_session_id(self):
        """সেশন আইডি জেনারেট"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = os.urandom(4).hex()
        return f"{timestamp}_{random_suffix}"
    
    def setup_logging(self):
        """লগিং সিস্টেম সেটআপ"""
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"{self.app_name}_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(self.app_name)
        self.logger.info(f"Logger initialized. Session ID: {self.session_id}")
        
    def log(self, message, level='INFO', metadata=None):
        """লগ মেসেজ"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'level': level.upper(),
            'message': message,
            'metadata': metadata or {}
        }
        
        # Log to file
        levels = {
            'DEBUG': self.logger.debug,
            'INFO': self.logger.info,
            'WARNING': self.logger.warning,
            'ERROR': self.logger.error,
            'CRITICAL': self.logger.critical
        }
        
        log_func = levels.get(level.upper(), self.logger.info)
        
        # Format message with metadata
        if metadata:
            formatted_message = f"{message} | Metadata: {json.dumps(metadata)}"
        else:
            formatted_message = message
        
        log_func(formatted_message)
        
        # Also save to structured log file
        self.save_structured_log(log_data)
        
        return log_data
    
    def save_structured_log(self, log_data):
        """স্ট্রাকচার্ড লগ সেভ"""
        structured_log_dir = self.log_dir / "structured"
        structured_log_dir.mkdir(parents=True, exist_ok=True)
        
        date_str = datetime.now().strftime("%Y%m%d")
        structured_log_file = structured_log_dir / f"structured_{date_str}.jsonl"
        
        try:
            with open(structured_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error saving structured log: {e}")
    
    def log_method_start(self, method_name, parameters=None):
        """মেথড স্টার্ট লগ"""
        return self.log(
            f"Method started: {method_name}",
            'INFO',
            {
                'method': method_name,
                'action': 'start',
                'parameters': parameters or {},
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def log_method_end(self, method_name, success=True, results=None, execution_time=None):
        """মেথড এন্ড লগ"""
        status = "SUCCESS" if success else "FAILED"
        
        metadata = {
            'method': method_name,
            'action': 'end',
            'status': status,
            'results_summary': self.summarize_results(results) if results else None,
            'execution_time': execution_time
        }
        
        return self.log(
            f"Method completed: {method_name} - Status: {status}",
            'INFO' if success else 'ERROR',
            metadata
        )
    
    def summarize_results(self, results, max_items=5):
        """রেজাল্টস সামারাইজ"""
        if isinstance(results, dict):
            summary = {}
            for key, value in results.items():
                if isinstance(value, (list, dict)):
                    summary[key] = f"{type(value).__name__} with {len(value) if hasattr(value, '__len__') else '?'} items"
                else:
                    summary[key] = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            return summary
        elif isinstance(results, list):
            return f"List with {len(results)} items"
        else:
            return str(results)[:200] + "..." if len(str(results)) > 200 else str(results)
    
    def log_error(self, method_name, error, context=None):
        """এরর লগ"""
        error_data = {
            'method': method_name,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {},
            'traceback': self.get_traceback()
        }
        
        return self.log(
            f"Error in {method_name}: {str(error)}",
            'ERROR',
            error_data
        )
    
    def get_traceback(self):
        """ট্রেসব্যাক পান"""
        import traceback
        return traceback.format_exc()
    
    def log_security_event(self, event_type, details):
        """সিকিউরিটি ইভেন্ট লগ"""
        security_log_dir = self.log_dir / "security"
        security_log_dir.mkdir(parents=True, exist_ok=True)
        
        event_data = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'event_type': event_type,
            'details': details,
            'ip_address': self.get_ip_address(),
            'user_agent': self.get_user_agent()
        }
        
        # Save to security log file
        security_log_file = security_log_dir / f"security_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(security_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event_data, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error saving security log: {e}")
        
        # Also log normally
        return self.log(
            f"Security event: {event_type}",
            'WARNING',
            event_data
        )
    
    def get_ip_address(self):
        """আইপি অ্যাড্রেস পান"""
        try:
            import socket
            return socket.gethostbyname(socket.gethostname())
        except:
            return "unknown"
    
    def get_user_agent(self):
        """ইউজার এজেন্ট পান"""
        return "MAR-PD-Logger/1.0"
    
    def log_data_export(self, export_type, data_size, destination):
        """ডাটা এক্সপোর্ট লগ"""
        return self.log(
            f"Data exported: {export_type}",
            'INFO',
            {
                'export_type': export_type,
                'data_size': data_size,
                'destination': destination,
                'action': 'data_export'
            }
        )
    
    def log_scan_result(self, target, method, findings_count):
        """স্ক্যান রেজাল্ট লগ"""
        return self.log(
            f"Scan completed: {target}",
            'INFO',
            {
                'target': target,
                'method': method,
                'findings_count': findings_count,
                'action': 'scan_complete'
            }
        )
    
    def get_log_statistics(self, date=None):
        """লগ স্ট্যাটিসটিক্স পান"""
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        log_file = self.log_dir / f"{self.app_name}_{date}.log"
        
        if not log_file.exists():
            return {'error': 'Log file not found'}
        
        stats = {
            'date': date,
            'total_lines': 0,
            'level_counts': {
                'DEBUG': 0,
                'INFO': 0,
                'WARNING': 0,
                'ERROR': 0,
                'CRITICAL': 0
            },
            'methods_logged': {},
            'error_count': 0
        }
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    stats['total_lines'] += 1
                    
                    # Count by level
                    for level in stats['level_counts'].keys():
                        if f" - {level} - " in line:
                            stats['level_counts'][level] += 1
                    
                    # Count errors
                    if 'ERROR' in line or 'CRITICAL' in line:
                        stats['error_count'] += 1
                    
                    # Count method logs
                    if 'Method started:' in line:
                        method_name = line.split('Method started: ')[1].split(' |')[0]
                        stats['methods_logged'][method_name] = stats['methods_logged'].get(method_name, 0) + 1
            
            return {'success': True, 'statistics': stats}
            
        except Exception as e:
            return {'error': str(e)}
    
    def cleanup_old_logs(self, days_to_keep=30):
        """পুরানো লগস ক্লিনআপ"""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        deleted_files = []
        deleted_size = 0
        
        try:
            for log_file in self.log_dir.rglob("*.log"):
                if log_file.is_file():
                    file_age = os.path.getmtime(log_file)
                    
                    if file_age < cutoff_date:
                        try:
                            file_size = log_file.stat().st_size
                            log_file.unlink()
                            deleted_files.append(str(log_file))
                            deleted_size += file_size
                        except Exception as e:
                            self.log(f"Error deleting log file {log_file}: {e}", 'ERROR')
            
            # Also clean structured logs
            structured_dir = self.log_dir / "structured"
            if structured_dir.exists():
                for jsonl_file in structured_dir.glob("*.jsonl"):
                    if jsonl_file.is_file():
                        file_age = os.path.getmtime(jsonl_file)
                        
                        if file_age < cutoff_date:
                            try:
                                file_size = jsonl_file.stat().st_size
                                jsonl_file.unlink()
                                deleted_files.append(str(jsonl_file))
                                deleted_size += file_size
                            except Exception as e:
                                self.log(f"Error deleting structured log {jsonl_file}: {e}", 'ERROR')
            
            self.log(
                f"Cleaned up {len(deleted_files)} old log files",
                'INFO',
                {
                    'action': 'log_cleanup',
                    'deleted_files': len(deleted_files),
                    'deleted_size': deleted_size,
                    'days_kept': days_to_keep
                }
            )
            
            return {
                'success': True,
                'deleted_files': len(deleted_files),
                'deleted_size': deleted_size,
                'files': deleted_files[:10]  # First 10 files
            }
            
        except Exception as e:
            self.log(f"Log cleanup error: {e}", 'ERROR')
            return {'success': False, 'error': str(e)}
    
    def export_logs(self, export_format='json', date_range=None):
        """লগস এক্সপোর্ট"""
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'logs': []
        }
        
        # Determine files to export
        if date_range:
            start_date, end_date = date_range
            log_files = []
            current_date = start_date
            
            while current_date <= end_date:
                date_str = current_date.strftime("%Y%m%d")
                log_file = self.log_dir / f"{self.app_name}_{date_str}.log"
                if log_file.exists():
                    log_files.append(log_file)
                current_date += timedelta(days=1)
        else:
            # Export today's logs
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = self.log_dir / f"{self.app_name}_{date_str}.log"
            log_files = [log_file] if log_file.exists() else []
        
        # Read and parse logs
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        # Parse log line
                        log_entry = self.parse_log_line(line)
                        if log_entry:
                            export_data['logs'].append(log_entry)
            except Exception as e:
                self.log(f"Error reading log file {log_file}: {e}", 'ERROR')
        
        # Export based on format
        export_dir = self.log_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == 'json':
            export_file = export_dir / f"logs_export_{timestamp}.json"
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        elif export_format == 'csv':
            export_file = export_dir / f"logs_export_{timestamp}.csv"
            self.export_logs_to_csv(export_data, export_file)
        
        else:
            export_file = export_dir / f"logs_export_{timestamp}.txt"
            with open(export_file, 'w', encoding='utf-8') as f:
                for log in export_data['logs']:
                    f.write(f"{log.get('timestamp')} - {log.get('level')} - {log.get('message')}\n")
        
        self.log(f"Logs exported to {export_file}", 'INFO')
        return {
            'success': True,
            'export_file': str(export_file),
            'log_count': len(export_data['logs']),
            'date_range': date_range
        }
    
    def parse_log_line(self, line):
        """লগ লাইন পার্স"""
        try:
            # Example: 2024-01-15 10:30:00 - MAR-PD - INFO - Message
            parts = line.strip().split(' - ', 3)
            if len(parts) == 4:
                timestamp_str, logger_name, level, message = parts
                
                # Parse metadata if present
                metadata = {}
                if ' | Metadata: ' in message:
                    message_part, metadata_part = message.split(' | Metadata: ', 1)
                    try:
                        metadata = json.loads(metadata_part)
                    except:
                        metadata = {'raw_metadata': metadata_part}
                    message = message_part
                
                return {
                    'timestamp': timestamp_str,
                    'logger': logger_name,
                    'level': level,
                    'message': message,
                    'metadata': metadata
                }
        except Exception as e:
            return None
        return None
    
    def export_logs_to_csv(self, log_data, filepath):
        """লগস CSV তে এক্সপোর্ট"""
        try:
            import csv
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['timestamp', 'level', 'message', 'method', 'action', 'status'])
                
                # Write data
                for log in log_data.get('logs', []):
                    metadata = log.get('metadata', {})
                    writer.writerow([
                        log.get('timestamp', ''),
                        log.get('level', ''),
                        log.get('message', '')[:200],  # Truncate long messages
                        metadata.get('method', ''),
                        metadata.get('action', ''),
                        metadata.get('status', '')
                    ])
                    
        except ImportError:
            # Fallback without CSV module
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("timestamp,level,message,method,action,status\n")
                for log in log_data.get('logs', []):
                    metadata = log.get('metadata', {})
                    f.write(f"{log.get('timestamp', '')},{log.get('level', '')},\"{log.get('message', '')[:200]}\",{metadata.get('method', '')},{metadata.get('action', '')},{metadata.get('status', '')}\n")