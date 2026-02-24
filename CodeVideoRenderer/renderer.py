from manim import *
from pathlib import Path
from copy import copy
from typing import Literal
from timeit import timeit
import numpy as np
import random, string

from .config import *
from .typing import *
from .utils import *

class CameraFollowCursorCV:
    """
    CameraFollowCursorCV is a class designed to create animated videos that simulate the process of typing code. It animates code line by line and character by 
    character while smoothly moving the camera to follow the cursor, creating a professional-looking coding demonstration.

    Args:
        video_name (str): The name of the output video file. Defaults to `"CameraFollowCursorCV"`.
        code_string (str): The code string to be animated. Defaults to None.
        code_file (str): The path to the code file to be animated. Defaults to None.
        language (PygmentsLanguage): The programming language of the code. Defaults to None.
        renderer (Literal['cairo', 'opengl']): The renderer to use for video rendering. Defaults to `"cairo"`.
        line_spacing (float | int): The line spacing for the code. Defaults to `DEFAULT_LINE_SPACING`.
        interval_range (tuple[float | int, float | int]): The range of typing intervals between characters. Defaults to `(DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL)`.
        camera_scale (float | int): The scale factor for the camera. Defaults to 0.5.
    """

    @typeChecker
    def __init__(self,
        video_name: str = "CameraFollowCursorCV",
        code_string: str = None,
        code_file: str = None,
        language: PygmentsLanguage = None,
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
        striped_code_str = stripEmptyLines(code_str)
        self.space_positions = findSpacePositions(striped_code_str)
        self.empty_line_positions = findEmptyLinePositions(striped_code_str)
        self.code_str = replaceMiddleSpacesWithOccupyCharacter("\n".join([" " if line == "" else line for line in striped_code_str.splitlines()]))
        self.code_str_lines = self.code_str.splitlines()
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
                max_char_num_per_line = max([len(line.rstrip()) for line in self.code_str_lines])
                line_number_mobject, code_mobject = Code(
                    code_string=self.code_str + f"\n{OCCUPY_CHARACTER*max_char_num_per_line}",
                    language=self.language, 
                    formatter_style=DEFAULT_CODE_FORMATTER_STYLE, 
                    paragraph_config={
                        'font': DEFAULT_CODE_FONT,
                        'line_spacing': self.line_spacing
                    }
                ).submobjects[1:3]
                line_number_mobject.set_color(GREY)

                total_line_numbers = len(self.code_str_lines)
                total_char_numbers = len(''.join(line.strip() for line in self.code_str_lines))

                # 调整代码对齐（manim内置bug）
                if all(check in "acegmnopqrsuvwxyz+,-.:;<=>_~" + EMPTY_CHARACTER for check in self.code_str_lines[0]):
                    code_mobject.shift(DOWN*CODE_OFFSET)
                    
                # 创建代码行矩形框
                code_line_rectangle = SurroundingRectangle(
                    VGroup(code_mobject[-1], line_number_mobject[-1]),
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0
                ).set_y(code_mobject[0].get_y())
                
                # 初始化光标位置
                cursor.align_to(code_mobject[0], LEFT).set_y(code_line_rectangle.get_y())

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

                with copy(DefaultProgressBar(self.output)) as progress:
                    total_progress = progress.add_task(description="[yellow]Total[/yellow]", total=total_char_numbers)

                    # 遍历代码行
                    for line in range(total_line_numbers):

                        line_number_mobject.set_color(GREY)
                        line_number_mobject[line].set_color(WHITE)

                        char_num = len(self.code_str_lines[line].strip())
                        current_line_progress = progress.add_task(description=f"[green]Line {line+1}[/green]", total=char_num)

                        code_line_rectangle.set_y(code_mobject[line].get_y())
                        scene.add(line_number_mobject[line])

                        def move_cursor_to_line_head():
                            """Move cursor to the first character in the line."""
                            cursor.align_to(code_mobject[line], LEFT).set_y(code_line_rectangle.get_y())
                            if line != 0:
                                linebreakAnimation()
                            JUDGE_cameraScaleAnimation()
                            playAnimation(run_time=DEFAULT_LINE_BREAK_RUN_TIME)
                        
                        try:
                            # if self.code_str_lines[line][0] not in string.whitespace:
                                move_cursor_to_line_head()
                        except IndexError:
                            move_cursor_to_line_head()

                        del move_cursor_to_line_head

                        # 如果当前行为空行，跳过
                        if line in self.empty_line_positions:
                            progress.remove_task(current_line_progress)
                            continue
                        
                        first_non_space_index = len(self.code_str_lines[line]) - len(self.code_str_lines[line].lstrip())
                        total_typing_chars = char_num # 当前行实际要打的字数

                        # 遍历当前行的每个字符
                        submobjects_char_index = 0
                        for column in range(first_non_space_index, char_num + first_non_space_index):
                            # 处理manim==0.19.1更新出现的空格消失问题
                            if not self.code_str_lines[line][column].isspace():
                                if [line, column] not in self.space_positions:
                                    scene.add(code_mobject[line][submobjects_char_index])
                                submobjects_char_index += 1
                            cursor.next_to(
                                code_mobject[line][submobjects_char_index-1],
                                RIGHT,
                                buff=DEFAULT_CURSOR_TO_CHAR_BUFFER
                            ).set_y(code_line_rectangle.get_y())
                            
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
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start rendering {self.video_name}.mp4.")
                    DEFAULT_OUTPUT_CONSOLE.log("Start rendering CameraFollowCursorCVScene. [dim](by manim)[/]")
                    if config.renderer == RendererType.CAIRO:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using CPU (Cairo Renderer) for rendering.[/]')
                    else:
                        DEFAULT_OUTPUT_CONSOLE.log('[blue]Currently using GPU (OpenGL Renderer) for rendering.[/]')
                    DEFAULT_OUTPUT_CONSOLE.log("Manim's config has been modified.")
                
                # 渲染并计算时间
                with noManimOutput():
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
                    DEFAULT_OUTPUT_CONSOLE.log(f"Start adding glow effect to CameraFollowCursorCVScene.mp4. [dim](by moviepy)[/]\n")

                # 添加发光效果
                input_path = str(scene.renderer.file_writer.movie_file_path)
                output_path = '\\'.join(input_path.split('\\')[:-1]) + rf'\{self.video_name}.mp4'
                total_effect_time = timeit(lambda: addGlowEffect(input_path=input_path, output_path=output_path, output=self.output), number=1)
                if self.output:
                    DEFAULT_OUTPUT_CONSOLE.log(f"Successfully added glow effect in {total_effect_time:,.2f} seconds. [dim](by moviepy)[/]")
                    DEFAULT_OUTPUT_CONSOLE.log(f"File ready at '{output_path}'.")
                del input_path, output_path, total_effect_time

        return CameraFollowCursorCVScene()
    
    @typeChecker
    def render(self, output: bool = DEFAULT_OUTPUT_VALUE):
        """Render the scene, optionally with console output."""
        self.output = output
        self.scene.render()

__all__ = ["CameraFollowCursorCV"]