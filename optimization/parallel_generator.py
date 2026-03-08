# optimization/parallel_generator.py
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

class ParallelGenerator:
    """Generate multiple payloads in parallel"""
    
    def __init__(self, max_workers=None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
    
    def batch_generate(self, payload_configs):
        """Generate multiple payloads simultaneously"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            futures = []
            for config in payload_configs:
                future = executor.submit(
                    self._generate_single,
                    config
                )
                futures.append(future)
            
            # Collect results
            for future in futures:
                try:
                    result = future.result(timeout=300)
                    results.append(result)
                except Exception as e:
                    results.append({'error': str(e)})
        
        return results
    
    def _generate_single(self, config):
        """Generate single payload (thread worker)"""
        generator = PayloadGenerator(verbose=False)
        return generator.generate_payload(**config)
