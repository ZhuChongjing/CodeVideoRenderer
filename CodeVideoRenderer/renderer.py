# from PyPI
from manim import *
from pydantic import validate_call, Field

# from Python standard library
from contextlib import contextmanager
from typing import Annotated
import logging, random, sys, os, time, string


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
        camera_floating_maximum_value: Annotated[float, Field(ge=0)] = 0.1,
        camera_move_interval: Annotated[float, Field(ge=0)] = 0.1,
        camera_move_duration: Annotated[float, Field(ge=0)] = 0.5,
        screen_scale: float = 0.5
    ):

        if interval_range[0] > interval_range[1]:
            raise ValueError("interval_range[0] must be less than or equal to interval_range[1]")

        config.output_file = video_name

        self.video_name = video_name
        self.code_string = code_string
        self.code_file = code_file
        self.language = language
        self.line_spacing = line_spacing
        self.interval_range = interval_range
        self.camera_floating_maximum_value = camera_floating_maximum_value
        self.camera_move_interval = camera_move_interval
        self.camera_move_duration = camera_move_duration
        self.screen_scale = screen_scale

        self.code_str = self._load_code()
        self.code_str_lines = self.code_str.split("\n")
        self.scene = self._create_scene()
        self.output = True

    def _load_code(self) -> str:
        """Load code from string or file, ensure it contains only ASCII characters."""
        if self.code_string and self.code_file:
            raise ValueError("Only one of code_string and code_file can be provided")

        if self.code_string is not None:
            code_str = self.code_string.replace("\t", " " * 4)
            if not code_str.isascii():
                raise ValueError("Non-ASCII characters found in the code, please remove them")
        elif self.code_file is not None:
            with open(os.path.abspath(self.code_file), "r") as f:
                try:
                    code_str = f.read().replace("\t", " " * 4)
                except UnicodeDecodeError:
                    raise ValueError("Non-ASCII characters found in the file, please remove them") from None
        else:
            raise ValueError("Either code_string or code_file must be provided")

        if code_str.translate(str.maketrans("", "", string.whitespace)) == "":
            raise ValueError("Code is empty")

        return code_str

    class LoopMovingCamera(VGroup):
        """Custom camera updater for floating and smooth cursor following."""

        def __init__(self, mob, scene, move_interval, move_duration, camera_floating_maximum_value):
            super().__init__()
            self.mob = mob
            self.scene = scene
            self.move_interval = move_interval
            self.move_duration = move_duration
            self.camera_floating_maximum_value = camera_floating_maximum_value

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
                    smooth(self.move_progress),
                )
                self.scene.camera.frame.move_to(current_pos)
                if self.move_progress >= 1:
                    self.is_moving = False
                    self.move_progress = 0
                return

            # Floating camera effect
            self.elapsed_time += dt
            if self.elapsed_time >= self.move_interval:
                self.start_pos = self.scene.camera.frame.get_center()
                self.target_pos = self.mob.get_center() + (
                        UP * random.uniform(-self.camera_floating_maximum_value, self.camera_floating_maximum_value)
                        + LEFT * random.uniform(-self.camera_floating_maximum_value, self.camera_floating_maximum_value)
                )
                self.is_moving = True
                self.elapsed_time -= self.move_interval

    def _create_scene(self):
        """Create manim scene to animate code rendering."""
        data = self

        # ANSI color codes for terminal output
        ANSI_YELLOW = "\033[38;2;229;229;16m"
        ANSI_GREEN = "\033[38;2;13;188;121m"
        ANSI_GREY = "\033[38;2;135;135;135m"
        ANSI_RESET = "\033[0m"

        class code_video(MovingCameraScene):
            @contextmanager
            def _no_manim_output(self):
                """Context manager to suppress manim log and stderr output."""
                manim_logger = logging.getLogger("manim")
                original_manim_level = manim_logger.getEffectiveLevel()
                original_stderr = sys.stderr
                try:
                    manim_logger.setLevel(logging.WARNING)
                    sys.stderr = open(os.devnull, "w")
                    yield
                finally:
                    manim_logger.setLevel(original_manim_level)
                    sys.stderr = original_stderr

            def render_output(self, text, **kwargs):
                """Print output only if enabled."""
                if data.output:
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
                    code_string=data.code_str,
                    language=data.language,
                    formatter_style="material",
                    paragraph_config={"font": "Consolas", "line_spacing": data.line_spacing},
                )
                line_number_mobject = code_block.submobjects[1].set_color(GREY).set_z_index(2)
                code_mobject = code_block.submobjects[2].set_z_index(2)

                line_number = len(line_number_mobject)
                max_char_num_per_line = max(len(line.rstrip()) for line in data.code_str_lines)
                output_char_num_per_line = max(20, max_char_num_per_line)

                # Occupy block (placeholder for alignment)
                occupy = Code(
                    code_string=line_number * (max_char_num_per_line * "#" + "\n"),
                    language=data.language,
                    paragraph_config={"font": "Consolas", "line_spacing": data.line_spacing},
                ).submobjects[2]

                # Adjust baseline alignment
                if all(ch in "acegmnopqrsuvwxyz" + string.whitespace for ch in data.code_str_lines[0]):
                    initial_y = code_mobject[0].get_y()
                    code_mobject[0].align_to(line_number_mobject[0], DOWN)
                    occupy[0].align_to(line_number_mobject[0], DOWN)
                    offset_y = initial_y - code_mobject[0].get_y()
                    code_mobject[1:].shift(DOWN * offset_y)
                    occupy[1:].shift(DOWN * offset_y)

                # Adjust positions to remove extra white space
                code_mobject.next_to(line_number_mobject, RIGHT, buff=0.1)
                occupy.next_to(line_number_mobject, RIGHT, buff=0.1)

                # Highlight rectangle
                code_line_rectangle = SurroundingRectangle(
                    VGroup(occupy[-1], line_number_mobject[-1]),
                    color="#333333",
                    fill_opacity=1,
                    stroke_width=0,
                ).set_z_index(1).set_y(occupy[0].get_y())

                # Setup camera
                self.camera.frame.scale(data.screen_scale).move_to(code_mobject[0][0].get_center())
                cursor.next_to(code_mobject[0][0], LEFT, buff=-cursor_width)
                self.add(cursor, line_number_mobject[0].set_color(WHITE), code_line_rectangle)
                self.wait()

                # Add moving camera effect
                moving_cam = data.LoopMovingCamera(
                    mob=cursor,
                    scene=self,
                    move_interval=data.camera_move_interval,
                    move_duration=data.camera_move_duration,
                    camera_floating_maximum_value=data.camera_floating_maximum_value,
                )
                self.add(moving_cam)

                # Output settings summary
                hyphens = (output_char_num_per_line + len(str(line_number)) + 4) * "─"
                self.render_output(
                    f"{ANSI_GREEN}Total:{ANSI_RESET}\n"
                    f" - line: {ANSI_YELLOW}{line_number}{ANSI_RESET}\n"
                    f" - character: {ANSI_YELLOW}{len(data.code_str)}{ANSI_RESET}\n"
                    f"{ANSI_GREEN}Settings:{ANSI_RESET}\n"
                    f" - language: {ANSI_YELLOW}{data.language if data.language else '-'}{ANSI_RESET}\n"
                    f"╭{hyphens}╮"
                )

                # Iterate through code lines
                for line in range(line_number):
                    line_number_mobject.set_color(GREY)
                    line_number_mobject[line].set_color(WHITE)
                    char_num = len(data.code_str_lines[line].strip())

                    code_line_rectangle.set_y(occupy[line].get_y())
                    self.add(line_number_mobject[line])

                    def move_cursor_to_line_head():
                        """Move cursor to the first non-space character in the line."""
                        line_text = data.code_str_lines[line]
                        if line_text.strip():
                            first_non_space_index = len(line_text) - len(line_text.lstrip())
                            if first_non_space_index < len(code_mobject[line]):
                                cursor.next_to(code_mobject[line][first_non_space_index], LEFT, buff=-cursor_width)
                            else:
                                cursor.move_to(
                                    [code_mobject[line].get_left()[0] - cursor_width, code_line_rectangle.get_y(), 0])
                        else:
                            cursor.move_to(
                                [code_mobject[line].get_left()[0] - cursor_width, code_line_rectangle.get_y(), 0])
                        self.wait(random.uniform(*data.interval_range))

                    try:
                        if data.code_str_lines[line] and data.code_str_lines[line][0] not in string.whitespace:
                            move_cursor_to_line_head()
                    except IndexError:
                        move_cursor_to_line_head()

                    # Progress bar init
                    line_number_spaces = (len(str(line_number)) - len(str(line + 1))) * " "
                    this_line_number = f"{ANSI_GREY}{line_number_spaces}{line + 1}{ANSI_RESET}"
                    spaces = output_char_num_per_line * " "
                    self.render_output(
                        f"│ {this_line_number}  {spaces} │ Rendering...  {ANSI_YELLOW}0%{ANSI_RESET}", end=""
                    )

                    # Skip empty line
                    if not data.code_str_lines[line] or char_num == 0:
                        self.render_output(
                            f"\r│ {this_line_number}  {spaces} │ {ANSI_GREEN}√{ANSI_RESET}               "
                        )
                        continue

                    first_non_space_index = len(data.code_str_lines[line]) - len(data.code_str_lines[line].lstrip())
                    output_highlighted_code = first_non_space_index * " "

                    # Animate characters
                    for column in range(first_non_space_index, char_num + first_non_space_index):
                        char_mobject = code_mobject[line][column]
                        r, g, b = [int(rgb * 255) for rgb in char_mobject.get_color().to_rgb()]
                        output_highlighted_code += f"\033[38;2;{r};{g};{b}m{data.code_str_lines[line][column]}{ANSI_RESET}"

                        self.add(char_mobject)
                        cursor.next_to(char_mobject, RIGHT, buff=0.05).set_y(code_line_rectangle.get_y())
                        self.wait(random.uniform(*data.interval_range))

                        percent = int((column - first_non_space_index + 1) / char_num * 100)
                        percent_spaces = (3 - len(str(percent))) * " "
                        code_spaces = (output_char_num_per_line - column - 1) * " "
                        self.render_output(
                            f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ "
                            f"Rendering...{ANSI_YELLOW}{percent_spaces}{percent}%{ANSI_RESET}",
                            end="",
                        )

                    code_spaces = (output_char_num_per_line - len(data.code_str_lines[line])) * " "
                    self.render_output(
                        f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ {ANSI_GREEN}√{ANSI_RESET}               "
                    )

                self.render_output(f"╰{hyphens}╯\nCombining to Movie file.")
                self.wait()

            def render(self):
                """Override render to add timing log."""
                start_time = time.time()
                with self._no_manim_output():
                    super().render()
                total_render_time = time.time() - start_time
                self.render_output(
                    f"File ready at {ANSI_GREEN}'{self.renderer.file_writer.movie_file_path}'{ANSI_RESET}\n"
                    f"{ANSI_GREY}[Finished rendering in {total_render_time:.2f}s]{ANSI_RESET}"
                )

        return code_video()

    def render(self, output=True):
        """Render the scene, optionally with console output."""
        self.output = output
        self.scene.render()
