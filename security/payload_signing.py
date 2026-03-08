# security/payload_signing.py
import hashlib
import hmac
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

class PayloadSigning:
    """Cryptographic signing of payloads"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
    
    def sign_payload(self, payload_data):
        """Sign payload with private key"""
        signature = self.private_key.sign(
            payload_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            'payload': payload_data.hex(),
            'signature': signature.hex(),
            'algorithm': 'RSA-PSS-SHA256'
        }
    
    def verify_payload(self, signed_payload):
        """Verify payload signature"""
        try:
            payload = bytes.fromhex(signed_payload['payload'])
            signature = bytes.fromhex(signed_payload['signature'])
            
            self.public_key.verify(
                signature,
                payload,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
