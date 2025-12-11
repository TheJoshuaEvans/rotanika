from enum import Enum

# All the raw number codes
class Codes:
    RESET = '0'
    BOLD = '1'
    DIM = '2'
    ITALIC = '3'
    UNDERLINE = '4'
    BLINK = '5'
    REVERSE = '7'
    HIDDEN = '8'
    STRIKETHROUGH = '9'
    RESET_BOLD = '22'
    RESET_DIM = '22'
    RESET_ITALIC = '23'
    RESET_UNDERLINE = '24'
    RESET_BLINK = '25'
    RESET_REVERSE = '27'
    RESET_HIDDEN = '28'
    RESET_STRIKETHROUGH = '29'
    COLOR_BLACK = '30'
    COLOR_RED = '31'
    COLOR_GREEN = '32'
    COLOR_YELLOW = '33'
    COLOR_BLUE = '34'
    COLOR_MAGENTA = '35'
    COLOR_CYAN = '36'
    COLOR_WHITE = '37'
    COLOR_DEFAULT = '39'
    BG_COLOR_BLACK = '40'
    BG_COLOR_RED = '41'
    BG_COLOR_GREEN = '42'
    BG_COLOR_YELLOW = '43'
    BG_COLOR_BLUE = '44'
    BG_COLOR_MAGENTA = '45'
    BG_COLOR_CYAN = '46'
    BG_COLOR_WHITE = '47'
    BG_COLOR_DEFAULT = '49'
    COLOR_BRIGHT_BLACK = '90'
    COLOR_BRIGHT_RED = '91'
    COLOR_BRIGHT_GREEN = '92'
    COLOR_BRIGHT_YELLOW = '93'
    COLOR_BRIGHT_BLUE = '94'
    COLOR_BRIGHT_MAGENTA = '95'
    COLOR_BRIGHT_CYAN = '96'
    COLOR_BRIGHT_WHITE = '97'
    BG_COLOR_BRIGHT_BLACK = '100'
    BG_COLOR_BRIGHT_RED = '101'
    BG_COLOR_BRIGHT_GREEN = '102'
    BG_COLOR_BRIGHT_YELLOW = '103'
    BG_COLOR_BRIGHT_BLUE = '104'
    BG_COLOR_BRIGHT_MAGENTA = '105'
    BG_COLOR_BRIGHT_CYAN = '106'
    BG_COLOR_BRIGHT_WHITE = '107'

def style(*codes: str) -> str:
    """
    Constructs the ANSI escape code string for given codes.

    Args:
        codes (str): The raw code strings.

    Returns:
        str: The ANSI escape code string.
    """

    # It's just a standardized magic string
    return f'\033[{";".join(codes)}m'

def remove_styles(text: str) -> str:
    """
    Removes all ANSI styles from the given text

    Args:
        text (str): The text with ANSI styles.
    Returns:
        str: The text without ANSI styles.
    """
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    return ansi_escape.sub('', text)

class Graphics:
    """
    Enum representing pre-rendered console graphics using ANSI escape codes.
    """
    RESET               = style(Codes.RESET)
    BOLD                = style(Codes.BOLD)
    DIM                 = style(Codes.DIM)
    ITALIC              = style(Codes.ITALIC)
    UNDERLINE           = style(Codes.UNDERLINE)
    BLINK               = style(Codes.BLINK)
    REVERSE             = style(Codes.REVERSE)
    HIDDEN              = style(Codes.HIDDEN)
    STRIKETHROUGH       = style(Codes.STRIKETHROUGH)
    RESET_BOLD          = style(Codes.RESET_BOLD)
    RESET_DIM           = style(Codes.RESET_DIM)
    RESET_ITALIC        = style(Codes.RESET_ITALIC)
    RESET_UNDERLINE     = style(Codes.RESET_UNDERLINE)
    RESET_BLINK         = style(Codes.RESET_BLINK)
    RESET_REVERSE       = style(Codes.RESET_REVERSE)
    RESET_HIDDEN        = style(Codes.RESET_HIDDEN)
    RESET_STRIKETHROUGH = style(Codes.RESET_STRIKETHROUGH)

class Colors:
    """
    Enum representing pre-rendered console text colors using ANSI escape codes.
    """
    RESET   = style(Codes.RESET)
    BLACK   = style(Codes.COLOR_BLACK)
    RED     = style(Codes.COLOR_RED)
    GREEN   = style(Codes.COLOR_GREEN)
    YELLOW  = style(Codes.COLOR_YELLOW)
    BLUE    = style(Codes.COLOR_BLUE)
    MAGENTA = style(Codes.COLOR_MAGENTA)
    CYAN    = style(Codes.COLOR_CYAN)
    WHITE   = style(Codes.COLOR_WHITE)
    DEFAULT = style(Codes.COLOR_DEFAULT)

class BackgroundColors:
    """
    Enum representing pre-rendered console background colors using ANSI escape codes.
    """
    RESET   = style(Codes.RESET)
    BLACK   = style(Codes.BG_COLOR_BLACK)
    RED     = style(Codes.BG_COLOR_RED)
    GREEN   = style(Codes.BG_COLOR_GREEN)
    YELLOW  = style(Codes.BG_COLOR_YELLOW)
    BLUE    = style(Codes.BG_COLOR_BLUE)
    MAGENTA = style(Codes.BG_COLOR_MAGENTA)
    CYAN    = style(Codes.BG_COLOR_CYAN)
    WHITE   = style(Codes.BG_COLOR_WHITE)
    DEFAULT = style(Codes.BG_COLOR_DEFAULT)

class BrightColors:
    """
    Enum representing pre-rendered bright console text colors using ANSI escape codes.
    """
    RESET   = style(Codes.RESET)
    BLACK   = style(Codes.COLOR_BRIGHT_BLACK)
    RED     = style(Codes.COLOR_BRIGHT_RED)
    GREEN   = style(Codes.COLOR_BRIGHT_GREEN)
    YELLOW  = style(Codes.COLOR_BRIGHT_YELLOW)
    BLUE    = style(Codes.COLOR_BRIGHT_BLUE)
    MAGENTA = style(Codes.COLOR_BRIGHT_MAGENTA)
    CYAN    = style(Codes.COLOR_BRIGHT_CYAN)
    WHITE   = style(Codes.COLOR_BRIGHT_WHITE)

class BrightBackgroundColors:
    """
    Enum representing pre-rendered bright console background colors using ANSI escape codes.
    """
    RESET   = style(Codes.RESET)
    BLACK   = style(Codes.BG_COLOR_BRIGHT_BLACK)
    RED     = style(Codes.BG_COLOR_BRIGHT_RED)
    GREEN   = style(Codes.BG_COLOR_BRIGHT_GREEN)
    YELLOW  = style(Codes.BG_COLOR_BRIGHT_YELLOW)
    BLUE    = style(Codes.BG_COLOR_BRIGHT_BLUE)
    MAGENTA = style(Codes.BG_COLOR_BRIGHT_MAGENTA)
    CYAN    = style(Codes.BG_COLOR_BRIGHT_CYAN)
    WHITE   = style(Codes.BG_COLOR_BRIGHT_WHITE)
