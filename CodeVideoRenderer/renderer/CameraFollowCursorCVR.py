from manim import *
from pathlib import Path
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.panel import Panel
import random, time, string, shutil
import numpy as np

from .functions import *
from .config import *

config.disable_caching = True

class CameraFollowCursorCV:
    """
    CameraFollowCursorCV is a class designed to create animated videos that simulate the process of typing code. It animates code line by line and character by 
    character while smoothly moving the camera to follow the cursor, creating a professional-looking coding demonstration.
    """

    @type_checker
    def __init__(
        self,
        video_name: str = "CameraFollowCursorCV",
        code_string: str = None,
        code_file: str = None,
        language: str = None,
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
        self.scene = self._create_scene()
        self.output = DEFAULT_OUTPUT_VALUE

    def _create_scene(self):
        """Create manim scene to animate code rendering."""
        config.output_file = self.video_name
        terminal_width = shutil.get_terminal_size().columns

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
                    color=WHITE,
                ).set_z_index(2)

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
                line_number_mobject = code_block.submobjects[1].set_color(GREY).set_z_index(2)
                code_mobject = code_block.submobjects[2].set_z_index(2)

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
                ).set_z_index(1).set_y(occupy[0].get_y())
                
                # 初始化光标位置
                cursor.align_to(occupy[0][0], LEFT).set_y(occupy[0][0].get_y())

                # 入场动画
                target_center = cursor.get_center()
                start_center = target_center + UP * 3
                scene.camera.frame.scale(self.camera_scale).move_to(start_center)
                scene.add(cursor, line_number_mobject[0].set_color(WHITE), code_line_rectangle)

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

                # 输出渲染信息
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.print(
                        f"{MARKUP_GREY}{'-'*terminal_width}{MARKUP_RESET}\n"
                        f"{MARKUP_GREY}Start Rendering '{self.video_name}.mp4'{MARKUP_RESET}\n",
                        Panel(
                            f"{MARKUP_GREEN}Total:{MARKUP_RESET}\n"
                            f" - line: {MARKUP_YELLOW}{total_line_numbers}{MARKUP_RESET}\n"
                            f" - character: {MARKUP_YELLOW}{total_char_numbers}{MARKUP_RESET}\n"
                            f"{MARKUP_GREEN}Settings:{MARKUP_RESET}\n"
                            f" - language: {MARKUP_ITALIC}{MARKUP_YELLOW}{self.language if self.language else '-'}{MARKUP_RESET}",
                            border_style="blue",
                            title="Summary",
                            expand=False,
                        )
                    )

                with Progress(
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[yellow]{task.completed}/{task.total}"),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeRemainingColumn(),
                    TransferSpeedColumn(),
                    console=DEFAULT_OUTPUT_CONSOLE if self.output else None
                ) as progress:
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
                        for column in range(first_non_space_index, char_num+first_non_space_index):

                            occupy_char = occupy[line][column]
                            scene.add(code_mobject[line][column])
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

                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.print("Please wait...\n", markup=False)
                scene.wait()

            def render(scene):
                """Override render to add timing log."""
                start_time = time.time()
                with no_manim_output():
                    super().render()
                end_time = time.time()
                total_render_time = end_time - start_time
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.print(
                        f"File ready at {MARKUP_GREEN}'{scene.renderer.file_writer.movie_file_path}'{MARKUP_RESET}\n"
                        f"{MARKUP_GREY}Rendering finished in {total_render_time:.2f}s{MARKUP_RESET}\n"
                        f"{MARKUP_GREY}{'-'*terminal_width}{MARKUP_RESET}",
                    )

        return CameraFollowCursorCVScene()

    @type_checker
    def render(self, output: bool = DEFAULT_OUTPUT_VALUE):
        """Render the scene, optionally with console output."""
        self.output = output
        self.scene.render()