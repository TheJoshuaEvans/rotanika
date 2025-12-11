import os
import sys
import toml
import unicodedata

def display_len(text: str) -> int:
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

def get_pyproject_path():
    """
    Get the path to the pyproject.toml file, whether running in a packaged environment or not.
    """
    if getattr(sys, 'frozen', False):
        # If the application is frozen, use the temporary directory set by PyInstaller
        base_path = sys._MEIPASS # type: ignore
    else:
        # If not frozen, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'pyproject.toml')

def get_version():
    """
    Retrieve the current version of the application from the pyproject.toml file in the root directory.
    This method can be safely run in a packaged environment.
    """
    pyproject_path = get_pyproject_path()
    with open(pyproject_path, 'r') as f:
        pyproject_data = toml.load(f)
    return pyproject_data['project']['version']

def wrap_line(text: str, max_width: int) -> list[str]:
    """
    Wraps a line of text to fit within the specified maximum width.

    Args:
        text (str): The text to wrap.
        max_width (int): The maximum width of each line.

    Returns:
        list[str]: A list of wrapped lines.
    """
    words = text.split(' ')
    wrapped_lines = []
    current_line = ""

    for word in words:
        new_line = current_line + (' ' if current_line else '') + word
        if display_len(new_line) <= max_width:
            current_line = new_line
        else:
            if current_line:
                wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines
