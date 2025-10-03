# from PyPI
from manim import *
from pydantic import validate_call, Field

# from Python standard library
from contextlib import contextmanager
from typing import Annotated
import logging, random, sys, os, time, string, re

class CodeVideo:

    @validate_call
    def __init__(
        self,
        video_name: str = "CodeVideo",
        code_string: str = None,
        code_file: str = None,
        language: str = None,
        line_spacing: float = 0.7,
        interval_range: tuple[Annotated[float, Field(ge=0.2)], Annotated[float, Field(ge=0.2)]] = (0.2, 0.2),
        camera_floating_max_value: Annotated[float, Field(ge=0)] = 0.1,
        camera_move_interval: Annotated[float, Field(ge=0)] = 0.1,
        camera_move_duration: Annotated[float, Field(ge=0)] = 0.5,
        camera_scale: float = 0.5
    ):
        if not video_name:
            raise ValueError("video_name must be provided")
        
        if interval_range[0] > interval_range[1]:
            raise ValueError("The first term of interval_range must be less than or equal to the second term")
        
        # Check code_string or code_file
        if code_string and code_file:
            raise ValueError("Only one of code_string and code_file can be provided")
        elif code_string is not None:
            code_str = code_string.replace("\t", ' '*4)
            if not code_str.isascii():
                raise ValueError("Non-ASCII characters found in the code, please remove them")
        elif code_file is not None:
            with open(os.path.abspath(code_file), "r") as f:
                try:
                    code_str = f.read().replace("\t", ' '*4)
                except UnicodeDecodeError:
                    raise ValueError("Non-ASCII characters found in the code, please remove them") from None
        else:
            raise ValueError("Either code_string or code_file must be provided")
        
        if code_str.translate(str.maketrans('', '', string.whitespace)) == '':
            raise ValueError("Code is empty")

        self.video_name = video_name
        self.code_string = code_string
        self.code_file = code_file
        self.language = language
        self.line_spacing = line_spacing
        self.interval_range = interval_range
        self.camera_floating_max_value = camera_floating_max_value
        self.camera_move_interval = camera_move_interval
        self.camera_move_duration = camera_move_duration
        self.camera_scale = camera_scale

        self.code_str = self.code_string
        self.code_str_lines = self.code_str.split("\n")
        self.scene = self._create_scene()
        self.output = True

    def without_ANSI_len(self, s) -> int:
        """Calculate the length of a string without ANSI escape sequences."""
        ansi_escape_pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned_string = ansi_escape_pattern.sub('', s)
        return len(cleaned_string)  
    
    class LoopMovingCamera(VGroup):
        """Custom camera updater for floating and smooth cursor following."""
        def __init__(
            self,
            mob,
            scene,
            move_interval,
            move_duration,
            camera_floating_max_value
        ):
            super().__init__()
            self.mob = mob
            self.scene = scene
            self.move_interval = move_interval
            self.move_duration = move_duration
            self.camera_floating_max_value = camera_floating_max_value
            self.elapsed_time = 0
            self.is_moving = False
            self.move_progress = 0
            self.start_pos = None
            self.target_pos = None
            self.last_mob_y = mob.get_y()

            self.add_updater(lambda m, dt: self.update_camera_position(dt))

        def update_camera_position(self, dt):
            """Update camera position with smooth transitions and floating effect."""
            current_mob_y = self.mob.get_y()

            # If cursor y changes, smoothly move camera to new cursor position
            if current_mob_y != self.last_mob_y:
                self.last_mob_y = current_mob_y
                self.is_moving = True
                self.move_progress = 0
                self.start_pos = self.scene.camera.frame.get_center()
                self.target_pos = self.mob.get_center()
                self.elapsed_time = 0
                return

            # Smooth interpolation while moving
            if self.is_moving:
                self.move_progress += dt / self.move_duration
                current_pos = interpolate(
                    self.start_pos,
                    self.target_pos,
                    smooth(self.move_progress)
                )
                self.scene.camera.frame.move_to(current_pos)
                if self.move_progress >= 1:
                    self.is_moving = False
                    self.move_progress = 0
                return

            self.elapsed_time += dt
            if self.elapsed_time >= self.move_interval:
                self.start_pos = self.scene.camera.frame.get_center()
                self.target_pos = self.mob.get_center() + (
                    UP * random.uniform(-self.camera_floating_max_value, self.camera_floating_max_value)
                    + LEFT * random.uniform(-self.camera_floating_max_value, self.camera_floating_max_value)
                )
                self.is_moving = True
                self.elapsed_time -= self.move_interval

    def _create_scene(self) -> MovingCameraScene:
        """Create manim scene to animate code rendering."""
        CodeVideo_self = self
        
        # ANSI color codes for terminal output
        ANSI_YELLOW = '\033[38;2;229;229;16m'
        ANSI_GREEN = '\033[38;2;13;188;121m'
        ANSI_GREY = '\033[38;2;135;135;135m'
        ANSI_RESET = '\033[0m'

        if self.video_name is None:
            raise ValueError("video_name cannot be empty")
        config.output_file = self.video_name

        output_max_width = os.get_terminal_size().columns - 19

        class code_video(MovingCameraScene):
            
            @contextmanager
            def _no_manim_output(self):
                """Context manager to suppress manim log and stderr output."""
                manim_logger = logging.getLogger("manim")
                original_manim_level = manim_logger.getEffectiveLevel()
                original_stderr = sys.stderr
                try:
                    manim_logger.setLevel(logging.WARNING)
                    sys.stderr = open(os.devnull, 'w')
                    yield
                finally:
                    manim_logger.setLevel(original_manim_level)
                    sys.stderr = original_stderr
            
            def render_output(self, text, **kwargs):
                """Print output only if enabled."""
                if CodeVideo_self.output:
                    print(text, **kwargs)

            def construct(self):
                """Build the code animation scene."""

                # Create cursor
                cursor_width = 0.0005
                cursor = RoundedRectangle(
                    height=0.35,
                    width=cursor_width,
                    corner_radius=cursor_width / 2,
                    fill_opacity=1,
                    fill_color=WHITE,
                    color=WHITE,
                ).set_z_index(2)

                # Create code block
                code_block = Code(
                    code_string=CodeVideo_self.code_str, 
                    language=CodeVideo_self.language, 
                    formatter_style="material", 
                    paragraph_config={
                        'font': 'Consolas',
                        'line_spacing': CodeVideo_self.line_spacing
                    }
                )
                line_number_mobject = code_block.submobjects[1].set_color(GREY).set_z_index(2)
                code_mobject = code_block.submobjects[2].set_z_index(2)

                number_of_lines = len(line_number_mobject)
                max_char_num_per_line = max([len(line.rstrip()) for line in CodeVideo_self.code_str_lines])
                output_char_num_per_line = min(output_max_width-number_of_lines-4, max(20, max_char_num_per_line))

                # Occupy block (placeholder for alignment)
                occupy = Code(
                    code_string=number_of_lines*(max_char_num_per_line*'#' + '\n'),
                    language=CodeVideo_self.language,
                    paragraph_config={
                        'font': 'Consolas', 
                        'line_spacing': CodeVideo_self.line_spacing
                    }
                ).submobjects[2]

                # Adjust baseline alignment
                if all(check in "acegmnopqrsuvwxyz" + string.whitespace for check in CodeVideo_self.code_str_lines[0]):
                    initial_y = code_mobject[0].get_y()
                    code_mobject[0].align_to(line_number_mobject[0], DOWN)
                    occupy[0].align_to(line_number_mobject[0], DOWN)
                    current_y = code_mobject[0].get_y()
                    offset_y = initial_y - current_y
                    code_mobject[1:].shift(DOWN*offset_y)
                    occupy[1:].shift(DOWN*offset_y)

                # Highlight rectangle
                code_line_rectangle = SurroundingRectangle(
                    VGroup(occupy[-1], line_number_mobject[-1]),
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0
                ).set_z_index(1).set_y(occupy[0].get_y())
                
                # Setup camera
                self.camera.frame.scale(CodeVideo_self.camera_scale).move_to(occupy[0][0].get_center())
                cursor.next_to(occupy[0][0], LEFT, buff=-cursor_width)
                self.add(cursor, line_number_mobject[0].set_color(WHITE), code_line_rectangle)
                self.wait()

                # Add moving camera effect
                moving_cam = CodeVideo_self.LoopMovingCamera(
                    mob=cursor,
                    scene=self,
                    move_interval=CodeVideo_self.camera_move_interval,
                    move_duration=CodeVideo_self.camera_move_duration,
                    camera_floating_max_value=CodeVideo_self.camera_floating_max_value
                )
                self.add(moving_cam)

                # Output settings summary
                hyphens = min(output_max_width, (output_char_num_per_line + len(str(number_of_lines)) + 4)) * '─'
                self.render_output(
                    f"{ANSI_GREEN}Total:{ANSI_RESET}\n"
                    f" - line: {ANSI_YELLOW}{number_of_lines}{ANSI_RESET}\n"
                    f" - character: {ANSI_YELLOW}{len(CodeVideo_self.code_str)}{ANSI_RESET}\n"
                    f"{ANSI_GREEN}Settings:{ANSI_RESET}\n"
                    f" - language: {ANSI_YELLOW}{CodeVideo_self.language if CodeVideo_self.language else '-'}{ANSI_RESET}\n"
                    f"╭{hyphens}╮"
                )

                # Iterate through code lines
                for line in range(number_of_lines):

                    line_number_mobject.set_color(GREY)
                    line_number_mobject[line].set_color(WHITE)

                    char_num = len(CodeVideo_self.code_str_lines[line].strip())

                    code_line_rectangle.set_y(occupy[line].get_y())
                    self.add(line_number_mobject[line])

                    def move_cursor_to_line_head():
                        """Move cursor to the first character in the line."""
                        cursor.next_to(occupy[line], LEFT, buff=-cursor_width)
                        self.wait(random.uniform(*CodeVideo_self.interval_range))

                    try:
                        if CodeVideo_self.code_str_lines[line][0] not in string.whitespace:
                            move_cursor_to_line_head()
                    except IndexError:
                        move_cursor_to_line_head()

                    # progress bar
                    line_number_spaces = (len(str(number_of_lines)) - len(str(line+1))) * ' '
                    this_line_number = f"{ANSI_GREY}{line_number_spaces}{line+1}{ANSI_RESET}"
                    spaces = output_char_num_per_line*' '
                    self.render_output(f"│ {this_line_number}  {spaces} │ Rendering...  {ANSI_YELLOW}0%{ANSI_RESET}", end='')

                    # if it is a empty line, skip
                    if CodeVideo_self.code_str_lines[line] == '' or char_num == 0:
                        self.render_output(f"\r│ {this_line_number}  {spaces} │ {ANSI_GREEN}√{ANSI_RESET}               ")
                        continue
                    
                    first_non_space_index = len(CodeVideo_self.code_str_lines[line]) - len(CodeVideo_self.code_str_lines[line].lstrip())

                    output_highlighted_code = first_non_space_index * " "

                    # Animate characters
                    for column in range(first_non_space_index, char_num+first_non_space_index):

                        char_mobject = code_mobject[line][column]
                        charR, charG, charB = [int(rgb*255) for rgb in char_mobject.get_color().to_rgb()]

                        if char_num > output_char_num_per_line:
                            remain_char_num = output_char_num_per_line - column
                            if remain_char_num > 3:
                                output_highlighted_code += f"\033[38;2;{charR};{charG};{charB}m{CodeVideo_self.code_str_lines[line][column]}{ANSI_RESET}"
                                code_spaces = (output_char_num_per_line - column - 1)*' '
                            elif remain_char_num == 3:
                                output_highlighted_code += "..."
                                code_spaces = (output_char_num_per_line - column - 3)*' '
                        else:
                            output_highlighted_code += f"\033[38;2;{charR};{charG};{charB}m{CodeVideo_self.code_str_lines[line][column]}{ANSI_RESET}"
                            code_spaces = (output_char_num_per_line - column - 1)*' '

                        occupy_char = occupy[line][column]
                        self.add(char_mobject)
                        cursor.next_to(occupy_char, RIGHT, buff=0.05).set_y(code_line_rectangle.get_y()) # cursor y coordinate in the same line
                        self.wait(random.uniform(*CodeVideo_self.interval_range))

                        # output progress
                        percent = int((column-first_non_space_index+1)/char_num*100)
                        percent_spaces = (3-len(str(percent)))*' '
                        self.render_output(
                            f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ "
                            f"Rendering...{ANSI_YELLOW}{percent_spaces}{percent}%{ANSI_RESET}",
                            end=''
                        )
                    
                    # Overwrite the previous progress bar
                    code_spaces = (output_char_num_per_line-len(CodeVideo_self.code_str_lines[line]))*' '
                    self.render_output(f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ {ANSI_GREEN}√{ANSI_RESET}               ")

                self.render_output(
                    f"╰{hyphens}╯\n"
                    "Combining to Movie file."
                )
                self.wait()

            def render(self):
                """Override render to add timing log."""
                start_time = time.time()
                with self._no_manim_output():
                    super().render()
                end_time = time.time()
                total_render_time = end_time - start_time
                self.render_output(
                    f"File ready at {ANSI_GREEN}'{self.renderer.file_writer.movie_file_path}'{ANSI_RESET}\n"
                    f"{ANSI_GREY}[Finished rendering in {total_render_time:.2f}s]{ANSI_RESET}"
                )

        return code_video()

    def render(self, output=True):
        """Render the scene, optionally with console output."""
        self.output = output
        self.scene.render()
