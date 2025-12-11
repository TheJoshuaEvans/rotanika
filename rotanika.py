from console import Console
from utils import get_version

console = Console()
console.top_border_text = f"Rotanika v{get_version()}"

while True:
    user_input = console.input()
    console.write(f'You entered: {user_input}')
    console.write_empty()
