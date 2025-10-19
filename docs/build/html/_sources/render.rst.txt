render
======

You can use the ``render`` method of the ``CodeVideo`` object to generate a video, and check the video's save location in the terminal.

.. code-block:: python

    def render(output: bool = True)

.. list-table::
    :widths: 30 70

    * - ``output``
      - Whether to output the video save location in the terminal.

It may take a little time, please be patient.

.. admonition:: An example of rendering a video.

    .. code-block:: python

        from CodeVideoRenderer import *
        video = CodeVideo(code_string="print('Hello World!')", language='python')
        video.render()

    .. raw:: html

        <video width="100%" controls>
            <source src="_static/videos/CodeVideo.mp4" type="video/mp4">
            你的浏览器不支持 HTML5 视频播放，请更新浏览器。
        </video>

