实用工具
=========

本模块提供内部助手功能、视频后处理效果以及进度条工具。 大多数用户不需要与这些用户直接互动，但是公开项目在这里被记录为完整项目。

字符串处理
-----------------

* :func:`~.stripEmptyLines` — Remove leading and trailing empty lines from a string.
* :func:`~.findSpacePositions` — Locate non-leading, non-trailing spaces in a multi-line string.
* :func:`~.replaceMiddleSpacesWithOccupyCharacter` — Replace middle spaces with a placeholder character used by Manim.

视频效果
-------------

* :func:`~.addGlowEffect` — Apply a soft-glow filter to a rendered video.

进度条
-------------

* :class:`~.DefaultProgressBar` — A ``rich`` progress bar used during rendering.
* :class:`~.RichProgressBarLogger` — A ``proglog`` logger that bridges to Rich progress bars.

背景管理器
----------------

* :func:`~.noManimOutput` — Suppress Manim console output within a ``with`` block.

.. automodule:: CodeVideoRenderer.utils
    :members:
    :undoc-members: