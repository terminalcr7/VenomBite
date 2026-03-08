# templates/template_engine.py
import os
import random
import string
from pathlib import Path

class TemplateEngine:
    """Generate payloads from custom templates"""
    
    def __init__(self, template_dir="templates"):
        self.template_dir = Path(template_dir)
        self.templates = self.load_templates()
    
    def load_templates(self):
        """Load available templates"""
        templates = {}
        for template_file in self.template_dir.glob("*.template"):
            with open(template_file, 'r') as f:
                templates[template_file.stem] = f.read()
        return templates
    
    def inject_payload(self, template_name, payload, options=None):
        """Inject payload into template"""
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")
        
        template = self.templates[template_name]
        
        # Replace placeholders
        template = template.replace('{{PAYLOAD}}', payload)
        template = template.replace('{{RANDOM_STRING}}', self.generate_random_string())
        
        if options:
            for key, value in options.items():
                template = template.replace(f'{{{{{key}}}}}', str(value))
        
        return template
    
    def generate_random_string(self, length=10):
        """Generate random string for obfuscation"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
