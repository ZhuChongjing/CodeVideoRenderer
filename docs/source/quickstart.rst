快速上手
========

以下代码展示了如何生成一个最简单的视频：

.. code-block:: python

    from CodeVideoRenderer import CameraFollowCursorCV
    video = CameraFollowCursorCV(
        video_name="Demo",                    # 文件名
        code_string="print('Hello World!')",  # 代码
        language="python"                     # 语言
    )
    video.render()

渲染结束后，您将在终端看到 Demo.mp4 文件的保存路径。

.. admonition:: Demo.mp4

    .. raw:: html

        <video width="100%" controls>
            <source src="_static/Demo.mp4" type="video/mp4">
            您的浏览器不支持 video 标签。
        </video>