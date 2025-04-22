# utils/display.py

from IPython.display import clear_output
from rich.console import Console
from rich.panel import Panel
import time

def display_console(text, title="Agent Log", color="green"):
    """Displays agent messages in a styled Rich console panel."""
    clear_output(wait=True)
    console = Console()
    panel = Panel(text, title=f"[bold {color}]{title}[/bold {color}]", border_style=color)
    console.print(panel)
    time.sleep(1)  # Add delay for readability
