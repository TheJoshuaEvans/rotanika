import os
import time
import unicodedata
import threading

from typing import List, Optional

from console_styles import Colors
from strings import GameStrings
from utils import wrap_line

class ConsoleEntry:
    """
    Represents a console entry.
    """
    def __init__(self, text: str, is_input: bool = False, is_dinkus: bool = False):
        self.text = text
        self.is_input = is_input
        self.is_dinkus = is_dinkus

class Console:
    """
    Singleton class to manage console input/output operations
    """

    # --------- Internal Variables ---------
    # Singleton instance
    _instance = None

    # List to store history of console interactions
    _history: List['ConsoleEntry'] = []

    # Loading state
    _is_loading: bool = False
    """Whether the loading animation is active."""

    _loading_thread: Optional[threading.Thread] = None
    """Thread running the loading animation."""

    _loading_stop_event: Optional[threading.Event] = None
    """Event to signal the loading thread to stop."""

    _loading_history_index: int = -1
    """Index of the loading message in history."""

    #* Property Attributes *#
    border_char: str = '#'
    """Border character."""

    border_color = Colors.BLUE
    """Border color."""

    top_border_text = ''
    """Top border text."""

    break_char: str = ''
    """Break character."""

    dinkus_char: str = '='
    """Dinkus character."""

    dinkus_color: str = Colors.CYAN
    """Dinkus color."""

    input_prefix: str = '> '
    """Input prompt prefix."""

    input_color = Colors.GREEN
    """Input text color."""

    # --- Dimension Override ---
    width = 0
    """Override for console width."""

    height = 0
    """Override for console height."""

    # --------- Constructor ---------
    def __new__(cls):
        """
        Ensures only one instance of ConsoleManager exists (Singleton pattern).
        """
        if cls._instance is None:
            cls._instance = super(Console, cls).__new__(cls)
        return cls._instance

    # --------- Utility Methods ---------
    def _clear(self) -> None:
        """
        Clears the console screen using the appropriate system command.
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def _get_console_size(self) -> tuple[int, int]:
        """
        Returns the (width, height) of the console window. Returns a (0, 0) tuple if not
        attached to a terminal.

        Returns:
            tuple: (width, height) of the console window.
        """
        try:
            size = os.get_terminal_size()
            return (size.columns, size.lines)
        except OSError:
            # Fallback if not attached to a terminal
            return (self.width, self.height)

    def _generate_dinkus(self) -> str:
        """
        Generate a dinkus line.
        """
        width, _ = self._get_console_size()
        dinkus_line = self.dinkus_color + (self.dinkus_char * width) + Colors.RESET
        return dinkus_line

    def _generate_empty_line(self) -> str:
        """
        Generate an empty line with borders.
        """
        width, _ = self._get_console_size()
        empty_line = f"{self.border_color}{self.border_char}{Colors.RESET}{' ' * (width - 2)}{self.border_color}{self.border_char}{Colors.RESET}\n"
        return empty_line

    def _generate_line(self, text: str, color: str = "") -> str:
        """
        Generate a line with borders.

        Args:
            text (str): The text to include in the line.
        Returns:
            str: The formatted line with borders.
        """
        width, _ = self._get_console_size()
        padding_space = 4 # Reserve space for borders and padding

        target_line_width = width - padding_space
        lines = self._wrap_line(text)
        wrapped_lines = [self._pad_text(line, target_line_width) for line in lines]
        return ''.join(f"{self.border_color}{self.border_char}{Colors.RESET} {color}{line}{Colors.RESET} {self.border_color}{self.border_char}{Colors.RESET}\n" for line in wrapped_lines)

    def _get_display_width(self, text: str) -> int:
        """
        Calculate the display width of text, accounting for emojis and wide characters.

        Args:
            text (str): The text to measure.
        Returns:
            int: The display width of the text.
        """
        width = 0
        for char in text:
            # Emojis and wide characters take 2 columns, others take 1
            if unicodedata.east_asian_width(char) in ['W', 'F']:
                width += 2
            else:
                width += 1
        return width

    def _loading_animation_loop(self, message: str, interval: float) -> None:
        """
        Runs the loading animation loop in a background thread.

        Args:
            message (str): The base loading message.
            interval (float): The interval in seconds between dot additions.
        """
        dot_count = 0
        while self._is_loading and self._loading_stop_event is not None and not self._loading_stop_event.wait(interval):
            # Calculate max dots every run to handle console resize events
            max_dots = self._get_console_size()[0] - self._get_display_width(message) - 4  # Reserve space for borders and padding
            dot_count += 1
            # Update the loading message with dots
            if 0 <= self._loading_history_index < len(self._history):
                animated_message = message + '.' * (dot_count % (max_dots + 1))  # Cycle through 0 to max_dots dots
                self._history[self._loading_history_index].text = animated_message
                self._render()

    def _pad_text(self, text: str, target_width: int) -> str:
        """
        Pad text to target display width, accounting for emoji display width.

        Args:
            text (str): The text to pad.
            target_width (int): The target display width.
        Returns:
            str: The padded text.
        """
        current_width = self._get_display_width(text)
        padding_needed = target_width - current_width
        return text + ' ' * max(0, padding_needed)

    def _render(self):
        """
        Renders the line history to the console, leaving some space at the bottom for input
        """
        # Do this by clearing the console and then building all the lines together into a single string,
        # one line at a time, then printing that string to the console.

        # Start by building the string. We need the console size
        width, height = self._get_console_size()
        output_lines = [] # type: list[str]

        # Start building the string with the top border
        border_line = self.border_color + self.border_char * width + Colors.RESET + '\n'
        if self.top_border_text:
            output_lines.append(border_line)

            centered_text = self.top_border_text.center(width - 2) # Account for border characters
            output_lines.append(f"{self.border_color}{self.border_char}{Colors.RESET}{centered_text}{self.border_color}{self.border_char}{Colors.RESET}\n")

            output_lines.append(border_line)
        else:
            output_lines.append(border_line)

        # Add an empty line after the top border
        output_lines.append(self._generate_empty_line())
        header_lines_num = len(output_lines)

        # Now add each line from history
        for entry in self._history:
            if entry.is_dinkus:
                output_lines.append(f"{self._generate_dinkus()}\n")
            else:
                line = entry.text
                color = ""
                if entry.is_input:
                    color = self.input_color
                    line = f"{self.input_prefix}{line}"

                output_lines.append(self._generate_line(line, color=color))

        # If there were not enough lines to fill the console, add empty lines above the generated lines,
        # so that the latest input always appears at the bottom of the console, even if there is not
        # enough history to fill the console.
        while len(output_lines) < height - 4: # Reserve space for bottom border + padding and input lines
            output_lines.insert(header_lines_num, self._generate_empty_line())

        # Add an empty line before the bottom border
        output_lines.append(self._generate_empty_line())

        # Add the bottom border
        output_lines.append(f"{self.border_color}{self.border_char * width}{Colors.RESET}\n")

        # Clear the console and print the output!
        self._clear()
        print(''.join(output_lines))

    def _wrap_line(self, text: str) -> list[str]:
        """
        Wraps a line of text to fit within the console width.

        Args:
            text (str): The text to wrap.
        Returns:
            list[str]: A list of wrapped lines.
        """
        width, _ = self._get_console_size()
        target_line_width = width - 4 # Reserve space for borders and padding
        return wrap_line(text, target_line_width)

    # --------- Public Methods ---------
    def load_start(self, message: str = GameStrings.LOADING_MESSAGE, interval: float = 1) -> None:
        """
        Starts a loading animation with the given message and dot interval.
        The animation runs in a background thread and does not block the main thread.

        Args:
            message (str): The loading message to display.
            interval (float): The interval in seconds between dot additions. Defaults to 1.
        """
        # End any existing loading animation
        if self._is_loading:
            self.load_end()

        # Set up loading state
        self._is_loading = True
        self._loading_stop_event = threading.Event()
        self._loading_history_index = len(self._history)

        # Write the initial loading message
        self._history.append(ConsoleEntry(text=message, is_input=False))
        self._render()

        # Start the loading animation thread
        self._loading_thread = threading.Thread(
            target=self._loading_animation_loop,
            args=(message, interval),
            daemon=True
        )
        self._loading_thread.start()

    def load_end(self) -> None:
        """
        Stops the loading animation and replaces the loading message with a blank line.
        """
        if not self._is_loading:
            return

        # Signal the loading thread to stop
        self._is_loading = False
        if self._loading_stop_event:
            self._loading_stop_event.set()

        # Wait for the thread to finish
        if self._loading_thread and self._loading_thread.is_alive():
            self._loading_thread.join(timeout=1.0)

        # Replace the loading message with a blank line
        if 0 <= self._loading_history_index < len(self._history):
            self._history[self._loading_history_index] = ConsoleEntry(text='', is_input=False)

        # Clean up
        self._loading_thread = None
        self._loading_stop_event = None
        self._loading_history_index = -1
        self._render()

    def exit(self, code: int = 0, delay_secs: float = 1.5, message: str = GameStrings.EXIT_MESSAGE):

        """
        Exits the console application on a delay and displays an exit message

        Args:
            code (int): The exit code. Defaults to 0.
            delay_secs (float): The delay, in seconds, before exiting. Defaults to 1.5.
            message (str): Optional custom exit message. Defaults to GameStrings.EXIT_MESSAGE.
        """
        self.write_empty()
        self.write(message)
        self._render()

        time.sleep(delay_secs)
        exit(code)

    def input(self, prompt: Optional[str] = None) -> str:
        """
        Prompts the user for input and records it in history. Will render the console before prompting.
        Automatically ends any active loading animation.

        Args:
            prompt (Optional[str]): The input prompt. Defaults to the property value
        Returns:
            str: The user input.
        """
        # End loading animation if active
        if self._is_loading:
            self.load_end()

        self._render()

        try:
            user_input = input(prompt if prompt is not None else self.input_prefix)
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            self.exit(message=GameStrings.EXIT_IMMEDIATE_MESSAGE, delay_secs=0)
        except Exception as e:
            raise e

        if user_input.lower() == 'exit':
            # Handle explicit exit command
            self.exit()

        self._history.append(ConsoleEntry(text=user_input, is_input=True))
        return user_input

    def write_empty(self) -> None:
        """
        Writes an empty line to the console history.
        Automatically ends any active loading animation.
        """
        # End loading animation if active
        if self._is_loading:
            self.load_end()

        self._history.append(ConsoleEntry(text='', is_input=False))

    def write(self, text: str, overwrite: bool = False) -> None:
        """
        Writes text to the console history. Does NOT render to the console. Can optionally overwrite the
        latest console entry. Automatically ends any active loading animation.

        Args:
            text (str): The text to write.
            overwrite (bool): Whether to overwrite the last entry in history. Defaults to False.
        """
        # End loading animation if active
        if self._is_loading:
            self.load_end()

        if overwrite and self._history:
            self._history[-1] = ConsoleEntry(text=text, is_input=False)
        else:
            self._history.append(ConsoleEntry(text=text, is_input=False))

if __name__ == "__main__":
    console = Console()
    console.top_border_text = "Console Test"

    while True:
        user_input = console.input()
        console.write(f'You entered: {user_input}')
        console.write_empty()
