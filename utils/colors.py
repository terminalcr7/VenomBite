#!/usr/bin/env python3
# utils/colors.py

from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform support
init(autoreset=True)

class Colors:
    """Professional color scheme for CLI output"""
    
    # Text colors
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Fore.RESET
    
    # Background colors
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_YELLOW = Back.YELLOW
    BG_BLUE = Back.BLUE
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE
    
    # Styles
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    NORMAL = Style.NORMAL
    
    # Professional status indicators
    SUCCESS = f"{GREEN}[✓]{RESET}"
    ERROR = f"{RED}[✗]{RESET}"
    WARNING = f"{YELLOW}[!]{RESET}"
    INFO = f"{BLUE}[*]{RESET}"
    PROMPT = f"{CYAN}[?]{RESET}"
    BANNER = f"{MAGENTA}{BRIGHT}"
    
    # NEW: Add HEADER attribute for section headers in main.py
    HEADER = f"{CYAN}{BRIGHT}"
    
    @staticmethod
    def banner(text):
        """Format banner text"""
        return f"{Colors.BANNER}{text}{Colors.RESET}"
    
    @staticmethod
    def section(text):
        """Format section headers"""
        return f"{Colors.CYAN}{Colors.BRIGHT}{text}{Colors.RESET}"
    
    @staticmethod
    def highlight(text):
        """Highlight important information"""
        return f"{Colors.YELLOW}{Colors.BRIGHT}{text}{Colors.RESET}"
    
    @staticmethod
    def success(text):
        """Success message"""
        return f"{Colors.SUCCESS} {text}"
    
    @staticmethod
    def error(text):
        """Error message"""
        return f"{Colors.ERROR} {text}"
    
    @staticmethod
    def warning(text):
        """Warning message"""
        return f"{Colors.WARNING} {text}"
    
    @staticmethod
    def info(text):
        """Info message"""
        return f"{Colors.INFO} {text}"
