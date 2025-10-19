CodeVideo
=========

A video object.

.. code-block:: python

    class CodeVideo(
        video_name: str = "CodeVideo",
        code_string: str = None,
        code_file: str = None,
        language: str = None,
        line_spacing: float = 0.7,
        interval_range: tuple[float, float] = (0.2, 0.2),
        camera_floating_max_value: float = 0.1,
        camera_move_interval: float = 0.1,
        camera_move_duration: float = 0.5,
        camera_scale: float = 0.5
    )

.. list-table::
    :widths: 30 70

    * - ``video_name``
      - The name of the generated video file.
        
    * - ``code_string``
      - The code string passed in directly.

    * - ``code_file``
      - The path to the code file.
        
    * - ``language``
      - The code language (for syntax highlighting).
        
    * - ``line_spacing``
      - The line spacing of the code.
        
    * - ``interval_range``
      - The range of time intervals for displaying characters (seconds), in tuple form; minimum value is 0.2.
        
    * - ``camera_floating_max_value``
      - The maximum range of camera floating, value less than or equal to 0.
        
    * - ``camera_move_interval``
      - The time interval for automatic camera movement (seconds), value less than or equal to 0.
        
    * - ``camera_move_duration``
      - The duration of camera movement (seconds), value less than or equal to 0.
        
    * - ``camera_scale``
      - The scale of the camera.

Use ``validate_call`` from ``pydantic``, which will automatically check the parameter types when you pass them in to ensure their correctness.

.. caution::
    ``code_string`` and ``code_file`` cannot be passed in at the same time, and the code passed in cannot contain non-ASCII characters.
