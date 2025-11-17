from contextlib import contextmanager
from io import StringIO
from manim import config
from functools import wraps
from typing import get_args, get_origin
from types import UnionType
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

def typeName(item_type):
    if isinstance(item_type, UnionType):
        return str(item_type).replace(" | ", "' or '")
    return item_type.__name__

def type_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        
        for param_name, param_value in bound_args.arguments.items():
            param_type = sig.parameters[param_name].annotation
            if param_type is inspect.Parameter.empty:
                continue  # 无注解则跳过
            
            # 处理带参数的泛型 tuple（如 tuple[float, float]）
            if get_origin(param_type) is tuple:
                # 校验是否为 tuple 实例
                if not isinstance(param_value, tuple):
                    raise TypeError(
                        f"Parameter '{param_name}': Expected 'tuple', got '{type(param_value).__name__}'"
                    )
                # 校验长度和元素类型
                item_types = get_args(param_type)
                if len(param_value) != len(item_types):
                    raise ValueError(
                        f"Parameter '{param_name}' length mismatch: Expected {len(item_types)}, got {len(param_value)}"
                    )
                for idx, (item, item_type) in enumerate(zip(param_value, item_types)):
                    if not isinstance(item, item_type):
                        raise TypeError(
                            f"Parameter '{param_name}' item (index: {idx}): Expected '{typeName(item_type)}', got '{type(item).__name__}'"
                        )
            
            # 普通类型
            else:
                if not isinstance(param_value, param_type):
                        raise TypeError(f"Parameter '{param_name}': Expected '{typeName(param_type)}', got '{type(param_value).__name__}'")
                        
        
        return func(*args, **kwargs)
    return wrapper
