<p align=center>
  <img  src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/logo.jpg" width="200" alt="Image Load Failed"/>
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

最新版 Latest version: `v1.0.5.post2`

安装依赖 Install Requires: `manim>=0.17.0`, `pydantic>=2.0`

--- 

> [!NOTE]
> 查看更多信息 For more information：[`Wiki`](https://github.com/ZhuChongjing/CodeVideoRenderer/wiki)
>
> 发现任何问题请发送至[我的邮箱](mailto:zhuchongjing_pypi@163.com)，欢迎大家来找茬，我们会尽快修复。<br/>
If you encounter any issues, please send an email to [my email address](mailto:zhuchongjing_pypi@163.com). We welcome bug feedback, and we will fix them as soon as possible.

本库用于生成输入代码的视频，相机会跟随光标移动。<br/>
This library is used to generate videos of input code, with the camera following the cursor movement.

软件支持 Software Support：[<img src="https://github.com/ZhuChongjing/CodeVideoRenderer/blob/main/README_files/manim.jpg" width="70" align="center" />](https://github.com/manimCommunity/manim)

> [!IMPORTANT]
> 使用`manim`进行动画渲染，使用前请确保`manim`能够正常运行。<br/>
Animation rendering is done with `manim`, please ensure `manim` runs properly before use.

命令行安装 Command Line Installation：
```bash
pip install CodeVideoRenderer
```

**示例 Example**

```python
from CodeVideoRenderer import *
video = CodeVideo(code_string="print('Hello World!')", language='python')
video.render()
```

> [!CAUTION]
> 传入的代码中不能含有非ASCII字符。<br/>The passed code must not contain non-ASCII characters.
