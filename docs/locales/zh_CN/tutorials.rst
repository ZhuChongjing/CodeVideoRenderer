教程和指南
==================

本节包含使用CodeVideoRenderer的逐步教程和全面指南。

正在开始
---------------

快速启动指南
^^^^^^^^^^^^^^^^^

创建您的第一个代码动画视频：

.. code-block:: python

    从 CodeVideoRenderer 导入摄像机跟随CursorCV

    代码 = ''
    def hello_world()：
        打印("你好，世界！")
        返回 True
    '''

    # 创建简单的代码动画
    视频 = 摄像机跟随CursorCV(
        代码=('string', 代码),
        language='python',
        formatter_style='github-dark'
    )

    video.render()

基本概念
--------------

了解CodeVideoRenderer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer 工作方式：

1. **解析代码**: 读取并处理你的代码
2. **语法高亮**：应用特定语言的着色
3. **动画**：按字符创建打字动画
4. **相机移动** ：平滑地跟随光标

核心组件
^^^^^^^^^^^^^^^

* **相机跟随CursorCV**: 用于创建动画的主类
* **代码输入**：支持字符串和文件
* **渲染器类型**：开罗(软件)和OpenGL (硬件加速)

中间教程
----------------------

自定义动画速度
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

控制输入速度和间隔范围：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       代码=('string', 'your_code_here'),
       language='python',
       间隔范围=(0.05, 0.1), # 快速输入
       # interval_range=(0.2, 0.5), # 慢慢, 故意输入
   )

使用文件
^^^^^^^^^^^^^^^^^^

从现有文件产生动画代码：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       代码=('file', 'path/to/your/script.py'),
       language='python',
       video_name='MyScriptAnimation'
   )

高级教程
------------------

自定义样式
^^^^^^^^^^^^^^

使用不同的语法高亮风格：

.. code-block:: python

   # 可用样式：github-dar、monokai、solized-dark等。
   视频 = 摄像机跟随CursorCV(
       代码=('string', 'code'),
       language='python',
       格式化样式='monokai'
   )

相机配置
^^^^^^^^^^^^^^^^^^^^

根据不同的代码大小调整相机行为：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       代码=('string', 'large-code_block'),
       language='python',
       摄像头缩放=0.3，# 放大大文件
       线性间距=1.2 # 增加可读性间距
   )

最佳做法
--------------

代码准备
^^^^^^^^^^^^^^^^

* **清理代码**：删除不必要的评论和空格
* **一致格式** ：使用一致缩进
* **合理长度**：将代码块保留在100行下以进行最佳查看

切换到 OpenGL
^^^^^^^^^^^^^^^^^^^

默认情况下，CodeVideoRenderer 使用开罗(CPU)后端。 如果您有兼容的 GPU，您可以切换到 OpenGL 以便更快地渲染：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       代码=('string', 'your_code_here'),
       language='python',
       渲染器='opengl' # 使用GPU加速
   )
   video.render()

.. 注：

   OpenGL 支持依赖您的图形驱动程序和操作系统。 如果与 OpenGL 渲染失败，请回到``render='cairo'`` (默认)。

控制控制台输出
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default :meth:`~.render` prints progress bars and timing logs. 静默运行：

.. code-block:: python

   渲染(output=False)

这对于在 CI/CD 管道或批处理脚本中渲染以尽量减少控制台噪音是有用的。

性能优化
^^^^^^^^^^^^^^^^^^^^^^^^

* * **使用 OpenGL**：为了更快地渲染支持的系统 (见上文实例)
* **批处理**：按顺序渲染多个视频
* **分辨率**：为您的需要选择适当的分辨率。

故障排除常见问题
------------------------------

See the :doc:`faq` section for solutions to common problems (FFmpeg errors, invalid characters, slow rendering, etc.).
