# file: utils/progress.py
import sys
import time
from datetime import datetime, timedelta

class ProgressBar:
    """প্রোগ্রেস বার সিস্টেম"""
    
    def __init__(self, total=100, prefix='Progress:', suffix='Complete', length=50, fill='█'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.start_time = time.time()
        self.current = 0
        self.eta = 'Calculating...'
        
    def update(self, iteration, **kwargs):
        """প্রোগ্রেস আপডেট"""
        self.current = iteration
        
        # Calculate percentage
        percent = ("{0:.1f}").format(100 * (iteration / float(self.total)))
        
        # Calculate filled length
        filled_length = int(self.length * iteration // self.total)
        
        # Create bar
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        
        # Calculate ETA
        elapsed_time = time.time() - self.start_time
        if iteration > 0:
            time_per_item = elapsed_time / iteration
            remaining_items = self.total - iteration
            eta_seconds = remaining_items * time_per_item
            self.eta = self.format_time(eta_seconds)
        else:
            self.eta = 'Calculating...'
        
        # Update suffix with additional info
        extra_suffix = ''
        if kwargs:
            extra_info = []
            for key, value in kwargs.items():
                if isinstance(value, (int, float)):
                    extra_info.append(f'{key}: {value}')
                else:
                    extra_info.append(f'{key}: {str(value)[:20]}')
            extra_suffix = ' | ' + ' | '.join(extra_info)
        
        # Print progress bar
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent}% {self.suffix} | ETA: {self.eta}{extra_suffix}')
        sys.stdout.flush()
        
        # Print new line on completion
        if iteration == self.total:
            print()
    
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def increment(self, step=1, **kwargs):
        """ইনক্রিমেন্ট"""
        self.current += step
        self.update(self.current, **kwargs)
    
    def finish(self):
        """ফিনিশ"""
        self.update(self.total)
        elapsed = time.time() - self.start_time
        print(f" Completed in {self.format_time(elapsed)}")

class MultiProgress:
    """মাল্টি প্রোগ্রেস ট্র্যাকার"""
    
    def __init__(self):
        self.trackers = {}
        self.start_time = time.time()
        
    def create_tracker(self, name, total, prefix=None, length=30):
        """ট্র্যাকার তৈরি"""
        if prefix is None:
            prefix = f"{name}:"
        
        tracker = {
            'progress': ProgressBar(total=total, prefix=prefix, length=length),
            'total': total,
            'current': 0,
            'status': 'running'
        }
        
        self.trackers[name] = tracker
        return tracker['progress']
    
    def update_tracker(self, name, iteration, **kwargs):
        """ট্র্যাকার আপডেট"""
        if name in self.trackers:
            self.trackers[name]['current'] = iteration
            self.trackers[name]['progress'].update(iteration, **kwargs)
            
            # Check if completed
            if iteration >= self.trackers[name]['total']:
                self.trackers[name]['status'] = 'completed'
    
    def increment_tracker(self, name, step=1, **kwargs):
        """ট্র্যাকার ইনক্রিমেন্ট"""
        if name in self.trackers:
            current = self.trackers[name]['current'] + step
            self.update_tracker(name, current, **kwargs)
    
    def get_overall_progress(self):
        """ওভারঅল প্রোগ্রেস পান"""
        if not self.trackers:
            return 0
        
        total_items = 0
        completed_items = 0
        
        for tracker in self.trackers.values():
            total_items += tracker['total']
            completed_items += tracker['current']
        
        if total_items == 0:
            return 0
        
        return (completed_items / total_items) * 100
    
    def show_summary(self):
        """সামারি দেখান"""
        print("\n" + "="*60)
        print(" Progress Summary")
        print("="*60)
        
        elapsed = time.time() - self.start_time
        
        for name, tracker in self.trackers.items():
            status_icon = "✓" if tracker['status'] == 'completed' else "?"
            percent = (tracker['current'] / tracker['total']) * 100
            print(f"{status_icon} {name}: {tracker['current']}/{tracker['total']} ({percent:.1f}%)")
        
        overall = self.get_overall_progress()
        print(f"\n Overall Progress: {overall:.1f}%")
        print(f"⏱️  Elapsed Time: {self.format_time(elapsed)}")
        print("="*60)
    
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        return str(timedelta(seconds=int(seconds)))

class Spinner:
    """স্পিনার (লোডিং ইন্ডিকেটর)"""
    
    def __init__(self, message="Processing", delay=0.1):
        self.message = message
        self.delay = delay
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.running = False
        self.spinner_thread = None
        
    def start(self):
        """স্পিনার শুরু"""
        self.running = True
        sys.stdout.write(f"\r{self.message} ")
        sys.stdout.flush()
        
        import threading
        self.spinner_thread = threading.Thread(target=self._spin)
        self.spinner_thread.start()
    
    def _spin(self):
        """স্পিন থ্রেড"""
        i = 0
        while self.running:
            sys.stdout.write(f"\r{self.message} {self.spinner_chars[i % len(self.spinner_chars)]}")
            sys.stdout.flush()
            time.sleep(self.delay)
            i += 1
    
    def stop(self, success=True, message=None):
        """স্পিনার বন্ধ"""
        self.running = False
        if self.spinner_thread:
            self.spinner_thread.join()
        
        if message is None:
            message = "Completed" if success else "Failed"
        
        icon = "✓" if success else "×"
        sys.stdout.write(f"\r{self.message} {icon} {message}\n")
        sys.stdout.flush()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        self.stop(success)

class TimedTask:
    """টাইমড টাস্ক ট্র্যাকার"""
    
    def __init__(self, task_name):
        self.task_name = task_name
        self.start_time = None
        self.end_time = None
        
    def start(self):
        """টাস্ক শুরু"""
        self.start_time = time.time()
        print(f"⏱️  Starting: {self.task_name}")
        return self
    
    def stop(self):
        """টাস্ক বন্ধ"""
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f" Completed: {self.task_name} in {self.format_time(elapsed)}")
        return elapsed
    
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{minutes}m {seconds:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

class DownloadProgress:
    """ডাউনলোড প্রোগ্রেস ট্র্যাকার"""
    
    def __init__(self, total_size, description="Downloading"):
        self.total_size = total_size
        self.description = description
        self.downloaded = 0
        self.start_time = time.time()
        self.last_update = 0
        
    def update(self, chunk_size):
        """আপডেট"""
        self.downloaded += chunk_size
        current_time = time.time()
        
        # Update every 0.5 seconds
        if current_time - self.last_update > 0.5:
            self._display()
            self.last_update = current_time
    
    def _display(self):
        """ডিসপ্লে"""
        percent = (self.downloaded / self.total_size) * 100
        
        # Calculate speed
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            speed = self.downloaded / elapsed
            speed_str = self.format_size(speed) + "/s"
        else:
            speed_str = "Calculating..."
        
        # Calculate ETA
        if self.downloaded > 0:
            remaining = self.total_size - self.downloaded
            if speed > 0:
                eta = remaining / speed
                eta_str = self.format_time(eta)
            else:
                eta_str = "Unknown"
        else:
            eta_str = "Calculating..."
        
        # Create progress bar
        bar_length = 40
        filled = int(bar_length * self.downloaded // self.total_size)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Format sizes
        downloaded_str = self.format_size(self.downloaded)
        total_str = self.format_size(self.total_size)
        
        sys.stdout.write(
            f"\r{self.description}: [{bar}] {percent:.1f}% | "
            f"{downloaded_str}/{total_str} | {speed_str} | ETA: {eta_str}"
        )
        sys.stdout.flush()
    
    def finish(self):
        """ফিনিশ"""
        self.downloaded = self.total_size
        self._display()
        print()  # New line
        
        elapsed = time.time() - self.start_time
        avg_speed = self.total_size / elapsed
        print(f" Download completed in {self.format_time(elapsed)} "
              f"({self.format_size(avg_speed)}/s average)")
    
    def format_size(self, size_bytes):
        """সাইজ ফরম্যাট"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"
    
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes}m {seconds}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"

class ProgressManager:
    """প্রোগ্রেস ম্যানেজার"""
    
    def __init__(self):
        self.tasks = {}
        self.active_tasks = {}
        
    def start_task(self, task_id, total_steps, description):
        """টাস্ক শুরু"""
        progress = ProgressBar(total=total_steps, prefix=description, length=40)
        self.tasks[task_id] = {
            'progress': progress,
            'total': total_steps,
            'current': 0,
            'description': description,
            'start_time': time.time(),
            'status': 'running'
        }
        self.active_tasks[task_id] = self.tasks[task_id]
        return progress
    
    def update_task(self, task_id, current_step, **kwargs):
        """টাস্ক আপডেট"""
        if task_id in self.tasks:
            self.tasks[task_id]['current'] = current_step
            self.tasks[task_id]['progress'].update(current_step, **kwargs)
            
            if current_step >= self.tasks[task_id]['total']:
                self.complete_task(task_id)
    
    def complete_task(self, task_id):
        """টাস্ক কমপ্লিট"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task['status'] = 'completed'
            task['end_time'] = time.time()
            task['elapsed'] = task['end_time'] - task['start_time']
            
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            
            task['progress'].finish()
    
    def fail_task(self, task_id, error_message):
        """টাস্ক ফেইল"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task['status'] = 'failed'
            task['error'] = error_message
            task['end_time'] = time.time()
            
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            
            print(f"\n {task['description']} failed: {error_message}")
    
    def get_status_report(self):
        """স্ট্যাটাস রিপোর্ট পান"""
        report = {
            'total_tasks': len(self.tasks),
            'completed_tasks': len([t for t in self.tasks.values() if t['status'] == 'completed']),
            'failed_tasks': len([t for t in self.tasks.values() if t['status'] == 'failed']),
            'running_tasks': len(self.active_tasks),
            'tasks': []
        }
        
        for task_id, task in self.tasks.items():
            task_info = {
                'id': task_id,
                'description': task['description'],
                'status': task['status'],
                'progress': f"{task['current']}/{task['total']}",
                'percentage': (task['current'] / task['total']) * 100 if task['total'] > 0 else 0
            }
            
            if 'elapsed' in task:
                task_info['elapsed_time'] = task['elapsed']
            
            if 'error' in task:
                task_info['error'] = task['error']
            
            report['tasks'].append(task_info)
        
        return report
    
    def show_dashboard(self):
        """ড্যাশবোর্ড দেখান"""
        report = self.get_status_report()
        
        print("\n" + "="*70)
        print(" Progress Dashboard")
        print("="*70)
        
        # Summary
        print(f"\n Summary:")
        print(f"   Total Tasks: {report['total_tasks']}")
        print(f"    Completed: {report['completed_tasks']}")
        print(f"    Running: {report['running_tasks']}")
        print(f"    Failed: {report['failed_tasks']}")
        
        # Running tasks
        if report['running_tasks'] > 0:
            print(f"\n Running Tasks:")
            for task in report['tasks']:
                if task['status'] == 'running':
                    bar_length = 20
                    filled = int(bar_length * task['percentage'] / 100)
                    bar = '█' * filled + '░' * (bar_length - filled)
                    print(f"   {task['description']}: [{bar}] {task['percentage']:.1f}%")
        
        # Recent completions
        completed_tasks = [t for t in report['tasks'] if t['status'] == 'completed'][-5:]  # Last 5
        if completed_tasks:
            print(f"\n Recently Completed:")
            for task in completed_tasks:
                time_str = self.format_time(task.get('elapsed_time', 0))
                print(f"   {task['description']} ({time_str})")
        
        print("="*70)
    
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{minutes}m {seconds:.0f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"