# CodeVideoRenderer 1.0.3

软件支持 Software Support：[$`\text{Manim}`$
](https://www.manim.community)

> [!IMPORTANT]
> 使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。<br/>
Animation rendering is done with `manim`, please ensure `manim` runs properly before use.

命令行安装：<br/>
Command Line Installation：
```bash
pip install CodeVideoRenderer
```

发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。<br/>
If you encounter any issues, please send an email to [my email address](mailto:zhuchongjing_pypi@163.com). We welcome bug feedback, and we will fix them as soon as possible.

<details>
    <summary>本次更新内容<br/>Update Content for This Version</summary>

<br/>

> **修复 Fixes**
> - 代码偏移（`manim`自带bug）<br/>
>   Code offset (built-in `manim` bug)
> - 换行时相机不及时移动<br/>
>   Camera not moving promptly during line breaks
> - 光标在换行时不在开头停顿<br/>
>   Cursor not pausing at the start when wrapping to a new line
> 
> **更新 Updates**
> - 每行代码首尾空白字符不参与动画，以免增加动画时长<br/>
>   Leading and trailing whitespace in each code line do not participate in the animation to avoid increasing the animation duration
> - 当前行背景宽度更改<br/>
>   Adjustment of the background width for the current line
> - 新增`line_spacing`参数用于更改行距<br/>
>   Added the new `line_spacing` parameter to adjust line spacing
> 
> **优化 Optimizations**
> - 终端渲染信息<br/>
>   Terminal rendering information
> - 相机移动<br/>
>   Camera movement
</details>

## 如何使用<br/>How to Use

本库用于生成输入代码的视频，相机会跟随光标移动。<br/>
This library is used to generate videos of input code, with the camera following the cursor movement.

> [!Tip]
> 视频生成时间可能略长，请耐心等待。<br/>Video generation may take a little time, please be patient.

### 创建视频对象<br/>Creating a Video Object

本库提供`CodeVideo`，您可以用它来创建一个视频对象。参数如下：<br/>
This library provides `CodeVideo`, which you can use to create a video object. The parameters are as follows:

```python
CodeVideo(
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
)
```

本库使用`pydantic`中的`validate_call`，在您传入参数时会自动检查参数类型，以确保其正确性。<br/>
This library uses `validate_call` from `pydantic`, which automatically checks parameter types when you pass them in to ensure correctness.
    
| 参数名<br/>Parameter Name | 说明<br/>Description | 默认值<br/>Default Value |
| ---- | ---- | ---- |
| `video_name` | 生成视频的文件。<br/>Name of the generated video file. | `"CodeVideo"` |
| `code_string` | 直接传入的代码字符串。<br/>Directly passed code string. | - |
| `code_file` | 代码文件路径。<br/>Path to the code file. | - |
| `font` | 代码显示字体。<br/>Font for code display. | `'Consolas'` |
| `language` | 代码语言（用于语法高亮）。<br/>Code language (for syntax highlighting). | - |
| `line_spacing` | 代码行间距。<br/>Line spacing of the code. | `0.7` |
| `interval_range` | 字符显示的时间间隔范围（秒），元组形式，最小值为$`0.2`$。<br/>Time interval range (in seconds) for character display, in tuple form; minimum value is $`0.2`$. | `(0.2, 0.2)` |
| `camera_floating_maximum_value` | 相机浮动的最大范围，值$`\geqslant 0`$。<br/>Maximum range of camera floating; value $`\geqslant 0`$. | `0.1` |
| `camera_move_interval` | 相机自动移动的时间间隔（秒），值$`\geqslant 0`$。<br/>Time interval (in seconds) for automatic camera movement, value $`\geqslant 0`$. | `0.1` |
| `camera_move_duration` | 相机移动的持续时间（秒），值$`\geqslant 0`$。<br/>Duration (in seconds) of camera movement, value $`\geqslant 0`$. | `0.5` |
| `screen_scale` | 屏幕缩放比例。<br/>Screen scaling ratio. | `0.5` |

> [!CAUTION]
> 所有带范围限制的参数均不能小于指定最小值，`code_string`与`code_file`不能同时传入。<br/>
All parameters with range restrictions cannot be less than the specified minimum value, and `code_string` and `code_file` cannot be passed in at the same time.

### 生成视频<br/>Generating a Video

你可以使用`CodeVideo`对象的`render`方法来生成视频，并在终端中查看视频的保存位置。<br/>
You can use the `render` method of the `CodeVideo` object to generate a video, and check the video's save location in the terminal.

> [!TIP]
> 示例 Example
> ```python
> from CodeVideoRenderer import *
> video = CodeVideo(code_string="print('Hello World!')", language='python')
> video.render()
> ```
