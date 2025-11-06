from string import digits, ascii_letters, punctuation
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
from rich.console import Console
from manim import config
import sys

ORIGINAL_STDOUT = sys.stdout
ORIGINAL_STDERR = sys.stderr
ORIGINAL_PROGRESS_BAR = config.progress_bar

ANSI_YELLOW = '\033[38;2;229;229;16m'
ANSI_GREEN = '\033[38;2;13;188;121m'
ANSI_BLUE = '\033[38;2;78;142;211m'
ANSI_GREY = '\033[38;2;135;135;135m'
ANSI_RESET = '\033[0m'

DEFAULT_OUTPUT_VALUE = True
DEFAULT_LINE_SPACING = 0.8
DEFAULT_CURSOR_HEIGHT = 0.35
DEFAULT_CURSOR_WIDTH = 0.0005
DEFAULT_CODE_FONT = 'Cascadia Code'
DEFAULT_CODE_FORMATTER_STYLE = 'material'
DEFAULT_CURSOR_TO_CHAR_BUFFER = 0.03
DEFAULT_TYPE_INTERVAL = 0.15
DEFAULT_TAB_WIDTH = 4

INDENT = "    "
CODE_OFFSET = 0.06
EMPTY_CHARACTER = ' \t\n'
AVAILABLE_CHARACTERS = digits + ascii_letters + punctuation + EMPTY_CHARACTER
OCCUPY_CHARACTER = '#'
SHORTEST_POSSIBLE_DURATION = 0.0166667
PROGRESS_BAR = Progress(
    TextColumn("[yellow][progress.description]{task.description}"),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
    TextColumn("[green]{task.completed}/{task.total}"),
    TimeRemainingColumn(),
    console=Console(file=ORIGINAL_STDOUT)
)
CURSOR_MAX_X = 6
CURSOR_MIN_Y = -3
