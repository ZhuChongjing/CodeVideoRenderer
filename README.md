**CodeVideoRenderer 1.0.3**

- [项目介绍](#项目介绍)
- [Project Description](#project-description)

# 项目介绍
发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。

**修复**
- 代码偏移（`manim`自带bug）
- 换行时相机不及时移动
- 光标在换行时不在开头停顿

**更新**
- 每行代码首尾空白字符不参与动画，以免增加动画时长
- 当前行背景宽度更改
- 新增`line_spacing`参数用于更改行距

**优化**
- 终端渲染信息
- 相机移动

**旧版本支持功能**
- 光标打字
- 相机持续移动
- 参数及代码检测

--- 

本库用于生成输入代码的视频，视频视角会跟随光标移动。（视频生成时间可能略长，请耐心等待）

**提示：使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。**

本库提供`CodeVideo`，您可以用它来创建一个视频对象。参数如下：

```python
(function) def CodeVideo(
    video_name: str = "CodeVideo",
    code_string: str = None,
    code_file: str = None,
    font: str = 'Consolas',
    language: str = None,
    line_spacing: float = 0.7,
    interval_range: tuple[float, float] = (0.2, 0.2),
    camera_floating_maximum_value: float = 0.1,
    camera_move_interval: float = 0.1,
    camera_move_duration: float = 0.5,
    screen_scale: float = 0.5
) -> code_video
```

**参数说明**
- `video_name`：生成视频的文件名，默认值为`"CodeVideo"`
- `code_string`：直接传入的代码字符串
- `code_file`：代码文件路径
- `font`：代码显示字体，默认值为`'Consolas'`
- `language`：代码语言（用于语法高亮）
- `line_spacing`：代码行间距，默认值为`0.7`
- `interval_range`：字符显示的时间间隔范围（秒），元组形式，默认`(0.2, 0.2)`，最小值为0.2
- `camera_floating_maximum_value`：相机浮动的最大范围，默认`0.1`，值≥0
- `camera_move_interval`：相机自动移动的时间间隔（秒），默认`0.1`，值≥0
- `camera_move_duration`：相机移动的持续时间（秒），默认`0.5`，值≥0
- `screen_scale`：屏幕缩放比例，默认值为`0.5`

**注：所有带范围限制的参数均不能小于指定最小值，`code_string`与`code_file`不能同时传入。**

--- 

本库使用`pydantic`中的`validate_call`，在你传入参数时会自动检查参数类型，以确保其正确性。

你可以使用`CodeVideo`对象的`render`方法来生成视频，你可以在终端中查看视频的保存位置。

**示例**
```python
from CodeVideoRenderer import *
video = CodeVideo(code_string="print('Hello World!')", language='python')
video.render()
```

# Project Description
If you find any issues, please send an email to [my email address](mailto:zhuchongjing_pypi@163.com). We welcome you to point out problems, and we will fix them as soon as possible.

**Fixes**
- Code offset (a built-in bug of `manim`)
- Camera not moving promptly when wrapping lines
- Cursor not pausing at the start when wrapping lines

**Updates**
- Leading and trailing whitespace characters of each code line are excluded from the animation to avoid increasing the animation duration
- Adjusted the background width of the current line
- Added the `line_spacing` parameter for adjusting line spacing

**Optimizations**
- Terminal rendering information
- Camera movement

**Features Supported by Older Versions**
- Cursor typing effect
- Continuous camera movement
- Parameter and code detection

---

This library is used to generate videos of input code, and the video perspective will follow the movement of the cursor. (The video generation process may take a little longer, please wait patiently.)

**Note: Animation rendering is done using `manim`. Please ensure that `manim` can run properly before use.**

The library provides `CodeVideo`, which you can use to create a video object. The parameters are as follows:

```python
(function) def CodeVideo(
    video_name: str = "CodeVideo",
    code_string: str = None,
    code_file: str = None,
    font: str = 'Consolas',
    language: str = None,
    line_spacing: float = 0.7,
    interval_range: tuple[float, float] = (0.2, 0.2),
    camera_floating_maximum_value: float = 0.1,
    camera_move_interval: float = 0.1,
    camera_move_duration: float = 0.5,
    screen_scale: float = 0.5
) -> code_video
```

**Parameter Description**
- `video_name`: The filename of the generated video, with a default value of `"CodeVideo"`
- `code_string`: The code string passed in directly
- `code_file`: The path to the code file
- `font`: The font used for displaying code, with a default value of `'Consolas'`
- `language`: The code language (used for syntax highlighting)
- `line_spacing`: The line spacing of the code, with a default value of `0.7`
- `interval_range`: The time interval range (in seconds) for character display, in tuple format, default is `(0.2, 0.2)`, with a minimum value of 0.2
- `camera_floating_maximum_value`: The maximum range of camera floating, default is `0.1`, value ≥ 0
- `camera_move_interval`: The time interval (in seconds) for automatic camera movement, default is `0.1`, value ≥ 0
- `camera_move_duration`: The duration (in seconds) of camera movement, default is `0.5`, value ≥ 0
- `screen_scale`: The screen scaling ratio, with a default value of `0.5`

**Note: All parameters with range restrictions cannot be less than the specified minimum value, and `code_string` and `code_file` cannot be passed in at the same time.**

---

This library uses `validate_call` from `pydantic`, which automatically checks the parameter types when you pass them in to ensure their correctness.

You can use the `render` method of the `CodeVideo` object to generate the video, and you can check the video's save location in the terminal.

**Example**
```python
from CodeVideoRenderer import *
video = CodeVideo(code_string="print('Hello World!')", language='python')
video.render()
```
