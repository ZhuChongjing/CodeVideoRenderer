# CodeVideoRenderer 1.0.3

> [!NOTE]
> 发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。

命令行安装：
```bash
pip install CodeVideoRenderer
```

## 本次更新内容

### 修复
- 代码偏移（`manim`自带bug）
- 换行时相机不及时移动
- 光标在换行时不在开头停顿

### 更新
- 每行代码首尾空白字符不参与动画，以免增加动画时长
- 当前行背景宽度更改
- 新增`line_spacing`参数用于更改行距

### 优化
- 终端渲染信息
- 相机移动

## 如何使用

> [!IMPORTANT]
> 使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。

本库用于生成输入代码的视频，视频视角会跟随光标移动。

视频生成时间可能略长，请耐心等待

### 创建视频对象

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

#### 参数说明

> [!NOTE]
> 本库使用`pydantic`中的`validate_call`，在你传入参数时会自动检查参数类型，以确保其正确性。
    
- `video_name`：生成视频的文件名，默认值为`"CodeVideo"`
- `code_string`：直接传入的代码字符串
- `code_file`：代码文件路径
- `font`：代码显示字体，默认值为`'Consolas'`
- `language`：代码语言（用于语法高亮）
- `line_spacing`：代码行间距，默认值为`0.7`
- `interval_range`：字符显示的时间间隔范围（秒），元组形式，默认`(0.2, 0.2)`，最小值为$`0.2`$
- `camera_floating_maximum_value`：相机浮动的最大范围，默认`0.1`，值$`\geqslant 0`$
- `camera_move_interval`：相机自动移动的时间间隔（秒），默认`0.1`，值$`\geqslant 0`$
- `camera_move_duration`：相机移动的持续时间（秒），默认`0.5`，值$`\geqslant 0`$
- `screen_scale`：屏幕缩放比例，默认值为`0.5`

> [!CAUTION]
> 所有带范围限制的参数均不能小于指定最小值，`code_string`与`code_file`不能同时传入。 

### 生成视频
你可以使用`CodeVideo`对象的`render`方法来生成视频，你可以在终端中查看视频的保存位置。

#### 示例
```python
from CodeVideoRenderer import *
video = CodeVideo(code_string="print('Hello World!')", language='python')
video.render()
```
