from manim import *
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from copy import copy
from contextlib import contextmanager
from io import StringIO
from functools import wraps
from typing import get_args, get_origin, Literal
from os import PathLike
from types import UnionType
from moviepy import VideoFileClip
from PIL import Image, ImageFilter, ImageEnhance
from proglog import ProgressBarLogger
from collections import OrderedDict
from timeit import timeit
import numpy as np
import random, time, string, sys, inspect, time

from .config import *

@contextmanager
def no_manim_output():
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

def strip_empty_lines(text: str):
    """
    Remove empty lines from the beginning and end of a string.
    """
    lines = text.split("\n")
    
    start = 0
    while start < len(lines) and lines[start].strip() == '':
        start += 1
    
    end = len(lines)
    while end > start and lines[end - 1].strip() == '':
        end -= 1
    
    return '\n'.join(lines[start:end])

def typeName(item_type):
    """
    Get the name of a type, handling union types and generic tuples.
    """
    if isinstance(item_type, UnionType):
        return str(item_type).replace(" | ", "' or '")
    return item_type.__name__

def type_checker(func):
    """
    Decorator to check types of function arguments and return value.
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

def add_glow_effect(input_path: PathLike, output_path: PathLike, output: bool):
    """
    Add a glow effect to a video.
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

def default_progress_bar(output: bool):
    """
    Create a Rich progress bar.
    """
    return Progress(
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
        self.progress_bar = copy(default_progress_bar(self.output))
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
        
        # elif attr == "message":
        #     # 处理消息更新（复刻原 postfix 逻辑）
        #     self.progress_bar.update(
        #         task_id,
        #         message=value[:20],  # 截断长消息
        #         description=f"{self.bars[bar]['title']}: {value[:20]}"
        #     )

    def stop(self):
        """
        Stop the Rich progress bar.
        """
        if self.progress_bar and self.progress_bar.live.is_started:
            self.progress_bar.stop()

class CameraFollowCursorCV:
    """
    CameraFollowCursorCV is a class designed to create animated videos that simulate the process of typing code. It animates code line by line and character by 
    character while smoothly moving the camera to follow the cursor, creating a professional-looking coding demonstration.
    """

    @type_checker
    def __init__(self,
        video_name: str = "CameraFollowCursorCV",
        code_string: str = None,
        code_file: str = None,
        language: Literal[
            'abap', 'amdgpu', 'apl', 'abnf', 'actionscript3', 'as3', 'actionscript', 'as', 'ada', 'ada95',
            'ada2005', 'adl', 'agda', 'aheui', 'alloy', 'ambienttalk', 'ambienttalk/2', 'at', 'ampl',
            'html+ng2', 'ng2', 'antlr-actionscript', 'antlr-as', 'antlr-csharp', 'antlr-c#', 'antlr-cpp',
            'antlr-java', 'antlr', 'antlr-objc', 'antlr-perl', 'antlr-python', 'antlr-ruby', 'antlr-rb',
            'apacheconf', 'aconf', 'apache', 'applescript', 'arduino', 'arrow', 'arturo', 'art', 'asc',
            'pem', 'asn1', 'aspectj', 'asymptote', 'asy', 'augeas', 'autoit', 'autohotkey', 'ahk', 'awk',
            'gawk', 'mawk', 'nawk', 'bbcbasic', 'bbcode', 'bc', 'bqn', 'bst', 'bst-pybtex', 'bare',
            'basemake', 'bash', 'sh', 'ksh', 'zsh', 'shell', 'openrc', 'console', 'shell-session', 'batch',
            'bat', 'dosbatch', 'winbatch', 'bdd', 'befunge', 'berry', 'be', 'bibtex', 'bib', 'blitzbasic',
            'b3d', 'bplus', 'blitzmax', 'bmax', 'blueprint', 'bnf', 'boa', 'boo', 'boogie', 'brainfuck',
            'bf', 'bugs', 'winbugs', 'openbugs', 'camkes', 'idl4', 'c', 'cmake', 'c-objdump', 'cpsa',
            'css+ul4', 'aspx-cs', 'csharp', 'c#', 'cs', 'ca65', 'cadl', 'capdl', 'capnp', 'carbon',
            'cbmbas', 'cddl', 'ceylon', 'cfengine3', 'cf3', 'chaiscript', 'chai', 'chapel', 'chpl',
            'charmci', 'html+cheetah', 'html+spitfire', 'htmlcheetah', 'javascript+cheetah', 'js+cheetah',
            'javascript+spitfire', 'js+spitfire', 'cheetah', 'spitfire', 'xml+cheetah', 'xml+spitfire',
            'cirru', 'clay', 'clean', 'clojure', 'clj', 'clojurescript', 'cljs', 'cobolfree', 'cobol',
            'codeql', 'ql', 'coffeescript', 'coffee-script', 'coffee', 'cfc', 'cfm', 'cfs', 'comal',
            'comal80', 'common-lisp', 'cl', 'lisp', 'componentpascal', 'cp', 'coq', 'cplint', 'cpp', 'c++',
            'cpp-objdump', 'c++-objdumb', 'cxx-objdump', 'crmsh', 'pcmk', 'croc', 'cryptol', 'cry', 'cr',
            'crystal', 'csound-document', 'csound-csd', 'csound', 'csound-orc', 'csound-score',
            'csound-sco', 'css+django', 'css+jinja', 'css+ruby', 'css+erb', 'css+genshitext', 'css+genshi',
            'css', 'css+php', 'css+smarty', 'cuda', 'cu', 'cypher', 'cython', 'pyx', 'pyrex', 'd',
            'd-objdump', 'dpatch', 'dart', 'dasm16', 'dax', 'debcontrol', 'control', 'debian.sources',
            'delphi', 'pas', 'pascal', 'objectpascal', 'desktop', 'devicetree', 'dts', 'dg', 'diff',
            'udiff', 'django', 'jinja', 'zone', 'docker', 'dockerfile', 'dtd', 'duel', 'jbst', 'jsonml+bst',
            'dylan-console', 'dylan-repl', 'dylan', 'dylan-lid', 'lid', 'ecl', 'ec', 'earl-grey',
            'earlgrey', 'eg', 'easytrieve', 'ebnf', 'eiffel', 'iex', 'elixir', 'ex', 'exs', 'elm', 'elpi',
            'emacs-lisp', 'elisp', 'emacs', 'email', 'eml', 'erb', 'erlang', 'erl', 'html+evoque', 'evoque',
            'xml+evoque', 'execline', 'ezhil', 'fsharp', 'f#', 'fstar', 'factor', 'fancy', 'fy', 'fan',
            'felix', 'flx', 'fennel', 'fnl', 'fift', 'fif', 'fish', 'fishshell', 'flatline', 'floscript',
            'flo', 'forth', 'fortranfixed', 'fortran', 'f90', 'foxpro', 'vfp', 'clipper', 'xbase',
            'freefem', 'func', 'fc', 'futhark', 'gap-console', 'gap-repl', 'gap', 'gdscript', 'gd', 'glsl',
            'gsql', 'gas', 'asm', 'gcode', 'genshi', 'kid', 'xml+genshi', 'xml+kid', 'genshitext', 'pot',
            'po', 'gherkin', 'cucumber', 'gleam', 'gnuplot', 'go', 'golang', 'golo', 'gooddata-cl',
            'googlesql', 'zetasql', 'gosu', 'gst', 'graphql', 'graphviz', 'dot', 'groff', 'nroff', 'man',
            'groovy', 'hlsl', 'html+ul4', 'haml', 'html+handlebars', 'handlebars', 'hare', 'haskell', 'hs',
            'haxe', 'hxsl', 'hx', 'hexdump', 'hsail', 'hsa', 'hspec', 'html+django', 'html+jinja',
            'htmldjango', 'html+genshi', 'html+kid', 'html', 'html+php', 'html+smarty', 'http', 'haxeml',
            'hxml', 'hylang', 'hy', 'hybris', 'idl', 'icon', 'idris', 'idr', 'igor', 'igorpro', 'inform6',
            'i6', 'i6t', 'inform7', 'i7', 'ini', 'cfg', 'dosini', 'io', 'ioke', 'ik', 'irc', 'isabelle',
            'j', 'jmespath', 'jp', 'jslt', 'jags', 'janet', 'jasmin', 'jasminxt', 'java',
            'javascript+django', 'js+django', 'javascript+jinja', 'js+jinja', 'javascript+ruby', 'js+ruby',
            'javascript+erb', 'js+erb', 'js+genshitext', 'js+genshi', 'javascript+genshitext',
            'javascript+genshi', 'javascript', 'js', 'javascript+php', 'js+php', 'javascript+smarty',
            'js+smarty', 'js+ul4', 'jcl', 'jsgf', 'json5', 'jsonld', 'json-ld', 'json', 'json-object',
            'jsonnet', 'jsp', 'jsx', 'react', 'jlcon', 'julia-repl', 'julia', 'jl', 'juttle', 'k', 'kal',
            'kconfig', 'menuconfig', 'linux-config', 'kernel-config', 'kmsg', 'dmesg', 'koka', 'kotlin',
            'kuin', 'kql', 'kusto', 'lsl', 'css+lasso', 'html+lasso', 'javascript+lasso', 'js+lasso',
            'lasso', 'lassoscript', 'xml+lasso', 'ldapconf', 'ldaprc', 'ldif', 'lean', 'lean3', 'lean4',
            'less', 'lighttpd', 'lighty', 'lilypond', 'limbo', 'liquid', 'literate-agda', 'lagda',
            'literate-cryptol', 'lcryptol', 'lcry', 'literate-haskell', 'lhaskell', 'lhs', 'literate-idris',
            'lidris', 'lidr', 'livescript', 'live-script', 'llvm', 'llvm-mir-body', 'llvm-mir', 'logos',
            'logtalk', 'lua', 'luau', 'mcfunction', 'mcf', 'mcschema', 'mime', 'mips', 'moocode', 'moo',
            'doscon', 'macaulay2', 'make', 'makefile', 'mf', 'bsdmake', 'css+mako', 'html+mako',
            'javascript+mako', 'js+mako', 'mako', 'xml+mako', 'maple', 'maql', 'markdown', 'md', 'mask',
            'mason', 'mathematica', 'mma', 'nb', 'matlab', 'matlabsession', 'maxima', 'macsyma', 'meson',
            'meson.build', 'minid', 'miniscript', 'ms', 'modelica', 'modula2', 'm2', 'trac-wiki', 'moin',
            'mojo', '🔥', 'monkey', 'monte', 'moonscript', 'moon', 'mosel', 'css+mozpreproc',
            'mozhashpreproc', 'javascript+mozpreproc', 'mozpercentpreproc', 'xul+mozpreproc', 'mql', 'mq4',
            'mq5', 'mql4', 'mql5', 'mscgen', 'msc', 'mupad', 'mxml', 'mysql', 'css+myghty', 'html+myghty',
            'javascript+myghty', 'js+myghty', 'myghty', 'xml+myghty', 'ncl', 'nsis', 'nsi', 'nsh', 'nasm',
            'objdump-nasm', 'nemerle', 'nesc', 'nestedtext', 'nt', 'newlisp', 'newspeak', 'nginx', 'nimrod',
            'nim', 'nit', 'nixos', 'nix', 'nodejsrepl', 'notmuch', 'nusmv', 'numpy', 'numba_ir', 'numbair',
            'objdump', 'objective-c', 'objectivec', 'obj-c', 'objc', 'objective-c++', 'objectivec++',
            'obj-c++', 'objc++', 'objective-j', 'objectivej', 'obj-j', 'objj', 'ocaml', 'octave', 'odin',
            'omg-idl', 'ooc', 'opa', 'openedge', 'abl', 'progress', 'openscad', 'org', 'orgmode',
            'org-mode', 'output', 'pacmanconf', 'pan', 'parasail', 'pawn', 'pddl', 'peg', 'perl6', 'pl6',
            'raku', 'perl', 'pl', 'phix', 'php', 'php3', 'php4', 'php5', 'pig', 'pike', 'pkgconfig',
            'plpgsql', 'pointless', 'pony', 'portugol', 'postscript', 'postscr', 'psql',
            'postgresql-console', 'postgres-console', 'postgres-explain', 'postgresql', 'postgres', 'pov',
            'powershell', 'pwsh', 'posh', 'ps1', 'psm1', 'pwsh-session', 'ps1con', 'praat', 'procfile',
            'prolog', 'promql', 'promela', 'properties', 'jproperties', 'protobuf', 'proto', 'prql',
            'psysh', 'ptx', 'pug', 'jade', 'puppet', 'pypylog', 'pypy', 'python2', 'py2', 'py2tb', 'pycon',
            'python-console', 'python', 'py', 'sage', 'python3', 'py3', 'bazel', 'starlark', 'pyi', 'pytb',
            'py3tb', 'py+ul4', 'qbasic', 'basic', 'q', 'qvto', 'qvt', 'qlik', 'qlikview', 'qliksense',
            'qlikscript', 'qml', 'qbs', 'rconsole', 'rout', 'rng-compact', 'rnc', 'spec', 'racket', 'rkt',
            'ragel-c', 'ragel-cpp', 'ragel-d', 'ragel-em', 'ragel-java', 'ragel', 'ragel-objc',
            'ragel-ruby', 'ragel-rb', 'rd', 'reasonml', 'reason', 'rebol', 'red', 'red/system', 'redcode',
            'registry', 'rego', 'resourcebundle', 'resource', 'rexx', 'arexx', 'rhtml', 'html+erb',
            'html+ruby', 'ride', 'rita', 'roboconf-graph', 'roboconf-instances', 'robotframework', 'rql',
            'rsl', 'restructuredtext', 'rst', 'rest', 'trafficscript', 'rts', 'rbcon', 'irb', 'ruby', 'rb',
            'duby', 'rust', 'rs', 'sas', 'splus', 's', 'r', 'sml', 'snbt', 'sarl', 'sass', 'savi', 'scala',
            'scaml', 'scdoc', 'scd', 'scheme', 'scm', 'scilab', 'scss', 'sed', 'gsed', 'ssed', 'shexc',
            'shex', 'shen', 'sieve', 'silver', 'singularity', 'slash', 'slim', 'slurm', 'sbatch', 'smali',
            'smalltalk', 'squeak', 'st', 'sgf', 'smarty', 'smithy', 'snobol', 'snowball', 'solidity',
            'androidbp', 'bp', 'soong', 'sophia', 'sp', 'debsources', 'sourceslist', 'sources.list',
            'sparql', 'spice', 'spicelang', 'sql+jinja', 'sql', 'sqlite3', 'squidconf', 'squid.conf',
            'squid', 'srcinfo', 'ssp', 'stan', 'stata', 'do', 'supercollider', 'sc', 'swift', 'swig',
            'systemverilog', 'sv', 'systemd', 'tap', 'tnt', 'toml', 'tablegen', 'td', 'tact', 'tads3',
            'tal', 'uxntal', 'tasm', 'tcl', 'tcsh', 'csh', 'tcshcon', 'tea', 'teal', 'teratermmacro',
            'teraterm', 'ttl', 'termcap', 'terminfo', 'terraform', 'tf', 'hcl', 'tex', 'latex', 'text',
            'ti', 'thingsdb', 'thrift', 'tid', 'tlb', 'tls', 'todotxt', 'tsql', 't-sql', 'treetop', 'tsx',
            'turtle', 'html+twig', 'twig', 'typescript', 'ts', 'typoscriptcssdata', 'typoscripthtmldata',
            'typoscript', 'typst', 'ul4', 'ucode', 'unicon', 'unixconfig', 'linuxconfig', 'urbiscript',
            'urlencoded', 'usd', 'usda', 'vbscript', 'vcl', 'vclsnippets', 'vclsnippet', 'vctreestatus',
            'vgl', 'vala', 'vapi', 'aspx-vb', 'vb.net', 'vbnet', 'lobas', 'oobas', 'sobas', 'visual-basic',
            'visualbasic', 'html+velocity', 'velocity', 'xml+velocity', 'verifpal', 'verilog', 'v', 'vhdl',
            'vim', 'visualprologgrammar', 'visualprolog', 'vue', 'vyper', 'wdiff', 'wast', 'wat', 'webidl',
            'wgsl', 'whiley', 'wikitext', 'mediawiki', 'wowtoc', 'wren', 'x10', 'xten', 'xml+ul4', 'xquery',
            'xqy', 'xq', 'xql', 'xqm', 'xml+django', 'xml+jinja', 'xml+ruby', 'xml+erb', 'xml', 'xml+php',
            'xml+smarty', 'xorg.conf', 'xpp', 'x++', 'xslt', 'xtend', 'extempore', 'yaml+jinja', 'salt',
            'sls', 'yaml', 'yang', 'yara', 'yar', 'zeek', 'bro', 'zephir', 'zig', 'ansys', 'apdl'
        ] = None,
        renderer: Literal['cairo', 'opengl'] = 'cairo',
        line_spacing: float | int = DEFAULT_LINE_SPACING,
        interval_range: tuple[float | int, float | int] = (DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL),
        camera_scale: float | int = 0.5
    ):
        # video_name
        if not video_name:
            raise ValueError("video_name must be provided")
        
        # code_string and code_file
        if code_string and code_file:
            raise ValueError("Only one of code_string and code_file can be provided")
        elif code_string is not None:
            code_str = code_string.expandtabs(tabsize=DEFAULT_TAB_WIDTH)
            if not all(char in AVAILABLE_CHARACTERS for char in code_str):
                raise ValueError("'code_string' contains invalid characters")
        elif code_file is not None:
            try:
                code_str = Path(code_file).read_text(encoding="gbk").expandtabs(tabsize=DEFAULT_TAB_WIDTH)
                if not all(char in AVAILABLE_CHARACTERS for char in code_str):
                    raise ValueError("'code_file' contains invalid characters")
            except UnicodeDecodeError:
                raise ValueError("'code_file' contains non-ASCII characters, please remove them") from None
        else:
            raise ValueError("Either code_string or code_file must be provided")
        
        if code_str.translate(str.maketrans('', '', EMPTY_CHARACTER)) == '':
            raise ValueError("Code is empty")
        
        # line_spacing
        if line_spacing <= 0:
            raise ValueError("line_spacing must be greater than 0")

        # interval_range
        shortest_possible_duration = round(1/config.frame_rate, 7)
        if not all(interval >= shortest_possible_duration for interval in interval_range):
            raise ValueError(f"interval_range must be greater than or equal to {shortest_possible_duration}")
        del shortest_possible_duration
        if interval_range[0] > interval_range[1]:
            raise ValueError("The first term of interval_range must be less than or equal to the second term")

        # 变量
        self.video_name = video_name
        self.code_string = code_string
        self.code_file = code_file
        self.language = language
        self.line_spacing = line_spacing
        self.interval_range = interval_range
        self.camera_scale = camera_scale

        # 其他
        self.code_str = strip_empty_lines(code_str)
        self.code_str_lines = self.code_str.split("\n")
        self.origin_config = {
            'disable_caching': config.disable_caching,
            'renderer': config.renderer
        }
        config.disable_caching = True
        config.renderer = renderer
        self.scene = self._create_scene()

    def _create_scene(self):
        """Create manim scene to animate code rendering."""
        class CameraFollowCursorCVScene(MovingCameraScene):

            def construct(scene):
                """Build the code animation scene."""

                # 初始化光标
                cursor = RoundedRectangle(
                    height=DEFAULT_CURSOR_HEIGHT,
                    width=DEFAULT_CURSOR_WIDTH,
                    corner_radius=DEFAULT_CURSOR_WIDTH / 2,
                    fill_opacity=1,
                    fill_color=WHITE,
                    color=WHITE
                )

                # 创建代码块
                code_block = Code(
                    code_string=self.code_str,
                    language=self.language, 
                    formatter_style=DEFAULT_CODE_FORMATTER_STYLE, 
                    paragraph_config={
                        'font': DEFAULT_CODE_FONT,
                        'line_spacing': self.line_spacing
                    }
                )
                line_number_mobject = code_block.submobjects[1].set_color(GREY)
                code_mobject = code_block.submobjects[2]

                total_line_numbers = len(line_number_mobject)
                total_char_numbers = len(''.join(line.strip() for line in self.code_str.split('\n')))
                max_char_num_per_line = max([len(line.rstrip()) for line in self.code_str_lines])

                # 占位代码块（用于对齐）
                occupy = Code(
                    code_string=total_line_numbers*(max_char_num_per_line*OCCUPY_CHARACTER + '\n'),
                    language=self.language,
                    paragraph_config={
                        'font': DEFAULT_CODE_FONT,
                        'line_spacing': self.line_spacing
                    }
                ).submobjects[2]

                # 调整代码对齐（manim内置bug）
                if all(check in "acegmnopqrsuvwxyz+,-.:;<=>_~" + EMPTY_CHARACTER for check in self.code_str_lines[0]):
                    code_mobject.shift(DOWN*CODE_OFFSET)
                    occupy.shift(DOWN*CODE_OFFSET)
                    
                # 创建代码行矩形框
                code_line_rectangle = SurroundingRectangle(
                    VGroup(occupy[-1], line_number_mobject[-1]),
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0
                ).set_y(occupy[0].get_y())
                
                # 初始化光标位置
                cursor.align_to(occupy[0][0], LEFT).set_y(occupy[0][0].get_y())

                # 适配opengl
                if config.renderer == RendererType.OPENGL:
                    scene.camera.frame = scene.camera

                # 入场动画
                target_center = cursor.get_center()
                start_center = target_center + UP * 3
                scene.camera.frame.scale(self.camera_scale).move_to(start_center)
                scene.add(code_line_rectangle, line_number_mobject[0].set_color(WHITE), cursor)

                scene.play(
                    scene.camera.frame.animate.move_to(target_center),
                    run_time=1,
                    rate_func=rate_functions.ease_out_cubic
                )
                
                # 定义固定动画
                scene.Animation_list = []
                def linebreakAnimation():
                    scene.Animation_list.append({"move_to": cursor.get_center()})

                def JUDGE_cameraScaleAnimation():
                    distance = (scene.camera.frame.get_x() - line_number_mobject.get_x()) / 14.22
                    if distance > self.camera_scale:
                        scene.Animation_list.append({"scale": distance/self.camera_scale})
                        self.camera_scale = distance

                def playAnimation(**kwargs):
                    if scene.Animation_list:
                        cameraAnimation = scene.camera.frame.animate

                        for anim in scene.Animation_list:
                            if "move_to" in anim:
                                cameraAnimation.move_to(anim["move_to"])
                            elif "scale" in anim:
                                cameraAnimation.scale(anim["scale"])
                        
                        scene.play(cameraAnimation, **kwargs)
                        scene.Animation_list.clear()
                        del cameraAnimation

                with copy(default_progress_bar(self.output)) as progress:
                    total_progress = progress.add_task(description="[yellow]Total[/yellow]", total=total_char_numbers)

                    # 遍历代码行
                    for line in range(total_line_numbers):

                        line_number_mobject.set_color(GREY)
                        line_number_mobject[line].set_color(WHITE)

                        char_num = len(self.code_str_lines[line].strip())
                        current_line_progress = progress.add_task(description=f"[green]Line {line+1}[/green]", total=char_num)

                        code_line_rectangle.set_y(occupy[line].get_y())
                        scene.add(line_number_mobject[line])

                        def move_cursor_to_line_head():
                            """Move cursor to the first character in the line."""
                            cursor.align_to(occupy[line], LEFT).set_y(occupy[line].get_y())
                            if line != 0:
                                linebreakAnimation()
                            JUDGE_cameraScaleAnimation()
                            playAnimation(run_time=DEFAULT_LINE_BREAK_RUN_TIME)
                        
                        try:
                            if self.code_str_lines[line][0] not in string.whitespace:
                                move_cursor_to_line_head()
                        except IndexError:
                            move_cursor_to_line_head()

                        del move_cursor_to_line_head

                        # 如果当前行为空行，跳过
                        if self.code_str_lines[line] == '' or char_num == 0:
                            progress.remove_task(current_line_progress)
                            continue
                        
                        first_non_space_index = len(self.code_str_lines[line]) - len(self.code_str_lines[line].lstrip())
                        total_typing_chars = char_num # 当前行实际要打的字数

                        # 遍历当前行的每个字符
                        submobjects_char_index = 0
                        for column in range(first_non_space_index, char_num + first_non_space_index):

                            occupy_char = occupy[line][column]
                            # 处理manim==0.19.1更新出现的空格消失问题
                            if not self.code_str_lines[line][column].isspace():
                                scene.add(code_mobject[line][submobjects_char_index])
                                submobjects_char_index += 1
                            cursor.next_to(occupy_char, RIGHT, buff=DEFAULT_CURSOR_TO_CHAR_BUFFER).set_y(code_line_rectangle.get_y())
                            
                            # 相机持续摆动逻辑
                            line_break = False
                            if column == first_non_space_index and first_non_space_index != 0:
                                # 如果是缩进后的第一个字符，先执行换行归位
                                linebreakAnimation()
                                line_break = True
                            else:
                                # 计算当前行的进度 (0.0 -> 1.0)
                                current_idx = column - first_non_space_index
                                max_idx = total_typing_chars - 1
                                
                                if max_idx > 0:
                                    alpha = current_idx / max_idx
                                else:
                                    alpha = 1.0
                                
                                # 包络线 sin(alpha * pi)，确保头尾为0
                                envelope = np.sin(alpha * np.pi)
                                
                                # 振荡项: sin(alpha * omega)
                                wave_count = total_typing_chars / 15
                                omega = wave_count * 2 * np.pi
                                oscillation = np.sin(alpha * omega)
                                
                                # 振幅为相机框高度的 2.5%
                                amplitude = scene.camera.frame.height * 0.025
                                offset_y = amplitude * envelope * oscillation
                                
                                target_pos = cursor.get_center() + UP * offset_y
                                scene.Animation_list.append({"move_to": target_pos})

                            # 缩放检测 & 播放
                            JUDGE_cameraScaleAnimation()
                            playAnimation(
                                run_time=DEFAULT_LINE_BREAK_RUN_TIME if line_break else random.uniform(*self.interval_range),
                                rate_func=rate_functions.smooth if line_break else rate_functions.linear
                            )

                            # 输出进度
                            progress.advance(total_progress, advance=1)
                            progress.advance(current_line_progress, advance=1)

                        progress.remove_task(current_line_progress)
                    progress.remove_task(total_progress)

                scene.wait()

            def render(scene):
                """Override render to add timing log."""
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start rendering '{self.video_name}.mp4'.")
                    DEFAULT_OUTPUT_CONSOLE.log("Start rendering CameraFollowCursorCVScene. [dim](by manim)[/]")
                    if config.renderer == RendererType.CAIRO:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using CPU (Cairo Renderer) for rendering.[/]')
                    else:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using GPU (OpenGL Renderer) for rendering.[/]')
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been modified.")
                
                # 渲染并计算时间
                with no_manim_output():
                    total_render_time = timeit(super().render, number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully rendered CameraFollowCursorCVScene in {total_render_time:,.2f} seconds. [dim](by manim)[/]")
                del total_render_time

                # 恢复配置
                config.disable_caching = self.origin_config['disable_caching']
                config.renderer = self.origin_config['renderer']
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been restored.")
                del self.origin_config
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start adding glow effect to 'CameraFollowCursorCVScene.mp4'. [dim](by moviepy)[/]\n")

                # 添加发光效果
                input_path = str(scene.renderer.file_writer.movie_file_path)
                output_path = '\\'.join(input_path.split('\\')[:-1]) + rf'\{self.video_name}.mp4'
                total_effect_time = timeit(lambda: add_glow_effect(input_path=input_path, output_path=output_path, output=self.output), number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully added glow effect in {total_effect_time:,.2f} seconds. [dim](by moviepy)[/]")
                    DEFAULT_OUTPUT_CONSOLE.log(f"File ready at '{output_path}'.")
                del input_path, output_path, total_effect_time

        return CameraFollowCursorCVScene()
    
    @type_checker
    def render(self, output: bool = DEFAULT_OUTPUT_VALUE):
        """Render the scene, optionally with console output."""
        self.output = output
        self.scene.render()