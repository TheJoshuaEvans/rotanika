import time

from console import Console
from utils import get_version

console = Console()
console.top_border_text = f"Rotanika v{get_version()}"

console.load_start("Loading")
while True:
    time.sleep(5)
    console.write("Loading complete!")
    console.input("Press Enter to continue...")
    break
