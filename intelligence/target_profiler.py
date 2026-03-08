# intelligence/target_profiler.py
import subprocess
import re

class TargetProfiler:
    """Profile target system for optimal payload selection"""
    
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.os_info = None
        self.services = []
    
    def scan_target(self):
        """Perform lightweight scanning to identify target OS"""
        # Nmap OS detection
        try:
            result = subprocess.run(
                ['nmap', '-O', '--osscan-guess', self.target_ip],
                capture_output=True, text=True, timeout=300
            )
            self.parse_nmap_output(result.stdout)
        except:
            pass
        
        return self.os_info
    
    def parse_nmap_output(self, output):
        """Extract OS information from nmap output"""
        # Look for OS detection
        os_match = re.search(r'OS details: (.+)', output)
        if os_match:
            self.os_info = os_match.group(1)
        
        # Extract open ports
        port_matches = re.finditer(r'(\d+)/tcp\s+open\s+(\S+)', output)
        for match in port_matches:
            self.services.append({
                'port': match.group(1),
                'service': match.group(2)
            })
    
    def recommend_payloads(self):
        """Recommend payloads based on target profile"""
        recommendations = []
        
        if not self.os_info:
            return ['windows/meterpreter/reverse_tcp', 
                   'linux/x86/meterpreter/reverse_tcp']
        
        if 'Windows' in self.os_info:
            recommendations.extend([
                'windows/meterpreter/reverse_tcp',
                'windows/shell/reverse_tcp',
                'windows/meterpreter/reverse_http'
            ])
            
            # Check for specific Windows versions
            if '10' in self.os_info:
                recommendations.append('windows/x64/meterpreter/reverse_tcp')
        
        elif 'Linux' in self.os_info:
            recommendations.extend([
                'linux/x86/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp'
            ])
        
        return recommendations
