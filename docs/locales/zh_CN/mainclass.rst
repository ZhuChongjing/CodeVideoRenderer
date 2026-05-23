摄像机跟随CursorCV
====================

``CameraFindCursorCV`` 是创建代码打字动画视频的主要类。 它处理代码解析、语法高亮、相机移动和完整渲染管道。

简单的例子
-------------

.. code-block:: python

   从 CodeVideoRenderer 导入摄像机跟随CursorCV

   视频 = 摄像机跟随CursorCV(
       code=('string', 'print("Hello, World!"),
       language='python',
       video_name='HelloWorld'
   )
   video.render()

构造参数
----------------------

下表概括了构造函数所接受的参数。 完整签名，见下面API参考。

.. 列表表：
   :header-rows: 1
   :widths: 20 15 65

   * - 参数
     - 默认
     - 描述
   * - ``code``
     - *必填*
     - 管道``('string', code_str)`` 或 ``('file', file_path)`` 。
   * - ``language``
     - *必填*
     - 语法高亮的编程语言(例如) ``'python'``, ``'javascript'``).
   * - ``格式化样式``
     - ``"material"``
     - Pygments 样式名称 (例如) ``"github-dark"``, ``"monokai"``).
   * - ``line_spacing``
     - ``0.8``
     - 代码行之间的垂直间距。
   * - ``interval_range``
     - ``(0.15, 0.15)``
     - 输入字符之间的最小/最大秒数。
   * - ``camera_scale``
     - ``0.5``
     - 初始相机缩放级别。
   * - ``video_name``
     - ``CameraFindCursorCV``
     - 输出MP4文件的基本名称 (无扩展名)。
   * - ``render``
     - ``"cairo"``
     - 渲染后端: ``cairo"`` (CPU) 或 ``opengl"`` (GPU)。

产出
------

After calling :meth:`~.render`, the final video is saved as an MP4 file. 默认位置遵循Manim的输出协议：

.. 代码块：文本

   ./media/videos/1080p60/{video_name}.mp4

确切的子目录 (例如) ``1080p60`` 取决于Manim的质量配置。 文件名由你传递给构造函数的 ``video_name`` 参数确定。

完整的 API 参考
------------------

.. 自动类：CodeVideoRenderer.render.CameraFollensorCV
    :members:
    :undoc-members:
    :private-members:
    :special-members: __getattribute__
