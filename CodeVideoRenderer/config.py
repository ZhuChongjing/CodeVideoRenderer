from string import digits, ascii_letters, punctuation
from manim import config
from rich.console import Console
import sys

# 原始标准输出和标准错误流
ORIGINAL_STDOUT = sys.stdout
ORIGINAL_STDERR = sys.stderr
ORIGINAL_PROGRESS_BAR = config.progress_bar

# 默认设置
DEFAULT_OUTPUT_VALUE = True
DEFAULT_LINE_SPACING = 0.8
DEFAULT_CURSOR_HEIGHT = 0.35
DEFAULT_CURSOR_WIDTH = 1e-4
DEFAULT_CODE_FONT = 'Consolas'
DEFAULT_CODE_FORMATTER_STYLE = 'material'
DEFAULT_CURSOR_TO_CHAR_BUFFER = 0.07
DEFAULT_TYPE_INTERVAL = 0.15
DEFAULT_LINE_BREAK_RUN_TIME = 0.4
DEFAULT_TAB_WIDTH = 4
DEFAULT_OUTPUT_CONSOLE = Console(file=ORIGINAL_STDOUT)
DEFAULT_CURSOR_BLINK_RUN_TIME = 0.5

# 其他设置
CODE_OFFSET = 0.04
EMPTY_CHARACTER = ' \t\n'
AVAILABLE_CHARACTERS = digits + ascii_letters + punctuation + EMPTY_CHARACTER
OCCUPY_CHARACTER = '('