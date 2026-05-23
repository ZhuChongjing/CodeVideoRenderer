常见问题和疑难解答
=====================

经常提出的问题和共同问题。

一般问题
-----------------

输出视频保存在哪里？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

调用了 ``render()`` 后，最后的 MP4 将放在Manim内部渲染输出的旁边，使用你通过 ``video_name`` 提供的名字：

.. 代码块：文本

   ./media/videos/1080p60/{video_name}.mp4

确切的子目录 (例如) ``1080p60`` 取决于Manim当前的质量配置。

Cairo vs. OpenGL - 我应该使用哪些？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Cairo** (默认, ``render='cairo'`` ) — — CPU基础, 几乎所有系统都可以工作。
* **OpenGL** (``render='opengl'`` ) — GPU基础可以更快，但需要兼容的图形驱动器。

如果您在 OpenGL 中遇到渲染错误，请切换回开罗：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       代码=('string', 'code'),
       language='python',
       渲染器='cairo'
   )

是否支持中文字符？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

是。 CodeVideoRenderer 捆绑了 ``CodeVideoRenderFont`` 以支持 CJK 字符。 如果您看到已加密文本，请确保您的输入代码是有效的 UTF-8。

常见问题
-------------

找不到FFmpeg
^^^^^^^^^^^^^^^^

如果渲染失败与FFmpeg相关的错误，请在你的 ``PATH`` 中验证FFmpeg：

.. 代码块:: bash

   ffmpeg 版本

If the command is not found, reinstall FFmpeg (see :doc:`installation`) and restart your terminal.

无效字符错误
^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRender拒绝以下字符，因为它们可以破坏Manim的文本布局：

* ``\r`` (transport return)
* ``\v`` (垂直标签)
* ``\f`` (表单种子)

如果你的代码包含这些内容(通常从某些编辑器复制)，在将字符串传递到 ``CameraCursorCV`` 之前，用普通空格或换行符替换它们。

代码被切断或过大
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你的代码阻止可见区域流过多或相机缩放感到错，请调整 ``camera_scale`` ：

.. code-block:: python

   # 放大大文件
   视频 = 摄像机跟随CursorCV(
       code=('file', 'large_script.py'),
       language='python',
       摄像头缩放=0.3
   )

数值小于默认的 ``0.5`` 缩放相机；更大的数值缩放。

如何在渲染时抑制控制台输出？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pass ``output=False`` to :meth:`~.render`:

.. code-block:: python

   渲染(output=False)

此操作仍在生成视频文件时禁用进度条和计时日志。

为什么Manim 缓存不起作用？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CodeVideoRenderer 内部设置 ``config.disable_caching = True`` ，以防止陈旧缓存文件干扰代码打字动画。 这是故意而不是漏洞。

为什么我的代码在垂直上略有不一致？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

某些字符 (``acegmnopqrsuvwxyz+,-.:;<=>_~``)触发了一个已知的 Manim 文本布局对齐错误。 CodeVideoRenderer automatically applies a workaround offset (:data:`~.CODE_OFFSET`) for these characters. 如果你仍然看到问题，请尝试调整 ``camera_scale`` 或在关键位置避免那些字符。

标签是否扩展？ 我可以更改标签大小吗？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes — tabs are always expanded to spaces using a tab size of ``4`` (the :data:`~.DEFAULT_TAB_WIDTH` constant). Currently this value cannot be changed at runtime; if you need a different tab size, preprocess your code string before passing it to :class:`~.CameraFollowCursorCV`.

如果``video_name`` 是空的，怎么办？
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果``video_name`` 为空或falsy，构造函数会提出``ValueError("video_name")`` 。 总是提供一个非空字符串。

渲染缓慢。
^^^^^^^^^^^^^^^^^

* 如果你有兼容的 GPU，请尝试使用 ``render='opengl'`` 。
* 缩短代码长度或将其分割成多个较短的视频。
* 确保您不会在非常缓慢的虚拟机内运行，没有GPU通行。
