.. CodeVideoRenderer 文档主文件创建于
   Sphinx-quickstart on Mon Apr 20 19:33:36 2026。
   您可以完全根据您的喜好修改这个文件，但它至少应该是
   包含根目录`toctree`指令。

CodeVideoRenderer
=================

**CodeVideoRender** 是基于 Manim 的 Python 动画库，专门用于创建动态代码演示视频。 它将静态代码变成生动的动画，模拟真正的编程过程。

核心概念
-------------

代码动画
^^^^^^^^^^^^^^

CodeVideoRenderer的核心功能是根据字符和行来动画代码。 与传统的静态代码显示不同，它可以：

* **模拟输入过程**：按角色显示代码字符，模拟实际编程体验
* **智能光标跟踪**：相机自动跟随光标移动，确保当前编辑的代码保持在视图中心
* **语法高亮支持**：Integrates Pygments 语法高亮引擎，支持多个编程语言

相机系统
^^^^^^^^^^^^^

图书馆包括一个智能相机系统，能够：

* **自动缩放**：根据代码内容自动调整相机缩放
* **平滑移动**：相机顺畅地跟随光标移动，避免突然跳转
* **焦点管理**：智能识别代码结构以确保重要部件保持可见

关键功能
------------

* **🎬 专业动画效果**: 基于 Manim 引擎, 提供高质量动画渲染。
* **📝 Multi-language support **: 语法高亮显示包括Python、JavaScript、Java 和更多
* **⚙️ 高度自定义**: 可调整的输入速度, 行间距, 相机行为, 及其他参数
* **🎨 Rich styling**: 多重代码高亮风格(例如github-dark, monokai等)
* **🔧 双渲染器**: 支持开罗和OpenGL 渲染后端

使用案例
---------

CodeVideoRenderer 特别适合以下应用场景：

* **教育示威**：为编程课程创建代码解释视频
* **技术介绍**：为会议会谈制作代码演示部分
* **算法可视化**：动态展示算法实现过程和逻辑。
* **代码审查**：可视化代码修改和重新排列过程

设计哲学
-----------------

CodeVideoRender的设计哲学是“让代码活着”，旨在通过动画更好地传达编程理念和代码逻辑。 它不仅仅是一个代码呈现工具，而且是一个代码讲故事工具。

索引
-----

.. testree::
   :maxdepth: 2
   :caption: Documentation

   示例：
   安装
   教程
   参考
   常见问题
   迁移
   更新日志
   贡献
   行为代码

.. testree::
   :maxdepth: 1
   :caption: External Links
   
   GitHub Repository <https://github.com/ExploreMaths/CodeVideoRenderer>
   PyPI 包 <https://pypi.org/project/codevideorenderer/>