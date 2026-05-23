Changelog
=========

This document records all notable changes to CodeVideoRenderer.

.. seealso::

   * :doc:`installation` for upgrade instructions
   * `GitHub releases <https://github.com/ExploreMaths/CodeVideoRenderer/releases>`_ for detailed change information
   * :doc:`contributing` for information on reporting issues

CodeVideoRenderer 1.2.3 :bdg-success-line:`Latest`
------------------------------------------------------------------------

**Date**: May 4, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.3/.

.. admonition:: Additions
   :class: additions

   * Added ``moviepy`` version requirement ``<2.0.0`` for Python 3.8

   * Added ``typing-extensions`` dependency with a minimum required version of ``4.0.0``

   * Added ``imageio-ffmpeg`` dependency with a minimum required version of ``0.4.0``

   * Added ``typeguard`` dependency with a minimum required version of ``3.0``

   * Added import of ``annotations`` (from ``__future__``) in ``typing.py`` and ``utils.py`` for compatibility with Python 3.8, 3.9

.. admonition:: Changes
   :class: changes

   * Downgraded the minimum required version of the ``manim`` dependency from ``0.20.1`` to ``0.18.0``

   * Downgraded the minimum required version of the ``numpy`` dependency from ``2.4.2`` to ``1.24.4``

   * Downgraded the minimum required version of the ``pillow`` dependency from ``11.2.1`` to ``9.1``

   * Downgraded the minimum required Python version from ``3.9`` to ``3.8``

   * Modified the import methods of ``TypeAlias``, ``UnionType`` and ``VideoFileClip`` for compatibility with Python 3.8, 3.9

   * Replaced all type annotations in the format of ``type | type`` with ``Union[type, type]`` for compatibility with Python 3.8, 3.9

   * Changed all ``PathLike[str]`` to ``PathLike`` (as ``PathLike`` in Python 3.8 does not support generics)

   * Replaced all type annotations in the formats of ``tuple[...]``, ``list[...]`` and ``dict[...]`` with ``Tuple[...]``, ``List[...]`` and ``Dict[...]`` respectively for compatibility with Python 3.8

   * Switched the type checker from :func:`typeChecker` to :func:`typeguard.typechecked`

.. admonition:: Deletions
   :class: deletions

   * Removed :func:`checkType` and :func:`typeChecker` from ``utils.py``

CodeVideoRenderer 1.2.2
------------------------------------------------------------------------

**Date**: Apr 27, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.2/.

.. admonition:: Changes
   :class: changes

   * Convert all documents (functions, classes, constants) to the reStructuredText format for better compatibility with Sphinx documentation.

   * Change the default value of the ``formatter_style`` parameter in the :class:`~.CameraFollowCursorCV` class to ``"material"``.

CodeVideoRenderer 1.2.1
----------------------------

**Date**: Mar 22, 2026

See details at https://pypi.org/project/codevideorenderer/1.2.1/.

.. admonition:: Additions
   :class: additions

   * Add the :data:`~.__version__` variable to ``__init__.py``

   * Add the :data:`~.__all__` variable to ``config.py``, ``renderer.py``, ``typing.py``, and ``utils.py``

   * Add the :attr:`~.formatter_style` parameter to the :class:`~.CameraFollowCursorCV` class

   * Add beautification for terminal error messages

   * Add parameter descriptions and type annotations for all functions and classes

   * Add the :meth:`~.__getattribute__` function to the :class:`~.CameraFollowCursorCV` class to prevent data modification by changing attributes

   * Add the CodeVideoRendererFont font to support Chinese characters

   * Add the :data:`~.NOT_AVAILABLE_CHARACTERS` variable to ``config.py``

   * Add the :class:`~.Parameters` class to the :class:`~.CameraFollowCursorCV` class for managing and retrieving parameters

   * Add ``version.py`` to manage package version

.. admonition:: Changes
   :class: changes

   * Change the function name format from ``aaa_bbb`` (snake_case) to ``aaaBbb`` (camelCase)

   * Change the :data:`~.PygmentsLanguage` class to a ``Literal`` type

   * Refactor the ``default_progress_bar`` function into the :class:`~.DefaultProgressBar` class

   * Split ``CameraFollowCursorCVR.py`` into ``renderer.py``, ``typing.py``, and ``utils.py``

   * Modify the whitespace handling logic to improve rendering speed

   * Make partial modifications to the parameters and descriptions of the :class:`~.CameraFollowCursorCV` class

   * Modify some terminal output content

   * Update the value of :data:`~.CODE_OFFSET` in ``config.py``

.. admonition:: Fixes
   :class: fixes

   * Fix the code offset issue caused by `@gaojj2000 <https://github.com/gaojj2000>`_ in `#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_

   * Fix the ``code_line_rectangle`` offset issue that occurs when code offset happens

.. admonition:: Deletions
   :class: deletions

   * Remove the :data:`~.DEFAULT_CODE_FORMATTER_STYLE`, :data:`~.AVAILABLE_CHARACTERS`, and :data:`~.EMPTY_CHARACTER` variables from ``config.py``

CodeVideoRenderer 1.1.2
----------------------------

**Date**: Feb 11, 2026

See details at https://pypi.org/project/codevideorenderer/1.1.2/.

.. admonition:: Fixes
   :class: fixes

   * Fixed the cursor position error caused by manim uniformly removing leading spaces on each line (see `#5 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/5>`_ for details).

CodeVideoRenderer 1.1.1
----------------------------

**Date**: Feb 11, 2026

See details at https://pypi.org/project/codevideorenderer/1.1.1/.

.. admonition:: Additions
   :class: additions

   * Added compatibility updates for ``manim==0.19.1`` (see `#3 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/3>`_ for details).

   * Added glow effects.

   * Adapted to OpenGL rendering and resolved related issues when switching to OpenGL rendering (see `#4 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/4>`_ for details).

   * Added the ``renderer`` parameter to :class:`~.CameraFollowCursorCV` to configure the renderer.

.. admonition:: Changes
   :class: changes

   * Modified :func:`~.type_checker` to adapt to ``Literal`` and :data:`~.PygmentsLanguage`.

   * Optimized terminal display.

   * Integrated ``functions.py`` into ``CameraFollowCursorCVR.py``.

   * Adopted the ``timeit`` module to calculate rendering time and eliminate redundant variables.

   * Changed the type of the ``language`` parameter in :class:`~.CameraFollowCursorCV` from ``str`` to :data:`~.PygmentsLanguage`.

   * Refactored the file structure.

.. admonition:: Deletions
   :class: deletions

   * Removed summary output before rendering the ``Scene``.

   * Deleted unused constants in ``config.py``.

CodeVideoRenderer 1.1.0
----------------------------

**Date**: Dec 25, 2025

See details at https://pypi.org/project/codevideorenderer/1.1.0/.

.. admonition:: Additions
   :class: additions

   * Added opening animation.

.. admonition:: Changes
   :class: changes

   * Revised camera movement logic.

.. admonition:: Fixes
   :class: fixes

   * Fixed the issue where output could not be terminated when ``output=False`` was used in :meth:`~.render`.

CodeVideoRenderer 1.0.9.post2
------------------------------

**Date**: Nov 24, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9.post2/.

.. admonition:: Changes
   :class: changes

   * Adjusted the spacing between the cursor and characters.

CodeVideoRenderer 1.0.9.post1
------------------------------

**Date**: Nov 17, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9.post1/.

.. admonition:: Changes
   :class: changes

   * Redesigned progress bar style and added a ``{task.completed}/{task.total}`` field.

.. admonition:: Fixes
   :class: fixes

   * Fixed partial issues with the :func:`~.type_checker` decorator.

CodeVideoRenderer 1.0.9
----------------------------

**Date**: Nov 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.9/.

.. admonition:: Changes
   :class: changes

   * Overhauled and rewrote camera movement logic, and added automatic camera scaling.

   * Used ``rich`` to print initial data at the start of rendering.

   * Rewrote the rendering progress bar with ``rich.progress``.

   * Refactored type checking and adopted ``rich.traceback`` for cleaner error output.

CodeVideoRenderer 1.0.8.post1
--------------------------------

**Date**: Nov 8, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.8.post1/.

.. admonition:: Fixes
   :class: fixes

   * Fixed issues in ``__init__.py``.

CodeVideoRenderer 1.0.8
----------------------------

**Date**: Nov 8, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.8/.

.. admonition:: Changes
   :class: changes

   * Reverted the default font to Consolas, as Cascadia Code converts ``>=`` to ``≥`` and triggers internal Manim errors.

.. admonition:: Fixes
   :class: fixes

   * Fixed code offset errors.

.. admonition:: Deletions
   :class: deletions

   * Removed unused constants in ``/renderer/config.py``.

CodeVideoRenderer 1.0.7.post3
--------------------------------

**Date**: Nov 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post3/.

.. admonition:: Fixes
   :class: fixes

   * Re-uploaded complete source code due to incomplete package upload on pip.

CodeVideoRenderer 1.0.7.post2
---------------------------------

**Date**: Nov 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post2/.

.. admonition:: Changes
   :class: changes

   * Disabled Manim caching to improve rendering speed.

.. admonition:: Fixes
   :class: fixes

   * Fixed rendering errors triggered by blank lines at the start of code content.

CodeVideoRenderer 1.0.7.post1
--------------------------------

**Date**: Oct 3, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7.post1/.

.. admonition:: Fixes
   :class: fixes

   * Resolved bugs occurring when using the ``code_file`` parameter.

CodeVideoRenderer 1.0.7
----------------------------

**Date**: Oct 3, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.7/.

.. admonition:: Changes
   :class: changes

   * Updated pip dependency configuration.

   * Changed parameter ``camera_floating_maximum_value`` to ``camera_floating_max_value``, ``screen_scale`` to ``camera_scale``.

   * Improved error message presentation.

CodeVideoRenderer 1.0.6
----------------------------

**Date**: Sep 27, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.6/.

.. admonition:: Changes
   :class: changes

   * Refactored the renderer module: optimized the structure and error handling of CodeVideoRenderer (see `#1 <https://github.com/ExploreMaths/CodeVideoRenderer/pull/1>`_ for details).

.. admonition:: Fixes
   :class: fixes

   * Fixed progress bar formatting errors caused by overly long code lines.

CodeVideoRenderer 1.0.5.post2
---------------------------------

**Date**: Sep 25, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5.post2/.

.. admonition:: Fixes
   :class: fixes

   * Fixed version compatibility issues of pip dependencies to ensure full compliance with project requirements.

   * Resolved inconsistent color display of ANSI escape sequences in rendering outputs across different terminals/compilers.

CodeVideoRenderer 1.0.5.post1
-------------------------------

**Date**: Sep 23, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5.post1/.

.. admonition:: Fixes
   :class: fixes

   * Fixed pip installation failures.

CodeVideoRenderer 1.0.5
----------------------------

**Date**: Sep 20, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.5/.

.. admonition:: Additions
   :class: additions

   * Added the new ``output`` parameter to the :meth:`~.render` method to control rendering output behavior.

.. admonition:: Changes
   :class: changes

   * Refactored ``CodeVideo`` from a function to a class for better code maintainability and scalability.

CodeVideoRenderer 1.0.4
----------------------------

**Date**: Sep 6, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.4/.

.. admonition:: Changes
   :class: changes

   * Optimized terminal rendering logs.

   * Improved overall code execution efficiency.

.. admonition:: Fixes
   :class: fixes

   * Fixed calculation errors of rendering duration.

.. admonition:: Deletions
   :class: deletions

   * Removed the deprecated ``font`` parameter.

CodeVideoRenderer 1.0.3
----------------------------

**Date**: Aug 29, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.3/.

.. admonition:: Additions
   :class: additions

   * Added the new ``line_spacing`` parameter to customize line spacing.

.. admonition:: Changes
   :class: changes

   * Excluded leading and trailing whitespace of each code line from animation playback to reduce redundant animation duration.

   * Adjusted the background width of the currently highlighted code line.

   * Optimized terminal rendering information output.

   * Fine-tuned camera movement logic.

.. admonition:: Fixes
   :class: fixes

   * Fixed the issue where the cursor failed to pause at the start of new lines.

CodeVideoRenderer 1.0.2
----------------------------

**Date**: Aug 26, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.2/.

.. admonition:: Additions
   :class: additions

   * Introduced Pydantic ``@validate_call`` for parameter validation.
   * Added explicit parameters: ``code_string``, ``code_file``, ``font``, ``language``, ``interval_range``, ``camera_floating_maximum_value``, ``camera_move_interval``, ``camera_move_duration``, and ``screen_scale``.
   * Added rendering time tracking using :func:`time.time`.
   * Added syntax-highlighted live code preview in terminal output with box borders and completion marks.
   * Added :meth:`~.replace_empty_chars` to validate non-empty code input.

.. admonition:: Changes
   :class: changes

   * Replaced ``**kwargs`` with explicit typed parameters.
   * Replaced :meth:`~.has_chinese` check with :meth:`str.isascii` for non-ASCII character detection.
   * Set default ``formatter_style`` to ``"material"``.
   * Improved occupy-block width calculation.
   * Overhauled terminal rendering logs with ANSI colors and progress borders.

.. admonition:: Deletions
   :class: deletions

   * Removed the ``speed`` parameter (already removed in 1.0.1.0).
   * Removed ``has_chinese`` method.

CodeVideoRenderer 1.0.1.2
----------------------------

**Date**: Aug 23, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.2/.

.. admonition:: Additions
   :class: additions

   * Added the :class:`~.LoopMovingCamera` class for continuous smooth camera tracking without infinite loops.

.. admonition:: Changes
   :class: changes

   * Changed default ``interval`` from ``0.05`` to ``0.3``.
   * Succeeded output path retrieval using ``self.renderer.file_writer.movie_file_path``.
   * Empty lines and character intervals now use ``random.uniform(interval-0.05, interval+0.05)``.

.. admonition:: Deletions
   :class: deletions

   * Removed :meth:`~.move_camera_to_cursor` method (replaced by :class:`~.LoopMovingCamera`).
   * Removed the ASCII table docstring from :meth:`~.construct`.

CodeVideoRenderer 1.0.1.1
----------------------------

**Date**: Aug 22, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.1/.

.. admonition:: Additions
   :class: additions

   * Added the new ``scale`` parameter to control camera frame scale.
   * Added :meth:`set_z_index` to cursor and code mobjects for proper layering.

.. admonition:: Changes
   :class: changes

   * Reduced cursor width from ``0.005`` to ``0.0005``.
   * Changed default line number color to ``GREY``; the current line number is highlighted in ``WHITE``.
   * Changed ``code_line_rectangle`` style to filled background color ``#333333``.
   * Improved terminal success message with green ANSI color.

.. admonition:: Deletions
   :class: deletions

   * Removed the code window (``window``) from the scene.

CodeVideoRenderer 1.0.1.0
----------------------------

**Date**: Aug 19, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.1.0/.

.. admonition:: Additions
   :class: additions

   * Added minimum interval validation to prevent overly short intervals.
   * Added ``code_line_rectangle`` to highlight the current code line.
   * Added left-right floating to camera movement.

.. admonition:: Changes
   :class: changes

   * Removed the ``speed`` parameter; camera movement now uses a fixed ``0.2`` second run time.
   * Improved terminal output with ANSI colors, total line count display, and refined progress bar format.
   * Translated comments and docstrings from Chinese to English.
   * Merged :meth:`~.successfully_rendered_info` logic into the :meth:`~.render` method.

CodeVideoRenderer 1.0.0.5
----------------------------

**Date**: Aug 18, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.5/.

.. admonition:: Additions
   :class: additions

   * Added :meth:`~.has_chinese` method to detect Chinese characters and punctuation.
   * Added the ``code_file`` parameter to read code from a file.
   * Added automatic Tab-to-spaces conversion (4 spaces).
   * Added handling for empty code lines.
   * Added skipping of leading spaces during animation playback.
   * Added extensive inline comments and an ASCII table docstring in :meth:`~.construct`.

.. admonition:: Changes
   :class: changes

   * Renamed parameter ``floating_pos`` to ``floating_camera``.
   * Adjusted cursor dimensions (narrower and shorter).
   * Changed initial camera scale from ``0.25`` to ``0.3``.
   * Moved :meth:`~.move_camera_to_cursor` definition earlier in the class.

CodeVideoRenderer 1.0.0.4
----------------------------

**Date**: Aug 17, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.4/.

.. admonition:: Deletions
   :class: deletions

   * Removed ``main.py``, keeping only ``renderer.py`` as the single entry point.

CodeVideoRenderer 1.0.0.3
----------------------------

**Date**: Aug 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.3/.

   Re-uploaded package with no code changes.

CodeVideoRenderer 1.0.0.2
----------------------------

**Date**: Aug 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.2/.

   Re-uploaded package with no code changes.

CodeVideoRenderer 1.0.0.1
----------------------------

**Date**: Aug 16, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.1/.

.. admonition:: Additions
   :class: additions

   * Added ``renderer.py`` (a copy of ``main.py``) as the primary renderer module.

.. admonition:: Changes
   :class: changes

   * Changed ``__init__.py`` to import from ``renderer`` instead of ``main``.

CodeVideoRenderer 1.0.0.0
----------------------------

**Date**: Aug 15, 2025

See details at https://pypi.org/project/codevideorenderer/1.0.0.0/.

   Initial release of CodeVideoRenderer.
