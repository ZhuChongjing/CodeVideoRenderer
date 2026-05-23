更新日志
=========

此文档记录了 CodeVideoRenderer 的所有显著变化。

.. seealso::

   * :doc:`installation` for upgrade instructions
   * `GitHub 发布了 <https://github.com/ExploreMaths/CodeVideoRenderer/releases>`_ 以获取详细的更改信息
   * :doc:`contributing` for information on reporting issues

CodeVideoRenderer 1.2.3 :bdg-success-line:`Latest`
------------------------------------------------------------------------

**日期**: 5月4日，2026

详情请访问https://pypi.org/project/codevideoender/1.2.3/。

.. 警告:添加:
   :class: additions

   * 添加 ``moviepy`` 版本需要 ``<2.0.0.0`` 的 Python 3.8

   * 添加了 ``ping-extensions`` 依赖，并且至少需要一个 ``4.0.0`` 的版本

   * 添加了 ``imageio-ffmpeg`` 依赖，并且至少需要一个 ``0.4.0`` 的版本

   * 添加了 ``typeguard`` 依赖，并且至少需要一个 ``3.0`` 的版本

   * Added import of ``annotations`` (from ``__future__``) in ``typing.py`` and ``utils.py`` for compatibility with Python 3.8, 3.9

.. 警告:: 更改
   :class: changes

   * 从 ``0.20.1`` 降级到了 ``manim`` 依赖所需的最小版本 ``0.18.0``

   * 从 ``2.4.2`` 的 ``numpy`` 依赖关系降级到了 ``1.24.4`` 的最小版本

   * 从 ``11.2.1`` 降级到了 ``pillow`` 依赖的最小版本为 ``9.1``

   * 从 ``3.9`` 降级到了 ``3.8`` 的 Python 版本的最小值

   * 修改了 ``TypeAlias`` 、 ``UnionType`` 和 ``VideoFileClip`` 的导入方法，以实现与 Python 3.8、3.9 的兼容性。

   * 将所有类型的注释替换为 ``type | type`` 的格式为 ``Union[typtype]`` ，以实现与 Python 3.8, 3.9 的兼容性。

   * 将所有 ``PathOpinion[str]`` 更改为 ``PathLie`` (因为Python 3.8 的 ``PathLie`` 不支持一般)

   * 将所有类型的注释替换为 ``tuple[...]``、``list[...]`` 和 ``dict[...]`` 格式为 ``Tuple[...]``， ``List[...]`` 和 ``Dict[...]`` 分别用于与 Python 3.8 兼容性

   * Switched the type checker from :func:`typeChecker` to :func:`typeguard.typechecked`

.. 警告:: 删除
   :class: deletions

   * Removed :func:`checkType` and :func:`typeChecker` from ``utils.py``

CodeVideoRenderer 1.2.2
------------------------------------------------------------------------

**日期**: Apr 27, 2026

详情请访问https://pypi.org/project/codevideoender/1.2.2/。

.. 警告:: 更改
   :class: changes

   * 将所有文档(函数、类、常量)转换为restructuredText格式，以便更好地与 Sphinx 文档兼容。

   * Change the default value of the ``formatter_style`` parameter in the :class:`~.CameraFollowCursorCV` class to ``"material"``.

CodeVideoRenderer 1.2.1
----------------------------

**日期**: 马22, 2026

详情请访问https://pypi.org/project/codevideoender/1.2.1/。

.. 警告:添加:
   :class: additions

   * Add the :data:`~.__version__` variable to ``__init__.py``

   * Add the :data:`~.__all__` variable to ``config.py``, ``renderer.py``, ``typing.py``, and ``utils.py``

   * Add the :attr:`~.formatter_style` parameter to the :class:`~.CameraFollowCursorCV` class

   * 为终端错误消息添加美化

   * 为所有函数和类别添加参数说明和类型注释

   * Add the :meth:`~.__getattribute__` function to the :class:`~.CameraFollowCursorCV` class to prevent data modification by changing attributes

   * 添加CodeVideoRendererFont字体以支持中文字符

   * Add the :data:`~.NOT_AVAILABLE_CHARACTERS` variable to ``config.py``

   * Add the :class:`~.Parameters` class to the :class:`~.CameraFollowCursorCV` class for managing and retrieving parameters

   * 添加 ``version.py`` 以管理软件包版本

.. 警告:: 更改
   :class: changes

   * 将函数名称格式从 ``aaa_bbb`` (snake_case) 更改为 ``aaaBbbb`` (camelCase)

   * Change the :data:`~.PygmentsLanguage` class to a ``Literal`` type

   * Refactor the ``default_progress_bar`` function into the :class:`~.DefaultProgressBar` class

   * 将 ``CameraFostCursorCVR.py`` 拆分为 ``render.py`` 、 ``py`` 和 ``utils.py``

   * 修改空格处理逻辑以提高渲染速度

   * Make partial modifications to the parameters and descriptions of the :class:`~.CameraFollowCursorCV` class

   * 修改一些终端输出内容

   * Update the value of :data:`~.CODE_OFFSET` in ``config.py``

.. 警告:: 修复
   :class: fixes

   * 修复`@gaojj2000 <https://github.com/gaojj2000>`_ 在 `#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_ 造成的代码偏移问题

   * 修复当代码偏移发生时发生的 ``code_line_rectangle`` 偏移问题。

.. 警告:: 删除
   :class: deletions

   * Remove the :data:`~.DEFAULT_CODE_FORMATTER_STYLE`, :data:`~.AVAILABLE_CHARACTERS`, and :data:`~.EMPTY_CHARACTER` variables from ``config.py``

CodeVideoRenderer 1.1.2
----------------------------

**日期**: Feb 11, 2026

详情请访问https://pypi.org/project/codevideoender/1.1.2/。

.. 警告:: 修复
   :class: fixes

   * 修复了手指在每一行上清除前面空格造成的光标位置错误(详情见`#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_ )。

CodeVideoRenderer 1.1.1
----------------------------

**日期**: Feb 11, 2026

详情请访问https://pypi.org/project/codevideoender/1.1.1/。

.. 警告:添加:
   :class: additions

   * 添加 ``manim==0.19.1`` 的兼容性更新(详情请参阅`#3 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/3>`_ )。

   * 增加了发光效果。

   * 在切换到 OpenGL 渲染时适应OpenGL 渲染和解决相关问题(见`#4 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/4>`_ )。

   * Added the ``renderer`` parameter to :class:`~.CameraFollowCursorCV` to configure the renderer.

.. 警告:: 更改
   :class: changes

   * Modified :func:`~.type_checker` to adapt to ``Literal`` and :data:`~.PygmentsLanguage`.

   * 优化终端显示。

   * 将 ``functions.py`` 集成到 ``CameraFollasCursorCVR.py`` 中。

   * 通过 ``timeit`` 模块来计算渲染时间并消除多余变量。

   * Changed the type of the ``language`` parameter in :class:`~.CameraFollowCursorCV` from ``str`` to :data:`~.PygmentsLanguage`.

   * 恢复了文件结构。

.. 警告:: 删除
   :class: deletions

   * 在渲染``Scene`` 之前删除了摘要输出。

   * 删除了 ``config.py`` 中未使用的常数。

CodeVideoRenderer 1.1.0
----------------------------

**日期**：2025年12月25日。

详情请访问https://pypi.org/project/codevideoender/1.1.0/。

.. 警告:添加:
   :class: additions

   * 添加了打开动画。

.. 警告:: 更改
   :class: changes

   * 经修订的相机移动逻辑。

.. 警告:: 修复
   :class: fixes

   * Fixed the issue where output could not be terminated when ``output=False`` was used in :meth:`~.render`.

CodeVideoRenderer 1.0.9.post2
------------------------------

**日期**: 2025

详细信息见 https://pypi.org/project/codevideoender/1.0.9.post2/。

.. 警告:: 更改
   :class: changes

   * 调整了光标和字符之间的间距。

CodeVideoRenderer 1.0.9.post1
------------------------------

**日期**: 2025

详情请访问https://pypi.org/project/codevideoender/1.0.9.post1/。

.. 警告:: 更改
   :class: changes

   * Redesigned progress bar style and added a ``{task.completed}/{task.total}`` field.

.. 警告:: 修复
   :class: fixes

   * Fixed partial issues with the :func:`~.type_checker` decorator.

CodeVideoRenderer 1.0.9
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.9/。

.. 警告:: 更改
   :class: changes

   * 校正和重写相机移动逻辑，并添加自动相机缩放。

   * 使用 ``rich`` 来在渲染开始时打印初始数据。

   * 使用 ``rich.progress`` 重写渲染进度栏。

   * 恢复的类型检查和使用 ``rich.traceback`` 进行更清洁的错误输出。

CodeVideoRenderer 1.0.8.post1
--------------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.8.post1/。

.. 警告:: 修复
   :class: fixes

   * Fixed issues in ``__init__.py``.

CodeVideoRenderer 1.0.8
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.8/。

.. 警告:: 更改
   :class: changes

   * 将默认字体还原到 Consolas，因为Cascadia 代码将 ``>=`` 转换为 ``0`` ，并触发了内部Manim错误。

.. 警告:: 修复
   :class: fixes

   * 固定代码偏移错误。

.. 警告:: 删除
   :class: deletions

   * 移除了 ``/render/config.py`` 中未使用的常数。

CodeVideoRenderer 1.0.7.post3
--------------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.7.post3/。

.. 警告:: 修复
   :class: fixes

   * 由于在管道上上传软件包不完整，重新上传完整的源代码。

CodeVideoRenderer 1.0.7.post2
---------------------------------

**日期**：2025

详细信息见 https://pypi.org/project/codevideoender/1.0.7.post2/。

.. 警告:: 更改
   :class: changes

   * 禁用Manim 缓存以提高渲染速度。

.. 警告:: 修复
   :class: fixes

   * 修复了代码内容开头的空白行触发的渲染错误。

CodeVideoRenderer 1.0.7.post1
--------------------------------

**日期**: 2025

详情请访问https://pypi.org/project/codevideoender/1.0.7.post1/。

.. 警告:: 修复
   :class: fixes

   * 使用 ``code_file`` 参数解决了 bug。

CodeVideoRenderer 1.0.7
----------------------------

**日期**: 2025

详情请访问https://pypi.org/project/codevideoender/1.0.7/。

.. 警告:: 更改
   :class: changes

   * 更新了 Pip 依赖者配置。

   * 参数``camera_floating_max_value`` 更改为 ``camera_floating_max_value`` ，``screen_scale`` 更改为 ``camera_scale`` 。

   * 改进了错误消息的演示。

CodeVideoRenderer 1.0.6
----------------------------

**日期**：27，2025

详情请访问https://pypi.org/project/codevideoender/1.0.6/。

.. 警告:: 更改
   :class: changes

   * 恢复了渲染器模块：优化了CodeVideoRenderer的结构和错误处理(详情见`#1 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/1>`_ )。

.. 警告:: 修复
   :class: fixes

   * 修复了由于代码行过长造成的进度条格式化错误。

CodeVideoRenderer 1.0.5.post2
---------------------------------

**日期**：25，2025

详细信息见 https://pypi.org/project/codevideoender/1.0.5.post2/。

.. 警告:: 修复
   :class: fixes

   * Pip 依赖关系的固定版本兼容性问题，以确保完全符合项目要求。

   * 解决了在不同终端/编译器渲染输出时ANSI的颜色显示不一致的顺序。

CodeVideoRenderer 1.0.5.post1
-------------------------------

**日期**：23，2025

详情请访问https://pypi.org/project/codevideoender/1.0.5.post1/。

.. 警告:: 修复
   :class: fixes

   * 修复pip安装失败。

CodeVideoRenderer 1.0.5
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.5/。

.. 警告:添加:
   :class: additions

   * Added the new ``output`` parameter to the :meth:`~.render` method to control rendering output behavior.

.. 警告:: 更改
   :class: changes

   * 从一个函数恢复到一个类的 ``CodeVideo`` 以更好的代码维护和可扩展性。

CodeVideoRenderer 1.0.4
----------------------------

**日期**：第6相，2025

详情请访问https://pypi.org/project/codevideoender/1.0.4/。

.. 警告:: 更改
   :class: changes

   * 优化终端渲染日志。

   * 提高了执行代码的整体效率。

.. 警告:: 修复
   :class: fixes

   * 修复渲染持续时间的计算错误。

.. 警告:: 删除
   :class: deletions

   * 删除了已废弃的 ``font`` 参数。

CodeVideoRenderer 1.0.3
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.3/。

.. 警告:添加:
   :class: additions

   * 添加了新的 ``line_spating`` 参数来自定义行间距。

.. 警告:: 更改
   :class: changes

   * 从动画回放中排除每条代码行的前导和尾随空白，以减少多余动画持续时间。

   * 调整了当前突出显示的代码行的背景宽度。

   * 优化终端渲染信息输出。

   * 微调相机移动逻辑。

.. 警告:: 修复
   :class: fixes

   * 修复了光标未能在新线开始时暂停的问题。

CodeVideoRenderer 1.0.2
----------------------------

**日期**: 2025

详情请访问https://pypi.org/project/codevideoender/1.0.2/。

.. 警告:添加:
   :class: additions

   * 引入了 Pydtatic ``@validate_call`` 用于参数验证。
   * 添加了显式参数： ``code_string`` 、 ``code_file`` 、 ``font`` 、 ``language`` 、 ``interval_range`` 、 ``camera_floating_maximum_value`` 、 ``camera_move_interval`` 、 ``camera_move_duration`` 和 ``screen_scale`` 。
   * Added rendering time tracking using :func:`time.time`.
   * 在终端输出中添加了语法高亮的实时代码预览，带有框边框和完成标记。
   * Added :meth:`~.replace_empty_chars` to validate non-empty code input.

.. 警告:: 更改
   :class: changes

   * 使用 ``**kwargs`` 替换为明确的输入参数。
   * Replaced :meth:`~.has_chinese` check with :meth:`str.isascii` for non-ASCII character detection.
   * 将默认的 ``formter_style`` 设置为 ``"material"`` 。
   * 改进占用区宽度计算。
   * 带有ANSI颜色和进度边界的超导终端渲染日志。

.. 警告:: 删除
   :class: deletions

   * 移除了 ``speed`` 参数(已在 1.0.1.0中移除)。
   * 移除 ``has_e`` 方法。

CodeVideoRenderer 1.0.1.2
----------------------------

**日期**: 23, 2025

详情请访问https://pypi.org/project/codevideoender/1.0.1.2/。

.. 警告:添加:
   :class: additions

   * Added the :class:`~.LoopMovingCamera` class for continuous smooth camera tracking without infinite loops.

.. 警告:: 更改
   :class: changes

   * 默认的 ``interval`` 从 ``0.05`` 更改为 ``0.3`` 。
   * 使用 ``self.render.file_writer.movie_file_path`` 检索成功的输出路径。
   * 空行和字符间隔现在使用 ``random.unique(interval-0.05, interval+0.05)`` 。

.. 警告:: 删除
   :class: deletions

   * Removed :meth:`~.move_camera_to_cursor` method (replaced by :class:`~.LoopMovingCamera`).
   * Removed the ASCII table docstring from :meth:`~.construct`.

CodeVideoRenderer 1.0.1.1
----------------------------

**日期**: 22, 2025

详情请访问https://pypi.org/project/codevideoender/1.0.1.1/。

.. 警告:添加:
   :class: additions

   * 添加了新的 ``scale`` 参数来控制相机帧缩放。
   * Added :meth:`set_z_index` to cursor and code mobjects for proper layering.

.. 警告:: 更改
   :class: changes

   * 光标宽度从 ``0.005`` 降低到 ``0.0005`` 。
   * 默认行号颜色改为 ``GREY`` ；当前行号在 ``WHITE`` 中高亮。
   * 将 ``code_line_rectangle`` 样式更改为填充背景颜色 ``#333333`` 。
   * 使用绿色ANSI颜色改进的终端成功消息。

.. 警告:: 删除
   :class: deletions

   * 已从场景中移除代码窗口 (``window`` )。

CodeVideoRenderer 1.0.1.0
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.1.0/。

.. 警告:添加:
   :class: additions

   * 增加最低验证间隔，以防止间隔过短。
   * 添加 ``code_line_rectangle`` 以突出当前代码行。
   * 添加了左右浮动到相机移动。

.. 警告:: 更改
   :class: changes

   * 移除了 ``speed`` 参数；相机移动现在使用了固定的 ``0.2`` 第二次运行时间。
   * 使用 ANSI 颜色改进终端输出、总行数显示和改进进度条格式。
   * 中文译成英文的评论和文件。
   * Merged :meth:`~.successfully_rendered_info` logic into the :meth:`~.render` method.

CodeVideoRenderer 1.0.0.5
----------------------------

**日期**：2025

详细信息见 https://pypi.org/project/codevideoender/1.0.0.5/。

.. 警告:添加:
   :class: additions

   * Added :meth:`~.has_chinese` method to detect Chinese characters and punctuation.
   * 将 ``code_file`` 参数添加到从文件中读取代码。
   * 添加了自动标签到空格转换(4个空格)。
   * 添加了对空代码行的处理。
   * 在动画播放过程中添加了跳过前面空格。
   * Added extensive inline comments and an ASCII table docstring in :meth:`~.construct`.

.. 警告:: 更改
   :class: changes

   * 将参数``floating_pos`` 重命名为 ``floating_camera`` 。
   * 调整后的光标尺寸（缩短和缩短）。
   * 初始相机缩放从 ``0.25`` 更改为 ``0.3`` 。
   * Moved :meth:`~.move_camera_to_cursor` definition earlier in the class.

CodeVideoRenderer 1.0.0.4
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.0.4/。

.. 警告:: 删除
   :class: deletions

   * 已删除 ``main.py`` ，只保留一个 ``render.py`` 作为单个切入点。

CodeVideoRenderer 1.0.0.3
----------------------------

**日期**: 16, 2025

详情请访问https://pypi.org/project/codevideoender/1.0.0.3/。

   重新上传软件包，但没有代码更改。

CodeVideoRenderer 1.0.0.2
----------------------------

**日期**: 16, 2025

详情请访问https://pypi.org/project/codevideoender/1.0.0.2/。

   重新上传软件包，但没有代码更改。

CodeVideoRenderer 1.0.0.1
----------------------------

**日期**: 16, 2025

详细信息见 https://pypi.org/project/codevideoender/1.0.0.1/。

.. 警告:添加:
   :class: additions

   * 添加 ``render.py`` (一个 ``main.py`` 的副本) 作为主渲染模块。

.. 警告:: 更改
   :class: changes

   * Changed ``__init__.py`` to import from ``renderer`` instead of ``main``.

CodeVideoRenderer 1.0.0.0
----------------------------

**日期**：2025

详情请访问https://pypi.org/project/codevideoender/1.0.0.0/。

   最初发布的 CodeVideoRendererer
