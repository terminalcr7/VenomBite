# tests/test_advanced_features.py
import unittest
import tempfile
import os

class TestAdvancedFeatures(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.generator = PayloadGenerator()
    
    def test_parallel_generation(self):
        """Test generating multiple payloads simultaneously"""
        configs = [
            {'platform': 'windows', 'lhost': '192.168.1.100', 'lport': 4444},
            {'platform': 'linux', 'lhost': '192.168.1.100', 'lport': 4445},
            {'platform': 'android', 'lhost': '192.168.1.100', 'lport': 4446}
        ]
        
        parallel_gen = ParallelGenerator(max_workers=3)
        results = parallel_gen.batch_generate(configs)
        
        self.assertEqual(len(results), 3)
    
    def test_template_injection(self):
        """Test template engine"""
        engine = TemplateEngine()
        payload = "test_payload"
        
        result = engine.inject_payload('default', payload)
        self.assertIn(payload, result)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
