# api/payload_api.py
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
import jwt
import datetime

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

class PayloadAPI:
    """REST API for remote payload generation"""
    
    def __init__(self, generator):
        self.generator = generator
        self.tokens = {}
    
    @app.route('/api/v1/generate', methods=['POST'])
    @auth.login_required
    def generate_payload(self):
        """Generate payload via API"""
        data = request.get_json()
        
        required_fields = ['platform', 'lhost', 'lport']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            result = self.generator.generate_payload(
                platform=data['platform'],
                lhost=data['lhost'],
                lport=data['lport'],
                payload_type=data.get('payload_type', 'reverse_tcp'),
                format_type=data.get('format', 'exe'),
                encoder=data.get('encoder'),
                iterations=data.get('iterations', 5)
            )
            
            return jsonify({
                'success': True,
                'payload_url': f"/download/{result['file_id']}",
                'file_info': result['file_info']
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def generate_token(self, username, expiry_hours=24):
        """Generate API token"""
        payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiry_hours)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
