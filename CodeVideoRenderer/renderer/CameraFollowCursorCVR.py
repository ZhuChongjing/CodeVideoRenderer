from manim import *
from pathlib import Path
import random, time, string, shutil

from .functions import *
from .config import *

class CameraFollowCursorCV:
    """
    CameraFollowCursorCV is a class designed to create animated videos that simulate the process of typing code. It animates code line by line and character by 
    character while smoothly moving the camera to follow the cursor, creating a professional-looking coding demonstration.
    """

    def __init__(
        self,
        video_name: str = "CameraFollowCursorCV",
        code_string: str = None,
        code_file: str = None,
        language: str = None,
        line_spacing: float = DEFAULT_LINE_SPACING,
        interval_range: tuple[float, float] = (DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL),
        camera_floating_max_value: float = 0.1,
        camera_move_interval: float = 0.1,
        camera_move_duration: float = 0.5,
        camera_scale: float = 0.5
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
        if not all(interval >= SHORTEST_POSSIBLE_DURATION for interval in interval_range):
            raise ValueError(f"interval_range must be greater than or equal to {SHORTEST_POSSIBLE_DURATION}")
        if interval_range[0] > interval_range[1]:
            raise ValueError("The first term of interval_range must be less than or equal to the second term")
        
        # camera_floating_max_value
        if camera_floating_max_value < 0:
            raise ValueError("camera_floating_max_value must be greater than or equal to 0")
        
        # camera_move_interval
        if camera_move_interval < 0:
            raise ValueError("camera_move_interval must be greater than or equal to 0")
        
        # camera_move_duration
        if camera_move_duration < 0:
            raise ValueError("camera_move_duration must be greater than or equal to 0")

        # Parameters
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

        # Other
        self.code_str = strip_empty_lines(code_str)
        self.code_str_lines = self.code_str.split("\n")
        self.scene = self._create_scene()
        self.output = DEFAULT_OUTPUT_VALUE

        config.disable_caching = True

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

    def _create_scene(self):
        """Create manim scene to animate code rendering."""
        cfccv = self

        config.output_file = self.video_name

        terminal_width = shutil.get_terminal_size().columns
        output_max_width = terminal_width - 19

        class CameraFollowCursorCVScene(MovingCameraScene):

            def construct(self):
                """Build the code animation scene."""

                # Create cursor
                cursor = RoundedRectangle(
                    height=DEFAULT_CURSOR_HEIGHT,
                    width=DEFAULT_CURSOR_WIDTH,
                    corner_radius=DEFAULT_CURSOR_WIDTH / 2,
                    fill_opacity=1,
                    fill_color=WHITE,
                    color=WHITE,
                ).set_z_index(2)

                # Create code block
                code_block = Code(
                    code_string=cfccv.code_str,
                    language=cfccv.language, 
                    formatter_style=DEFAULT_CODE_FORMATTER_STYLE, 
                    paragraph_config={
                        'font': DEFAULT_CODE_FONT,
                        'line_spacing': cfccv.line_spacing
                    }
                )
                line_number_mobject = code_block.submobjects[1].set_color(GREY).set_z_index(2)
                code_mobject = code_block.submobjects[2].set_z_index(2)

                line_numbers = len(line_number_mobject)
                max_char_num_per_line = max([len(line.rstrip()) for line in cfccv.code_str_lines])
                output_char_num_per_line = min(output_max_width-line_numbers-4, max(20, max_char_num_per_line))

                # Occupy block (placeholder for alignment)
                occupy = Code(
                    code_string=line_numbers*(max_char_num_per_line*OCCUPY_CHARACTER + '\n'),
                    language=cfccv.language,
                    paragraph_config={
                        'font': DEFAULT_CODE_FONT,
                        'line_spacing': cfccv.line_spacing
                    }
                ).submobjects[2]

                # Adjust baseline alignment
                if all(check in "acegmnopqrsuvwxyz+,-.:;<=>_~" + EMPTY_CHARACTER for check in cfccv.code_str_lines[0]):
                    code_mobject.shift(DOWN*CODE_OFFSET)
                    occupy.shift(DOWN*CODE_OFFSET)
                    
                # Highlight rectangle
                code_line_rectangle = SurroundingRectangle(
                    VGroup(occupy[-1], line_number_mobject[-1]),
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0
                ).set_z_index(1).set_y(occupy[0].get_y())
                
                # Setup camera
                self.camera.frame.scale(cfccv.camera_scale).move_to(occupy[0][0].get_center())
                cursor.align_to(occupy[0][0], LEFT).set_y(occupy[0][0].get_y())
                self.add(cursor, line_number_mobject[0].set_color(WHITE), code_line_rectangle)
                self.wait()

                # Add moving camera effect
                moving_cam = cfccv.LoopMovingCamera(
                    mob=cursor,
                    scene=self,
                    move_interval=cfccv.camera_move_interval,
                    move_duration=cfccv.camera_move_duration,
                    camera_floating_max_value=cfccv.camera_floating_max_value
                )
                self.add(moving_cam)

                # Output settings summary
                hyphens = min(output_max_width, (output_char_num_per_line + len(str(line_numbers)) + 4)) * '─'
                render_output(cfccv,
                    f"{ANSI_GREY}{'-'*terminal_width}{ANSI_RESET}\n"
                    f"{ANSI_GREY}Start Rendering '{cfccv.video_name}.mp4' (Mode: CameraFollowCursor){ANSI_RESET}\n"
                    f"{ANSI_GREEN}Total:{ANSI_RESET}\n"
                    f" - line: {ANSI_YELLOW}{line_numbers}{ANSI_RESET}\n"
                    f" - character: {ANSI_YELLOW}{len(cfccv.code_str.replace('\n', ''))}{ANSI_RESET}\n"
                    f"{ANSI_GREEN}Settings:{ANSI_RESET}\n"
                    f" - language: {ANSI_YELLOW}{cfccv.language if cfccv.language else '-'}{ANSI_RESET}\n"
                    f"╭{hyphens}╮"
                )

                # Iterate through code lines
                for line in range(line_numbers):

                    line_number_mobject.set_color(GREY)
                    line_number_mobject[line].set_color(WHITE)

                    char_num = len(cfccv.code_str_lines[line].strip())

                    code_line_rectangle.set_y(occupy[line].get_y())
                    self.add(line_number_mobject[line])

                    def move_cursor_to_line_head():
                        """Move cursor to the first character in the line."""
                        cursor.align_to(occupy[line], LEFT).set_y(occupy[line].get_y())
                        self.wait(random.uniform(*cfccv.interval_range))

                    try:
                        if cfccv.code_str_lines[line][0] not in string.whitespace:
                            move_cursor_to_line_head()
                    except IndexError:
                        move_cursor_to_line_head()

                    # progress bar
                    line_number_spaces = (len(str(line_numbers)) - len(str(line+1))) * ' '
                    this_line_number = f"{ANSI_GREY}{line_number_spaces}{line+1}{ANSI_RESET}"
                    spaces = output_char_num_per_line*' '
                    render_output(cfccv,
                        f"│ {this_line_number}  {spaces} │ Rendering...  {ANSI_YELLOW}0%{ANSI_RESET}",
                        end=''
                    )

                    # if it is a empty line, skip
                    if cfccv.code_str_lines[line] == '' or char_num == 0:
                        render_output(cfccv,
                            f"\r│ {this_line_number}  {spaces} │                 "
                        )
                        continue
                    
                    first_non_space_index = len(cfccv.code_str_lines[line]) - len(cfccv.code_str_lines[line].lstrip())

                    output_highlighted_code = first_non_space_index * " "

                    # Animate characters
                    for column in range(first_non_space_index, char_num+first_non_space_index):

                        char_mobject = code_mobject[line][column]
                        charR, charG, charB = [int(rgb*255) for rgb in char_mobject.get_color().to_rgb()]

                        if char_num > output_char_num_per_line:
                            remain_char_num = output_char_num_per_line - column
                            if remain_char_num > 3:
                                output_highlighted_code += f"\033[38;2;{charR};{charG};{charB}m{cfccv.code_str_lines[line][column]}{ANSI_RESET}"
                                code_spaces = (output_char_num_per_line - column - 1)*' '
                            elif remain_char_num == 3:
                                output_highlighted_code += "..."
                                code_spaces = (output_char_num_per_line - column - 3)*' '
                        else:
                            output_highlighted_code += f"\033[38;2;{charR};{charG};{charB}m{cfccv.code_str_lines[line][column]}{ANSI_RESET}"
                            code_spaces = (output_char_num_per_line - column - 1)*' '

                        occupy_char = occupy[line][column]
                        self.add(char_mobject)
                        cursor.next_to(occupy_char, RIGHT, buff=DEFAULT_CURSOR_TO_CHAR_BUFFER).set_y(code_line_rectangle.get_y())
                        self.wait(random.uniform(*cfccv.interval_range))

                        # output progress
                        percent = int((column-first_non_space_index+1)/char_num*100)
                        percent_spaces = (3-len(str(percent)))*' '
                        render_output(cfccv,
                            f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ "
                            f"Rendering...{ANSI_YELLOW}{percent_spaces}{percent}%{ANSI_RESET}",
                            end=''
                        )
                    
                    # Overwrite the previous progress bar
                    code_spaces = (output_char_num_per_line-len(cfccv.code_str_lines[line]))*' '
                    render_output(cfccv,
                        f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │                 "
                    )

                render_output(cfccv,
                    f"╰{hyphens}╯"
                )
                self.wait()

            def render(self):
                """Override render to add timing log."""
                start_time = time.time()
                with no_manim_output():
                    super().render()
                end_time = time.time()
                total_render_time = end_time - start_time
                render_output(cfccv,
                    f"File ready at {ANSI_GREEN}'{self.renderer.file_writer.movie_file_path}'{ANSI_RESET}\n"
                    f"{ANSI_GREY}Rendering finished in {total_render_time:.2f}s{ANSI_RESET}\n"
                    f"{ANSI_GREY}{'-'*terminal_width}{ANSI_RESET}"
                )
                del start_time, end_time, total_render_time

        return CameraFollowCursorCVScene()

    def render(self, output: bool = DEFAULT_OUTPUT_VALUE):
        """Render the scene, optionally with console output."""
        if not isinstance(output, bool):
            raise ValueError("'output' must be a boolean value")
        self.output = output
        self.scene.render()
