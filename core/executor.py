#!/usr/bin/env python3
# core/executor.py

import subprocess
import shlex
from utils.colors import Colors

class CommandExecutor:
    """Professional command execution with error handling"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def execute(self, command, shell=False):
        """
        Execute system command with proper error handling
        Returns: (success, stdout, stderr)
        """
        try:
            if self.verbose:
                print(Colors.info(f"Executing: {command}"))
            
            if shell:
                # Use shell for complex commands
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # Split command for direct execution
                args = shlex.split(command)
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                return True, stdout, stderr
            else:
                return False, stdout, stderr
                
        except FileNotFoundError:
            return False, "", f"Command not found: {command}"
        except PermissionError:
            return False, "", f"Permission denied: {command}"
        except Exception as e:
            return False, "", str(e)
    
    def check_msfvenom(self):
        """Check if msfvenom is available"""
        success, stdout, stderr = self.execute("which msfvenom")
        if not success:
            print(Colors.error("msfvenom not found! Please install Metasploit framework."))
            return False
        
        # Get version
        success, stdout, stderr = self.execute("msfvenom --version")
        if success:
            version = stdout.split('\n')[0] if stdout else "Unknown"
            print(Colors.success(f"Found msfvenom: {version}"))
        
        return True
