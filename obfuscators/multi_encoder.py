# obfuscators/multi_encoder.py
import random

class MultiEncoder:
    """Apply multiple encoding layers for better evasion"""
    
    def __init__(self):
        self.encoders = [
            'x86/shikata_ga_nai',
            'x86/polymorphic',
            'x86/call4_dword_xor',
            'x86/countdown',
            'x86/fnstenv_mov',
            'x86/jmp_call_additive',
            'x86/alpha_mixed',
            'x86/alpha_upper',
            'x86/avoid_underscore_tolower',
            'x86/avoid_utf8_tolower'
        ]
    
    def generate_encoding_chain(self, min_encoders=2, max_encoders=5):
        """Generate random encoder chain"""
        num_encoders = random.randint(min_encoders, max_encoders)
        selected = random.sample(self.encoders, num_encoders)
        
        chain = []
        for encoder in selected:
            iterations = random.randint(1, 10)
            chain.append({
                'encoder': encoder,
                'iterations': iterations
            })
        
        return chain
    
    def build_msfvenom_command(self, base_cmd, encoder_chain):
        """Build command with encoder chain"""
        cmd = base_cmd
        for enc in encoder_chain:
            cmd += f" -e {enc['encoder']} -i {enc['iterations']}"
        return cmd
