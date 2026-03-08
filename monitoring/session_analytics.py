# monitoring/session_analytics.py
import sqlite3
import json
from datetime import datetime, timedelta

class SessionAnalytics:
    """Track and analyze session data"""
    
    def __init__(self, db_path="sessions.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Create analytics tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                payload_type TEXT,
                target_ip TEXT,
                target_os TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                commands_run INTEGER,
                data_exfiltrated INTEGER
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                command TEXT,
                timestamp TIMESTAMP,
                output_size INTEGER
            )
        """)
    
    def log_session_start(self, session_id, payload_type, target_ip):
        """Log session start"""
        self.conn.execute("""
            INSERT INTO sessions (session_id, payload_type, target_ip, start_time)
            VALUES (?, ?, ?, ?)
        """, (session_id, payload_type, target_ip, datetime.now()))
        self.conn.commit()
    
    def log_command(self, session_id, command, output_size):
        """Log command execution"""
        self.conn.execute("""
            INSERT INTO commands (session_id, command, timestamp, output_size)
            VALUES (?, ?, ?, ?)
        """, (session_id, command, datetime.now(), output_size))
        self.conn.commit()
    
    def generate_report(self, days=7):
        """Generate analytics report"""
        cutoff = datetime.now() - timedelta(days=days)
        
        cursor = self.conn.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                AVG(commands_run) as avg_commands,
                SUM(data_exfiltrated) as total_data,
                payload_type,
                COUNT(*) as type_count
            FROM sessions
            WHERE start_time > ?
            GROUP BY payload_type
        """, (cutoff,))
        
        report = {
            'period': f"Last {days} days",
            'summary': {},
            'by_payload': []
        }
        
        for row in cursor:
            report['by_payload'].append({
                'payload_type': row[3],
                'count': row[4],
                'avg_commands': row[1],
                'total_data': row[2]
            })
        
        return report
