#!/usr/bin/env python3
# utils/file_organizer.py

import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

class FileOrganizer:
    """Professional file organization and management"""
    
    def __init__(self, base_dir="payloads"):
        self.base_dir = Path(base_dir)
        self.current_session = None
        self.setup_directories()
    
    def setup_directories(self):
        """Create base directory structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session = f"session_{timestamp}"
        
        # Create session directory
        session_dir = self.base_dir / self.current_session
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Create category subdirectories
        categories = ['windows', 'linux', 'android', 'macos', 'web', 'listeners']
        for cat in categories:
            (session_dir / cat).mkdir(exist_ok=True)
        
        return session_dir
    
    def save_payload(self, payload_data, platform, filename):
        """Save payload file with proper organization"""
        session_dir = self.base_dir / self.current_session
        platform_dir = session_dir / platform
        
        # Ensure filename has proper extension
        filepath = platform_dir / filename
        
        # If payload_data is bytes, write binary; if string, write text
        if isinstance(payload_data, bytes):
            with open(filepath, 'wb') as f:
                f.write(payload_data)
        else:
            with open(filepath, 'w') as f:
                f.write(payload_data)
        
        return filepath
    
    def save_listener(self, listener_content, platform, port):
        """Save listener RC file"""
        session_dir = self.base_dir / self.current_session
        listener_dir = session_dir / 'listeners'
        
        filename = f"{platform}_tcp_{port}.rc"
        filepath = listener_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(listener_content)
        
        return filepath
    
    def get_file_info(self, filepath):
        """Get file information (size, hashes)"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            return None
        
        # File size
        size = filepath.stat().st_size
        
        # Calculate hashes
        with open(filepath, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            sha1 = hashlib.sha1(data).hexdigest()
        
        return {
            'size': size,
            'md5': md5,
            'sha1': sha1,
            'path': str(filepath)
        }
    
    def get_session_path(self):
        """Get current session path"""
        return self.base_dir / self.current_session
