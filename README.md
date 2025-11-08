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

最新版本：`v1.0.8`

Python版本要求：`>=3.9`

Python依赖库: `manim>=0.17.0`

第三方软件依赖: [<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/FFmpeg.png" width="80" align="center" alt="FFmpeg"/>](https://ffmpeg.org//) [<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/MikTex.png" width="30" align="center" alt="MikTex"/>](https://miktex.org/download)

> [!NOTE]
> 发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。

## 安装

```bash
pip install CodeVideoRenderer
```

> [!IMPORTANT]
> 使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。

## 使用方法

```python
from CodeVideoRenderer import *
video = CameraFollowCursorCV(code_string="print('Hello World!')", language='python')
video.render()
```

### 基本参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `video_name` | `str` | `"CameraFollowCursorCV`" | 生成的视频文件名称，必须提供 |
| `code_string` | `str` | `None` | 要演示的代码字符串，与`code_file`二选一 |
| `code_file` | `str` | `None` | 要读取的代码文件路径，与`code_string`二选一 |
| `language` | `str` | `None` | 代码语言，用于语法高亮显示 |

### 排版与动画参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `line_spacing` | `float` | `DEFAULT_LINE_SPACING`[^1] | 代码行之间的间距，必须大于0 |
| `interval_range` | `tuple[float, float]` | `(DEFAULT_TYPE_INTERVAL, DEFAULT_TYPE_INTERVAL)`[^2] | 字符输入的时间间隔范围，单位为秒，元组中第一个值必须小于等于第二个值 |

### 相机控制参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `camera_floating_max_value` | `float` | `0.1` | 相机浮动效果的最大偏移值，控制相机轻微晃动的幅度 |
| `camera_move_interval` | `float` | `0.1` | 相机自动移动的时间间隔，单位为秒 |
| `camera_move_duration` | `float` | `0.5` | 相机移动到新位置的持续时间，单位为秒，影响移动的平滑度 |
| `camera_scale` | `float` | `0.5` | 相机缩放比例，控制代码在画面中的显示大小 |

### 使用注意事项

> [!WARNING]
> 1. `code_string` 和 `code_file` 必须且只能提供其中一个
> 2. 所有时间相关参数必须大于或等于`SHORTEST_POSSIBLE_DURATION`[^3]
> 3. 相机控制相关参数必须大于或等于`0`
> 4. 代码内容不能为空，且只能包含系统支持的字符

该类通过 `render()` 方法执行视频渲染，并可选择是否在控制台显示输出信息。渲染过程中会展示代码输入的进度条，并在完成后显示渲染时间和文件保存位置。
        
> [!CAUTION]
> 传入的代码中不能含有非ASCII字符。

[^1]: 在`renderer/config.py`中，定义`DEFAULT_LINE_SPACING = 0.8`
[^2]: 在`renderer/config.py`中，定义`DEFAULT_TYPE_INTERVAL = 0.15`
[^3]: 在`renderer/config.py`中，定义`SHORTEST_POSSIBLE_DURATION = 0.0166667`

## 鸣谢
感谢给`CodeVideoRenderer`提出宝贵建议的各位！

<a href="https://www.douyin.com/user/MS4wLjABAAAAuIknm2_gFZa7gxNw2o-FhWlTR-yl4VHPuRxjxJy88p3iin2s9O5t2f7pylFLCZfC">
	<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/douyin_%E6%AC%BE%E5%86%AC.png" width=30 >
</a> <a href="https://www.douyin.com/user/MS4wLjABAAAAPsW8ElarFqE08lFoTd49nQwHfHBr25pz4fXRnHI-xrc3ruPwprfpgyxFcSqHNN5Q">
	<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/douyin_Goway_Hui.png" width=30 >
</a> <a href="mailto:heigirl5201314@vip.qq.com">
	<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/avatars/email_%E7%A0%B4%E7%A2%8E%E5%B0%8F%E8%9D%B4%E8%9D%B6INFP.png" width=30 >
</a>
