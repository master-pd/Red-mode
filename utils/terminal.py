# file: utils/terminal.py
import sys
import time
from datetime import datetime

class TerminalUI:
    """কালারফুল টার্মিনাল UI"""
    
    # কালার কোড
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m'
    }
    
    # Background colors
    BG_COLORS = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'cyan': '\033[46m',
        'white': '\033[47m'
    }
    
    # Styles
    STYLES = {
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reverse': '\033[7m',
        'hidden': '\033[8m'
    }
    
    def __init__(self):
        self.start_time = time.time()
        
    def print_color(self, text, color='white', style='', bg_color=None, end='\n'):
        """কালার সহ প্রিন্ট"""
        color_code = self.COLORS.get(color, self.COLORS['white'])
        style_code = self.STYLES.get(style, '')
        bg_code = self.BG_COLORS.get(bg_color, '')
        
        formatted = f"{style_code}{bg_code}{color_code}{text}{self.COLORS['reset']}"
        print(formatted, end=end)
        
    def print_success(self, text):
        """সাকসেস মেসেজ"""
        self.print_color(f"[✓] {text}", 'bright_green')
        
    def print_error(self, text):
        """এরর মেসেজ"""
        self.print_color(f"[✗] {text}", 'bright_red')
        
    def print_warning(self, text):
        """ওয়ার্নিং মেসেজ"""
        self.print_color(f"[!] {text}", 'bright_yellow')
        
    def print_info(self, text):
        """ইনফো মেসেজ"""
        self.print_color(f"[i] {text}", 'bright_cyan')
        
    def print_progress(self, current, total, prefix="", suffix="", length=50):
        """প্রোগ্রেস বার"""
        percent = current / total
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)
        
        sys.stdout.write(f"\r{prefix} |{bar}| {current}/{total} {suffix}")
        sys.stdout.flush()
        
        if current == total:
            print()
            
    def print_header(self, text):
        """হেডার প্রিন্ট"""
        width = 60
        print("\n" + "=" * width)
        self.print_color(text.center(width), 'bright_magenta', 'bold')
        print("=" * width)
        
    def print_menu(self, title, options):
        """মেনু প্রিন্ট"""
        self.print_header(title)
        
        for i, option in enumerate(options, 1):
            self.print_color(f"{i:2}. {option}", 'bright_cyan')
            
        print("-" * 60)
        
    def get_input(self, prompt, color='bright_yellow'):
        """কালারফুল ইনপুট"""
        self.print_color(prompt, color, end=' ')
        return input()
        
    def show_banner(self):
        """ব্যানার দেখান"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║         ███╗   ███╗ █████╗ ██████╗ ██████╗ ██████╗       ║
║         ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔══██╗      ║
║         ██╔████╔██║███████║██████╔╝██║  ██║██║  ██║      ║
║         ██║╚██╔╝██║██╔══██║██╔═══╝ ██║  ██║██║  ██║      ║
║         ██║ ╚═╝ ██║██║  ██║██║     ██████╔╝██████╔╝      ║
║         ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═════╝ ╚═════╝       ║
║                                                          ║
║               Multi-Algorithmic Reconnaissance           ║
║                   Profile Decoder v3.0                   ║
║                    [For Educational Use]                 ║
╚══════════════════════════════════════════════════════════╝
"""
        self.print_color(banner, 'bright_cyan')
        
    def show_stats(self):
        """স্ট্যাটস দেখান"""
        elapsed = time.time() - self.start_time
        current_time = datetime.now().strftime("%H:%M:%S")
        
        stats = f"""
╔══════════════════════════════════════════════════════════╗
║                       Statistics                         ║
╠══════════════════════════════════════════════════════════╣
║  Start Time:   {datetime.now().strftime("%Y-%m-%d %H:%M:%S"):<40} ║
║  Elapsed Time: {self.format_time(elapsed):<40}           ║
║  Current Time: {current_time:<40}                        ║
╚══════════════════════════════════════════════════════════╝
"""
        self.print_color(stats, 'bright_green')
        
    def format_time(self, seconds):
        """টাইম ফরম্যাট"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"