#!/usr/bin/env python3
# utils/logger.py

import logging
import json
from datetime import datetime
from pathlib import Path

class PayloadLogger:
    """Professional logging system for payload generation"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file logging
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"payload_generator_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also print to console
            ]
        )
        
        self.logger = logging.getLogger('PayloadGenerator')
        
        # JSON log file for structured data
        self.json_log = self.log_dir / f"payloads_{timestamp}.json"
        self.payload_log = []
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def success(self, message):
        """Log success message"""
        self.logger.info(f"SUCCESS: {message}")
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def log_payload_generation(self, payload_data):
        """Log payload generation details to JSON"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'payload': payload_data
        }
        self.payload_log.append(entry)
        
        # Write to JSON file
        with open(self.json_log, 'w') as f:
            json.dump(self.payload_log, f, indent=2)
