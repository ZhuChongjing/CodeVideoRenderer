from contextlib import contextmanager
from io import StringIO
from manim import config
from functools import wraps
import logging, sys, inspect

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

def strip_empty_lines(text):
    lines = text.split("\n")
    
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    
    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    
    return '\n'.join(lines[start:end])


def type_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        
        for param_name, param_value in bound_args.arguments.items():
            param_type = sig.parameters[param_name].annotation
            if param_type is inspect.Parameter.empty:
                continue  # 无注解则不校验
            
            if not isinstance(param_value, param_type):
                raise ValueError(
                    f"Parameter '{param_name}': Expected '{param_type.__name__}', got '{type(param_value).__name__}'"
                )
        
        # 类型校验通过，执行原函数
        return func(*args, **kwargs)
    return wrapper
