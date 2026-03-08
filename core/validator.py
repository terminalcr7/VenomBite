#!/usr/bin/env python3
# core/validator.py

import os
import re
from utils.colors import Colors

class PayloadValidator:
    """Validate all user inputs before generation"""
    
    # Valid payload platforms
    PLATFORMS = {
        '1': {'name': 'Windows', 'formats': ['exe', 'dll', 'ps1', 'vba']},
        '2': {'name': 'Linux', 'formats': ['elf', 'py', 'c']},
        '3': {'name': 'Android', 'formats': ['apk']},
        '4': {'name': 'macOS', 'formats': ['macho', 'py', 'c']},
        '5': {'name': 'Web', 'formats': ['php', 'jsp', 'asp', 'war']}
    }
    
    # Valid payload types
    PAYLOAD_TYPES = {
        '1': 'reverse_tcp',
        '2': 'reverse_http',
        '3': 'reverse_https',
        '4': 'bind_tcp'
    }
    
    # Staged vs Stageless
    STAGE_OPTIONS = {
        '1': {'name': 'Staged', 'suffix': ''},
        '2': {'name': 'Stageless', 'suffix': '_reverse_tcp'}
    }
    
    @staticmethod
    def validate_platform(choice):
        """Validate platform selection"""
        if choice in PayloadValidator.PLATFORMS:
            return True, PayloadValidator.PLATFORMS[choice]
        return False, None
    
    @staticmethod
    def validate_payload_type(choice):
        """Validate payload type selection"""
        if choice in PayloadValidator.PAYLOAD_TYPES:
            return True, PayloadValidator.PAYLOAD_TYPES[choice]
        return False, None
    
    @staticmethod
    def validate_format(platform_key, format_choice):
        """Validate output format for specific platform"""
        if platform_key in PayloadValidator.PLATFORMS:
            valid_formats = PayloadValidator.PLATFORMS[platform_key]['formats']
            if format_choice in valid_formats:
                return True, format_choice
        return False, None
    
    @staticmethod
    def validate_ip(ip):
        """Validate IP address format"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(pattern, ip):
            parts = ip.split('.')
            for part in parts:
                if int(part) > 255:
                    return False
            return True
        return False
    
    @staticmethod
    def validate_port(port):
        """Validate port number"""
        try:
            port = int(port)
            return 1 <= port <= 65535
        except:
            return False
    
    @staticmethod
    def validate_output_filename(filename):
        """Validate output filename"""
        # Remove potentially dangerous characters
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
        if not filename:
            return False, None
        return True, filename
