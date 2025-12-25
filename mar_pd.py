#!/usr/bin/env python3
"""
MAR-PD v3.0 - Multi-Algorithmic Reconnaissance Profile Decoder
Main Entry Point
"""

import os
import sys
import time
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.scanner import Scanner
from core.analyzer import Analyzer
from core.reporter import Reporter
from utils.terminal import TerminalUI
from utils.logger import Logger

class MARPD:
    """মার-পিডি মেইন ক্লাস"""
    
    def __init__(self):
        self.version = "3.0"
        self.author = "MAR-PD Development Team"
        self.terminal = TerminalUI()
        self.logger = Logger()
        self.scanner = Scanner()
        self.analyzer = Analyzer()
        self.reporter = Reporter()
        
    def show_banner(self):
        """ব্যানার দেখান"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║            MAR-PD v3.0 - Profile Decoder                 ║
║            Multi-Algorithmic Reconnaissance              ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        self.terminal.print_color(banner, "cyan")
        
    def check_ethical_agreement(self):
        """নৈতিক চুক্তি চেক"""
        agreement_file = "ethical_agreement.txt"
        
        if not os.path.exists(agreement_file):
            self.terminal.print_error("নৈতিক চুক্তি ফাইল পাওয়া যায়নি!")
            return False
            
        with open(agreement_file, 'r', encoding='utf-8') as f:
            agreement = f.read()
            
        self.terminal.print_color(agreement, "yellow")
        self.terminal.print_warning("\n⚠️ you follow the rules tos ? (yes/ no): ")
        
        response = input().strip().lower()
        if response not in ['yes', 'y', 'no', 'n']:
            self.terminal.print_error("voilence tos to exit please!")
            return False
            
        return True
        
    def run(self, target=None):
        """মেইন রান মেথড"""
        try:
            # শো ব্যানার
            self.show_banner()
            
            # নৈতিক চুক্তি চেক
            if not self.check_ethical_agreement():
                return
                
            self.logger.log("MAR-PD started", "INFO")
            
            # টার্গেট ইনপুট
            if not target:
                self.terminal.print_info("🎯 Target input :")
                self.terminal.print_info("   (Facebook ID, URL, Username, Email / Phone)")
                target = input("   ➜ ").strip()
                
            if not target:
                self.terminal.print_error("Target required !")
                return
                