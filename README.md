<p align=center>
  <img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/logo.jpg" width="200" alt="Image Load Failed"/>
</p>

<p align=center>
  <strong>
    一个用于渲染代码视频的Python库
  </strong>
  <br/>
  <strong>
    <i>A Python library for rendering code videos</i>
  </strong>
</p>

<p align="center">
	<a href="https://github.com/ZhuChongjing/CodeVideoRenderer/stargazers">
    <img src="https://img.shields.io/github/stars/ZhuChongjing/CodeVideoRenderer?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/ZhuChongjing/CodeVideoRenderer/network/members">
    <img src="https://img.shields.io/github/forks/ZhuChongjing/CodeVideoRenderer?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/ZhuChongjing/CodeVideoRenderer/watchers">
    <img src="https://img.shields.io/github/watchers/ZhuChongjing/CodeVideoRenderer?style=flat-square&logo=GitHub"></a>
	<a href="https://github.com/ZhuChongjing/CodeVideoRenderer/issues">
    <img src="https://img.shields.io/github/issues/ZhuChongjing/CodeVideoRenderer.svg?style=flat-square&logo=GitHub"></a>
</p>

---

## 基本信息

最新版本：`v1.0.9.post2`

Python版本要求：`>=3.9`

Python依赖库：`manim>=0.17.0`, `rich>=13.0.0`

第三方软件依赖：[<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/FFmpeg.png" width="80" align="center" alt="FFmpeg"/>](https://ffmpeg.org//) [<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/MikTex.png" width="30" align="center" alt="MikTex"/>](https://miktex.org/download)

## 安装

```bash
pip install CodeVideoRenderer
```

> [!TIP]
> 本库使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。

## 示例

### 简单代码

```python
from CodeVideoRenderer import *
video = CameraFollowCursorCV(video_name="Hello World", code_string="print('Hello World!')", language='python')
video.render()
```

总用时4.53秒

https://github.com/user-attachments/assets/f4f016c5-04cf-4669-b6d2-1f0d884fd2a5

## 代码视频对象

```python
class CameraFollowCursorCV(
    video_name: str = "CameraFollowCursorCV",
    code_string: str = None,
    code_file: str = None,
    language: str = None,
    line_spacing: float | int = DEFAULT_LINE_SPACING,
    interval_range: tuple[float | int, float | int] = (DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL),
    camera_scale: float | int = 0.5
)
```

> [!NOTE]
>
> 在`v1.0.7.post2`版本中更名为`CameraFollowCursorCV`，原名`CodeVideo`
>
> 参数`camera_floating_max_value`、`camera_move_interval`、`camera_move_duration`在`v1.0.9`版本中被删除

### 基本参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `video_name` | `str` | `"CameraFollowCursorCV`" | 生成的视频文件名称，必须提供 |
| `code_string` | `str` | `None` | 要演示的代码字符串，与`code_file`二选一 |
| `code_file` | `str` | `None` | 要读取的代码文件路径，与`code_string`二选一 |
| `language` | `str` | `None` | 代码语言，用于语法高亮显示 |

> [!WARNING]
> 
> `code_string`和`code_file`必须且只能提供其中一个
>
> 代码内容不能为空，且只能包含`AVAILABLE_CHARACTERS`[^4]

### 排版与动画参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `line_spacing` | `float` | `DEFAULT_LINE_SPACING`[^1] | 代码行之间的间距，必须大于0 |
| `interval_range` | `tuple[float, float]` | `(DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL)`[^2] | 字符输入的时间间隔范围，单位为秒，元组中第一个值必须小于等于第二个值 |

> [!WARNING]
>
> 所有时间相关参数必须大于或等于$`\frac{1}{当前帧率}`$（取七位小数）

### 相机控制参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `camera_scale` | `float` | `0.5` | 相机缩放比例，控制代码在画面中的显示大小 |

> [!WARNING]
>
> 相机控制相关参数必须大于或等于0

[^1]: 在`renderer/config.py`中，定义`DEFAULT_LINE_SPACING = 0.8`
[^2]: 在`renderer/config.py`中，定义`DEFAULT_TYPE_INTERVAL = 0.15`
[^4]: 在`renderer/config.py`中，定义``AVAILABLE_CHARACTERS = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ \t\n"""``

## 渲染

该类通过 `render()` 方法执行视频渲染，并可选择是否在控制台显示输出信息。渲染过程中会展示代码输入的进度条，并在完成后显示渲染时间和文件保存位置。

```python
def render(output: bool = DEFAULT_OUTPUT_VALUE) -> None
```

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `output` | `bool` | `DEFAULT_OUTPUT_VALUE`[^5] | 渲染时是否输出 |

[^5]: 在`renderer/config.py`中，定义`DEFAULT_OUTPUT_VALUE = True`

## 鸣谢
感谢给`CodeVideoRenderer`提出宝贵建议的各位！

[<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/douyin_%E6%AC%BE%E5%86%AC.png" width=30 >](https://www.douyin.com/user/MS4wLjABAAAAuIknm2_gFZa7gxNw2o-FhWlTR-yl4VHPuRxjxJy88p3iin2s9O5t2f7pylFLCZfC)
[<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/douyin_Goway_Hui.png" width=30 >](https://www.douyin.com/user/MS4wLjABAAAAPsW8ElarFqE08lFoTd49nQwHfHBr25pz4fXRnHI-xrc3ruPwprfpgyxFcSqHNN5Q)
[<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/email_%E7%A0%B4%E7%A2%8E%E5%B0%8F%E8%9D%B4%E8%9D%B6INFP.png" width=30 >](mailto:heigirl5201314@vip.qq.com)

## 联系我们

> [!NOTE]
> 发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。
