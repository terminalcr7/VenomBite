#!/usr/bin/env python3
# utils/ip_detector.py

import socket
import netifaces
import requests
import re
from .colors import Colors

class IPDetector:
    """Professional IP address detection and validation"""
    
    @staticmethod
    def get_local_ip(interface=None):
        """
        Get local IP address from interface or auto-detect
        Supports: eth0, wlan0, tun0, etc.
        """
        try:
            if interface:
                # Get IP from specific interface
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    return addrs[netifaces.AF_INET][0]['addr']
                else:
                    print(Colors.warning(f"No IPv4 address found on {interface}"))
                    return None
            else:
                # Auto-detect default interface
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
        except Exception as e:
            print(Colors.error(f"IP detection failed: {str(e)}"))
            return None
    
    @staticmethod
    def get_wan_ip():
        """Get public/WAN IP address"""
        try:
            # Try multiple services for redundancy
            services = [
                'https://api.ipify.org',
                'https://icanhazip.com',
                'https://ifconfig.me/ip'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        ip = response.text.strip()
                        if IPDetector.validate_ip(ip):
                            return ip
                except:
                    continue
            
            return None
        except Exception as e:
            print(Colors.error(f"WAN IP detection failed: {str(e)}"))
            return None
    
    @staticmethod
    def validate_ip(ip):
        """Validate IPv4 address format"""
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
    def get_interface_list():
        """Get list of available network interfaces"""
        try:
            interfaces = netifaces.interfaces()
            active_interfaces = []
            
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    ip = addrs[netifaces.AF_INET][0]['addr']
                    active_interfaces.append(f"{iface} ({ip})")
            
            return active_interfaces
        except:
            return []
