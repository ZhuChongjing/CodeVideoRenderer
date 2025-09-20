# from PyPI
from manim import *
from pydantic import validate_call, Field
import logging
# from Python standard library
from contextlib import contextmanager
from typing import Annotated
import random, sys, os, time, string

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
            raise ValueError("interval_range[0] must be less than interval_range[1]")
        
        # logging.basicConfig(level=logging.INFO)
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

    def _load_code(self):
        if self.code_string and self.code_file:
            raise ValueError("Only one of code_string and code_file can be passed in")

        # get code string and check if it contains chinese characters or punctuation
        if self.code_string is not None:
            code_str = self.code_string.replace("\t", 4*' ')
            if not code_str.isascii():
                raise ValueError("There are non-English characters in the code, please remove them")
        elif self.code_file is not None:
            with open(os.path.abspath(self.code_file), "r") as f:
                try:
                    code_str = f.read().replace("\t", 4*' ')
                except UnicodeDecodeError:
                    raise ValueError("There are non-English characters in the code, please remove them") from None
        
        if code_str.translate(str.maketrans('', '', string.whitespace)) == '':
            raise ValueError("code is empty")
        
        return code_str

    class LoopMovingCamera(VGroup):
        def __init__(
            self,
            mob,
            scene,
            move_interval,
            move_duration,
            camera_floating_maximum_value
        ):
            super().__init__()
            self.mob = mob
            self.scene = scene
            self.move_interval = move_interval
            self.move_duration = move_duration
            self.camera_floating_maximum_value = camera_floating_maximum_value
            self.elapsed_time = 0
            self.is_moving = False  # whether it is moving
            self.move_progress = 0  # move progress (0 to 1)
            self.start_pos = None   # move start position
            self.target_pos = None  # move target position
            self.last_mob_y = mob.get_y()  # last mob y position

            self.add_updater(lambda m, dt: self.update_camera_position(dt))

        def update_camera_position(self, dt):
            # whether y position of mob changes
            current_mob_y = self.mob.get_y()
            if current_mob_y != self.last_mob_y:
                # y position of mob changes: smooth move camera to mob position
                self.last_mob_y = current_mob_y  # update last mob y position
                # reset current moving state, prepare for new smooth move
                self.is_moving = True
                self.move_progress = 0
                self.start_pos = self.scene.camera.frame.get_center()  # current camera position as start point
                self.target_pos = self.mob.get_center()  # mob position as new target
                self.elapsed_time = 0  # reset timer
                return

            # original automatic moving logic (not affected)
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
                    UP * random.uniform(-self.camera_floating_maximum_value, self.camera_floating_maximum_value) +
                    LEFT * random.uniform(-self.camera_floating_maximum_value, self.camera_floating_maximum_value)
                )
                self.is_moving = True
                self.elapsed_time -= self.move_interval

    def _create_scene(self):
        data = self

        class code_video(MovingCameraScene):
            
            # no manim output
            @contextmanager
            def _no_manim_output(self):
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
                if data.output:
                    print(text, **kwargs)

            def construct(self):

                # initialize cursor
                cursor_width = 0.0005
                cursor = RoundedRectangle(height=0.35, width=cursor_width, corner_radius=cursor_width/2, 
                                        fill_opacity=1, fill_color=WHITE, color=WHITE).set_z_index(2)
                
                # initialize code block
                code_block = Code(code_string=data.code_str, 
                                language=data.language, 
                                formatter_style='material', 
                                paragraph_config={
                                    'font': 'Consolas',
                                    'line_spacing': data.line_spacing
                                    })
                line_number_mobject = code_block.submobjects[1].set_color(GREY).set_z_index(2) # line numbers
                code_mobject = code_block.submobjects[2].set_z_index(2) # code

                line_number = len(line_number_mobject)
                max_char_num_per_line = max([len(data.code_str_lines[i].rstrip()) for i in range(line_number)])
                output_char_num_per_line = max(20, max_char_num_per_line)

                # occupy block
                # use '#' to occupy, prevent no volume space
                occupy = Code(
                    code_string=line_number*(max_char_num_per_line*'#' + '\n'),
                    language=data.language,
                    paragraph_config={'font': 'Consolas', 'line_spacing': data.line_spacing}
                ).submobjects[2]

                # align line numbers and codes
                for check in data.code_str_lines[0]:
                    if check not in "acegmnopqrsuvwxyz"+string.whitespace:
                        break
                else:
                    initial_y = code_mobject[0].get_y()
                    code_mobject[0].align_to(line_number_mobject[0], DOWN)
                    occupy[0].align_to(line_number_mobject[0], DOWN)
                    current_y = code_mobject[0].get_y()
                    code_mobject[1:].shift(DOWN*(initial_y-current_y))
                    occupy[1:].shift(DOWN*(initial_y-current_y))

                code_line_rectangle = SurroundingRectangle(VGroup(occupy[-1], line_number_mobject[-1]), 
                                                        color="#333333", fill_opacity=1, stroke_width=0
                                                        ).set_z_index(1).set_y(occupy[0].get_y())
                
                self.camera.frame.scale(data.screen_scale).move_to(occupy[0][0].get_center())
                cursor.next_to(occupy[0][0], LEFT, buff=-cursor_width) # cursor move to the left of occupy block
                self.add(cursor, line_number_mobject[0].set_color(WHITE), code_line_rectangle)
                self.wait()

                # create loop moving camera
                moving_cam = data.LoopMovingCamera(
                    mob=cursor,
                    scene=self,
                    move_interval=data.camera_move_interval,
                    move_duration=data.camera_move_duration,
                    camera_floating_maximum_value=data.camera_floating_maximum_value
                )
                self.add(moving_cam)

                hyphens = (output_char_num_per_line+len(str(line_number))+4)*'─'
                self.render_output(f"\033[32mTotal:\033[0m\n"
                    f" - line: \033[33m{line_number}\033[0m\n"
                    f" - character: \033[33m{len(data.code_str)}\033[0m\n"
                    f"\033[32mSettings:\033[0m\n"
                    f" - language: \033[33m{data.language if data.language else '-'}\033[0m\n"
                    f"╭{hyphens}╮")

                # traverse code lines
                for line in range(line_number):

                    # set line number color
                    line_number_mobject.set_color(GREY)
                    line_number_mobject[line].set_color(WHITE)

                    # code line character number, exclude the trailing spaces
                    char_num = len(data.code_str_lines[line].strip())

                    code_line_rectangle.set_y(occupy[line].get_y())
                    self.add(line_number_mobject[line]) # add line number

                    def move_cursor_to_line_head():
                        cursor.next_to(occupy[line], LEFT, buff=-cursor_width) # cursor move to the left of occupy block
                        self.wait(random.uniform(*data.interval_range))

                    try:
                        if data.code_str_lines[line][0] not in string.whitespace:
                            move_cursor_to_line_head()
                    except IndexError:
                        move_cursor_to_line_head()

                    # progress bar
                    line_number_spaces = (len(str(line_number))-len(str(line+1)))*' '
                    this_line_number = f"\033[30m{line_number_spaces}{line+1}\033[0m"
                    spaces = output_char_num_per_line*' '
                    self.render_output(f"│ {this_line_number}  {spaces} │ Rendering...  \033[33m0%\033[0m", end='')

                    # if it is a empty line, skip
                    if data.code_str_lines[line] == '' or char_num == 0:
                        self.render_output(f"\r│ {this_line_number}  {spaces} │ \033[32m√\033[0m               ")
                        continue
                    
                    first_non_space_index = len(data.code_str_lines[line]) - len(data.code_str_lines[line].lstrip())

                    output_highlighted_code = first_non_space_index * " "

                    for column in range(first_non_space_index, char_num+first_non_space_index):

                        char_mobject = code_mobject[line][column] # code line character
                        charR, charG, charB = [int(rgb*255) for rgb in char_mobject.get_color().to_rgb()]
                        # use RGB to set output text color
                        output_highlighted_code += f"\033[38;2;{charR};{charG};{charB}m{data.code_str_lines[line][column]}\033[0m"

                        occupy_char = occupy[line][column] # occupy block character
                        self.add(char_mobject) # add code line character
                        cursor.next_to(occupy_char, RIGHT, buff=0.05).set_y(code_line_rectangle.get_y()) # cursor y coordinate in the same line
                        self.wait(random.uniform(*data.interval_range))

                        # output progress
                        code_spaces = (output_char_num_per_line - column - 1)*' '
                        percent = int((column-first_non_space_index+1)/char_num*100)
                        percent_spaces = (3-len(str(percent)))*' '
                        self.render_output(f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ "
                            f"Rendering...\033[33m{percent_spaces}{percent}%\033[0m", end='')
                    
                    # overwrite the previous progress bar
                    code_spaces = (output_char_num_per_line-len(data.code_str_lines[line]))*' '
                    self.render_output(f"\r│ {this_line_number}  {output_highlighted_code}{code_spaces} │ \033[32m√\033[0m               ")

                self.render_output(f"╰{hyphens}╯\n"
                    "Combining to Movie file.")
                self.wait()

            def render(self, output=True):
                start_time = time.time()
                with self._no_manim_output():
                    super().render()
                end_time = time.time()
                total_render_time = end_time - start_time
                self.render_output(f"File ready at \033[32m'{self.renderer.file_writer.movie_file_path}'\033[0m\n"
                    f"\033[30m[Finished rendering in {total_render_time:.2f}s]\033[0m")

        return code_video()

    def render(self, output=True):
        self.output = output
        self.scene.render()
