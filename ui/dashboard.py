# ui/dashboard.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.layout import Layout
from rich.live import Live

class Dashboard:
    """Interactive real-time dashboard"""
    
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.setup_layout()
    
    def setup_layout(self):
        """Setup dashboard layout"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        self.layout["main"].split_row(
            Layout(name="jobs"),
            Layout(name="stats"),
            Layout(name="sessions")
        )
    
    def display_jobs(self, jobs):
        """Display active jobs"""
        table = Table(title="Active Jobs")
        table.add_column("ID")
        table.add_column("Payload")
        table.add_column("Target")
        table.add_column("Status")
        table.add_column("Progress")
        
        for job in jobs:
            table.add_row(
                str(job['id']),
                job['payload'],
                job['target'],
                job['status'],
                f"{job['progress']}%"
            )
        
        return table
    
    def display_stats(self, stats):
        """Display statistics"""
        content = f"""
        Total Payloads: {stats['total']}
        Success Rate: {stats['success_rate']}%
        Active Sessions: {stats['active_sessions']}
        Data Transferred: {stats['data_transferred']} MB
        """
        return Panel(content, title="Statistics")
    
    def live_dashboard(self, jobs, stats, sessions):
        """Show live updating dashboard"""
        with Live(self.layout, refresh_per_second=4) as live:
            while True:
                self.layout["header"].update(
                    Panel("Payload Generator v3.0", style="bold cyan")
                )
                self.layout["jobs"].update(self.display_jobs(jobs))
                self.layout["stats"].update(self.display_stats(stats))
                self.layout["sessions"].update(self.display_sessions(sessions))
                self.layout["footer"].update(
                    Panel("Press 'q' to quit", style="bold yellow")
                )
                time.sleep(0.25)
