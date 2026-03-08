# patterns/payload_factory.py
from abc import ABC, abstractmethod

class PayloadStrategy(ABC):
    """Strategy pattern for different payload generation approaches"""
    
    @abstractmethod
    def generate(self, context):
        pass

class StealthPayloadStrategy(PayloadStrategy):
    def generate(self, context):
        # Add evasion techniques
        context['encoder'] = 'x86/shikata_ga_nai'
        context['iterations'] = 10
        context['template'] = 'stealth_template.exe'
        return context

class QuickPayloadStrategy(PayloadStrategy):
    def generate(self, context):
        # Minimal options for speed
        return context

class PayloadFactory:
    """Factory pattern for creating different payload types"""
    
    @staticmethod
    def create_payload(platform, payload_type):
        if platform == 'windows':
            if 'meterpreter' in payload_type:
                return WindowsMeterpreterPayload()
            elif 'shell' in payload_type:
                return WindowsShellPayload()
        elif platform == 'linux':
            return LinuxPayload()
        # etc.
