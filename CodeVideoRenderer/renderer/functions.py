from contextlib import contextmanager
from io import StringIO
import logging, sys
from manim import config

from .config import *

@contextmanager
def no_manim_output():
    sys.stdout = StringIO()
    stderr_buffer = StringIO()
    sys.stderr = stderr_buffer

    manim_logger = logging.getLogger("manim")
    original_log_handlers = manim_logger.handlers.copy()
    original_log_level = manim_logger.level
    manim_logger.handlers = []
    manim_logger.setLevel(logging.CRITICAL + 1)
    config.progress_bar = "none"

    try:
        yield
    finally:
        sys.stdout = ORIGINAL_STDOUT
        sys.stderr = ORIGINAL_STDERR
        manim_logger.handlers = original_log_handlers
        manim_logger.setLevel(original_log_level)
        config.progress_bar = ORIGINAL_PROGRESS_BAR
        stderr_content = stderr_buffer.getvalue()
        if stderr_content:
            print(stderr_content, file=ORIGINAL_STDERR)

def render_output(CV, text, **kwargs):
    """Print output only if enabled."""
    if CV.output:
        print(text, file=ORIGINAL_STDOUT, **kwargs)

def strip_empty_lines(text):
    lines = text.split("\n")
    
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    
    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    
    return '\n'.join(lines[start:end])
