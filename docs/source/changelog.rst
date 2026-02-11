更新日志
===========

这里记录了每个版本的新增功能、改进和修复的问题。

``v1.1.2``
----------

处理 ``manim`` 会统一去掉每行前面都有的空格 导致的光标位置错误的问题（详见 `#5 <https://github.com/ZhuChongjing/CodeVideoRenderer/pull/5>`_）

``v1.1.1``
----------

兼容 ``manim==0.19.1`` 的更新（详见 `#3 <https://github.com/ZhuChongjing/CodeVideoRenderer/pull/3>`_）

对 :func:`~.type_checker` 进行修改，适配 ``Literal`` 及 :class:`~.PygmentsLanguage`

优化终端显示

增加发光效果

将 ``functions.py`` 整合到 ``CameraFollowCursorCVR.py`` 中

适配OpenGL渲染，处理了切换OpenGL渲染时的相关问题（详见 `#4 <https://github.com/ZhuChongjing/CodeVideoRenderer/pull/4>`_）

在 :class:`~.CameraFollowCursorCV` 中增加 ``renderer`` 参数，用于设置渲染器

使用 ``timeit`` 模块计算渲染时间，避免冗余变量

删除渲染 ``Scene`` 前的汇总输出

删除 ``config.py`` 中的无用常量

将 :class:`~.CameraFollowCursorCV` 中 ``language`` 参数的类型从 ``str`` 改为 :class:`~.PygmentsLanguage`

修改文件组织架构

``v1.1.0``
----------

修改相机运动逻辑

增加开头动画

修复在 :meth:`~.render` 中使用 ``output=False`` 时无法终止输出的问题

``v1.0.9.post2``
----------------

更改光标与字符的间距

``v1.0.9.post1``
----------------

修复 :func:`~.type_checker` 装饰器的部分问题

更改进度条样式，增加 ``{task.completed}/{task.total}`` 一栏

``v1.0.9``
----------

修改相机运动逻辑，重写相机移动逻辑，增加相机自动缩放功能

使用 ``rich`` 输出渲染开始时的数据

重写渲染进度条，现使用 ``rich.progress`` 进行进度条输出

重写类型检查，使用 ``rich.traceback`` 抛出更美观的错误

``v1.0.8.post1``
----------------

修复 ``__init__.py`` 的问题

``v1.0.8``
----------

修复代码偏移问题

由于 Cascadia Code 会将 ``>=`` 变成 ``≥`` 导致 :math:`\mathbb{M}\text{anim}` 内部错误，因此将字体换回 Consolas

删除 ``/renderer/config.py`` 中的无用常量

``v1.0.7.post3``
----------------

``pip`` 未上传完整代码，重新上传

``v1.0.7.post2``
----------------

修复了代码开头有空行时的渲染问题

禁止 :math:`\mathbb{M}\text{anim}` 缓存以加快渲染速度

``v1.0.7.post1``
----------------

修复使用 ``code_file`` 时出现的问题

``v1.0.7``
----------

更新 ``pip`` 安装依赖配置

.. admonition:: 参数更改

    ``camera_floating_maximum_value`` → ``camera_floating_max_value``

    ``screen_scale`` → ``camera_scale``

报错信息优化

``v1.0.6``
------------

修复代码超长导致进度条格式错误的问题

重构（ ``renderer`` ）：优化 ``CodeVideoRenderer`` 的结构和错误处理（详见 `#1 <https://github.com/ZhuChongjing/CodeVideoRenderer/pull/1>`_）

``v1.0.5.post2``
----------------

修复了 ``pip`` 依赖库安装版本问题，确保所有依赖库的版本与项目要求一致。

修复渲染输出的ANSI转义在不同编译器显示颜色不同的问题。

``v1.0.5.post1``
----------------

修复通过 ``pip`` 安装失败的问题

``v1.0.5``
----------

新增 ``output`` 参数到 :meth:`~.render` 方法中，用于控制渲染输出。

将 ``CodeVideo`` 从函数变为类，以提高代码的可维护性和扩展性。

``v1.0.4``
------------

修复渲染时间计算问题

删除 ``font`` 参数

优化终端渲染信息

优化代码运行速度

``v1.0.3``
------------

修复代码偏移问题（:math:`\mathbb{M}\text{anim}` 自带 bug）

修复换行时相机不及时移动的问题

修复光标在换行时不在开头停顿的问题

每行代码首尾空白字符不参与动画，以免增加动画时长

当前行背景宽度更改

新增 ``line_spacing`` 参数用于更改行距

优化终端渲染信息

优化相机移动逻辑

更早版本
------------

``v1.0.3`` 及之前版本没有更新日志
