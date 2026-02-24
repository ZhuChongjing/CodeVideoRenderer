from manim import *
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from copy import copy
from contextlib import contextmanager
from io import StringIO
from functools import wraps
from typing import get_args, get_origin, Literal, Generator, Any, Callable
from os import PathLike
from types import UnionType
from moviepy import VideoFileClip
from PIL import Image, ImageFilter, ImageEnhance
from proglog import ProgressBarLogger
from collections import OrderedDict
import numpy as np
import time, sys, inspect

from .config import *

@contextmanager
def noManimOutput() -> Generator[None, Any, None]:
    """
    Context manager used to execute code without outputting Manim logs.
    """
    sys.stdout = StringIO()
    stderr_buffer = StringIO()
    sys.stderr = stderr_buffer
    config.progress_bar = "none"

    try:
        yield
    finally:
        sys.stdout = ORIGINAL_STDOUT
        sys.stderr = ORIGINAL_STDERR
        config.progress_bar = ORIGINAL_PROGRESS_BAR
        stderr_content = stderr_buffer.getvalue()
        if stderr_content:
            print(stderr_content, file=ORIGINAL_STDERR)

def stripEmptyLines(text: str) -> str:
    """
    Remove empty lines from the beginning and end of a string.

    Args:
        text (str): The input string to process.
        
    Returns:
        str: The string with empty lines removed from the beginning and end.
    """
    lines = text.split("\n")
    
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    
    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    
    return '\n'.join(lines[start:end])

def typeName(item_type: type) -> str:
    """
    Get the name of a type, handling union types and generic tuples.

    Args:
        item_type (type): The type to get the name of.
        
    Returns:
        str: The name of the type.
    """
    if isinstance(item_type, UnionType):
        return str(item_type).replace(" | ", "' or '")
    return item_type.__name__

def typeChecker(func: Callable) -> Callable:
    """
    Decorator to check types of function arguments and return value.

    Args:
        func (Callable): The function to decorate.
        
    Returns:
        Callable: The wrapped function with type checking.
    """
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
                    
            elif get_origin(param_type) is Literal:
                # 校验是否为 Literal 中的值
                if param_value not in get_args(param_type):
                    raise ValueError(
                        f"Parameter '{param_name}': Expected value in {get_args(param_type)}, got '{param_value}'"
                    )
            
            # 普通类型
            else:
                if not isinstance(param_value, param_type):
                    raise TypeError(f"Parameter '{param_name}': Expected '{typeName(param_type)}', got '{type(param_value).__name__}'")
                        
        return func(*args, **kwargs)
    return wrapper

def addGlowEffect(input_path: PathLike, output_path: PathLike, output: bool) -> None:
    """
    Add a glow effect to a video.

    Args:
        input_path (PathLike): Path to the input video file.
        output_path (PathLike): Path to save the output video file.
        output (bool): Whether to display progress bars.
        
    Returns:
        None
    """
    # 内部帧处理函数
    def _frame_glow(t: np.ndarray):
        # 获取MoviePy的numpy帧并转为PIL图像
        frame = t.astype(np.uint8)
        pil_img = Image.fromarray(frame).convert("RGBA")

        # 提升基础亮度
        brightness_enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = brightness_enhancer.enhance(1.2)

        # 创建模糊光晕层
        glow = pil_img.filter(ImageFilter.GaussianBlur(radius=10))

        # 提升光晕的亮度和饱和度
        glow_bright_enhancer = ImageEnhance.Brightness(glow)
        glow = glow_bright_enhancer.enhance(1.5)
        glow_color_enhancer = ImageEnhance.Color(glow)
        glow = glow_color_enhancer.enhance(1.2)

        # 混合原图像与光晕层
        soft_glow_img = Image.blend(glow, pil_img, 0.4)
        glow_frame = np.array(soft_glow_img.convert("RGB")).astype(np.uint8)
        return np.clip(glow_frame, 0, 255)
    
    glow_video: VideoFileClip = VideoFileClip(input_path).image_transform(_frame_glow)
    glow_video.write_videofile(output_path, codec='libx264', audio=True, logger=RichProgressBarLogger(output=output, title="Glow Effect", leave_bars=False))

def findSpacePositions(string: str) -> list[list[int]]:
    """
    Find the 2D positions of all non-leading, non-trailing spaces in a string.
    Each position is represented as a list `[row_index, column_index]`.
    
    Args:
        string (str): A string.
        
    Returns:
        list[list[int]]: A list of 2D positions of all non-leading, non-trailing spaces.
        Each position is represented as a list `[row_index, column_index]`.
    """
    result = []  # 存储所有[行, 列]格式的空格位置
    for row_idx, s in enumerate(string.splitlines()):
        # 找到第一个非空格字符的列索引
        first_non_space = 0
        while first_non_space < len(s) and s[first_non_space] == ' ':
            first_non_space += 1
        
        # 找到最后一个非空格字符的列索引
        last_non_space = len(s) - 1
        while last_non_space >= 0 and s[last_non_space] == ' ':
            last_non_space -= 1
        
        # 全空格/空字符串，跳过
        if first_non_space > last_non_space:
            result.extend([[row_idx, col_idx] for col_idx in range(len(s))])  # 记录整行空格位置
            continue
        
        # 遍历中间部分，收集[行, 列]格式的位置
        for col_idx in range(first_non_space, last_non_space + 1):
            if s[col_idx] == ' ':
                result.append([row_idx, col_idx])
    
    return result

def findEmptyLinePositions(string: str) -> list[int]:
    """
    Find the line indices of all empty lines in a string.
    
    Args:
        string (str): A string.
        
    Returns:
        list[int]: A list of line indices of all empty lines.
    """
    return [idx for idx, line in enumerate(string.splitlines()) if line.strip() == '']

def replaceMiddleSpacesWithOccupyCharacter(string: str) -> str:
    """
    Replace all non-leading, non-trailing spaces in the input string with `OCCUPY_CHARACTER`.
    Retain leading and trailing spaces.
    
    Args:
        string (str): Original string.
        
    Returns:
        str: Processed string with middle spaces replaced by `OCCUPY_CHARACTER`.
    """
    result = []
    for s in string.splitlines():
        # 处理非字符串元素，直接保留原元素
        if not isinstance(s, str):
            result.append(s)
            continue
        
        # 空字符串直接保留
        if len(s) == 0:
            result.append(s)
            continue
        
        # 转为列表方便修改字符
        s_list = list(s)
        
        # 找到第一个非空格字符的索引
        first_non_space = 0
        while first_non_space < len(s_list) and s_list[first_non_space] == ' ':
            first_non_space += 1
        
        # 找到最后一个非空格字符的索引
        last_non_space = len(s_list) - 1
        while last_non_space >= 0 and s_list[last_non_space] == ' ':
            last_non_space -= 1
        
        # 全是空格的情况，直接保留原字符串
        if first_non_space > last_non_space:
            result.append(s.replace(' ', OCCUPY_CHARACTER))
            continue
        
        # 遍历中间区域，替换空格为1
        for idx in range(first_non_space, last_non_space + 1):
            if s_list[idx] == ' ':
                s_list[idx] = OCCUPY_CHARACTER
        
        # 转回字符串并加入结果
        result.append(''.join(s_list))
    
    return '\n'.join(result)

class DefaultProgressBar(Progress):
    """
    Default progress bar.
    """
    def __init__(self, output: bool):
        super().__init__(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[yellow]{task.completed}/{task.total}"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TransferSpeedColumn(),
            console=DEFAULT_OUTPUT_CONSOLE if output else None
        )

class RichProgressBarLogger(ProgressBarLogger):
    """
    A progress logger that uses Rich to display progress bars.
    """
    def __init__(
        self,
        output: bool,
        title: str,
        init_state=None,
        bars=None,
        leave_bars=True,
        ignored_bars=None,
        logged_bars="all",
        print_messages=True,
        min_time_interval=0.1,
        ignore_bars_under=0,
    ):
        # 调用父类构造函数，初始化核心属性
        super().__init__(
            init_state=init_state,
            bars=bars,
            ignored_bars=ignored_bars,
            logged_bars=logged_bars,
            ignore_bars_under=ignore_bars_under,
            min_time_interval=min_time_interval,
        )
        
        # 初始化自定义属性
        self.leave_bars = leave_bars
        self.print_messages = print_messages
        self.output = output
        self.title = title
        self.start_time = time.time()
        
        # 初始化 Rich 进度条
        self.progress_bar = copy(DefaultProgressBar(self.output))
        self.rich_bars = OrderedDict()  # 存储 {bar_name: task_id}
        
        # 启动 Rich 进度条
        if self.progress_bar and not self.progress_bar.live.is_started:
            self.progress_bar.start()

    def new_tqdm_bar(self, bar):
        """
        Create a Rich progress bar task for the given bar.
        """
        if not self.output or self.progress_bar is None:
            return
        
        # 关闭已有进度条
        if bar in self.rich_bars:
            self.close_tqdm_bar(bar)
        
        # 获取父类维护的进度条信息
        infos = self.bars[bar]
        # 创建 Rich 进度条任务
        task_id = self.progress_bar.add_task(description=f"[yellow]{self.title}[/yellow]", total=infos["total"])
        self.rich_bars[bar] = task_id

    def close_tqdm_bar(self, bar):
        """
        Close the Rich progress bar task for the given bar.
        """
        if not self.output or self.progress_bar is None:
            return
        
        if bar in self.rich_bars:
            task_id = self.rich_bars[bar]
            # 若不需要保留，移除任务
            if not self.leave_bars:
                self.progress_bar.remove_task(task_id)
            del self.rich_bars[bar]

    def bars_callback(self, bar, attr, value, old_value):
        """
        Update the Rich progress bar task based on the attribute change.
        """
        if bar not in self.rich_bars:
            self.new_tqdm_bar(bar)
        
        task_id = self.rich_bars.get(bar)
        if attr == "index":
            # 处理帧数更新（核心）
            if value >= old_value:
                total = self.bars[bar]["total"]
                # 计算处理速度
                elapsed = time.time() - self.start_time
                speed = value / elapsed if elapsed > 0 else 0.0
                
                # 更新 Rich 进度条
                self.progress_bar.update(
                    task_id,
                    completed=value,
                    speed=speed
                )
                
                # 完成后关闭（复刻原逻辑）
                if total and (value >= total):
                    self.close_tqdm_bar(bar)
            else:
                # 帧数回退：重置进度条
                self.new_tqdm_bar(bar)
                self.progress_bar.update(self.rich_bars[bar], completed=value)

    def stop(self):
        """
        Stop the Rich progress bar.
        """
        if self.progress_bar and self.progress_bar.live.is_started:
            self.progress_bar.stop()

__all__ = [
    "noManimOutput",
    "stripEmptyLines",
    "typeName",
    "typeChecker",
    "addGlowEffect",
    "findSpacePositions",
    "findEmptyLinePositions",
    "replaceMiddleSpacesWithOccupyCharacter",
    "DefaultProgressBar",
    "RichProgressBarLogger"
]