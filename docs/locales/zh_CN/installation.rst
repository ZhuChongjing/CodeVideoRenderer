安装
============

CodeVideoRenderer可以使用Python软件包管理器安装。

必备条件
-------------

在安装 CodeVideoRenderer之前，请确保您：

* **Python 3.8 或更高**
* **管道** (Python软件包安装程序)
* **FFmpeg** (用于视频渲染)

我们强烈建议在虚拟环境中安装，因为Manim(严重依赖)可能与您的全局Python环境中的其他软件包发生冲突。

.. 代码块:: bash

   python -m venv .venv
   源.venv/bin/activity # 在Windows上：.venv\Scripts\激活

Installing FFmpeg
^^^^^^^^^^^^^^^^^

.. tab-set:

   .. 标签项目：窗口

      .. 代码块:: bash

         winget 安装 ffmpeg

   .. tab-item:: macOS

      .. 代码块:: bash

         酿造安装 ffmpeg

   .. tab-item:: Linux

      .. 代码块:: bash

         sudo apt 更新
         sudo apt install ffmpeg

正在验证 FFmpeg
^^^^^^^^^^^^^^^^

安装后，确认你的 ``PATH`` 中的FFmpeg 可用：

.. 代码块:: bash

   ffmpeg 版本

您应该看到版本信息已打印。 如果你得到了“未找到的命令”错误，请在继续之前重新启动你的终端或添加FFmpeg 到你的系统 ``PATH`` 。

基本安装
------------------

使用管道安装CodeVideoRenderer：

.. 代码块:: bash

   pip 安装编解码视频渲染器

开发安装
------------------------

从开发源安装：

.. 代码块:: bash

   git clone https://github.com/ExploreMaths/CodeVideoRenderer.git
   cd CodeVideoRenderer
   pip 安装 -e

正在验证安装
----------------------

测试您的安装：

.. code-block:: python

   导入 CodeVideoRenderer
   print(CodeVideoRenderer.__version__)

故障排除
---------------

共同安装问题：

* **ModuleNotFoundError**：确保您使用 Python 3.8+
* **FFmpeg 未找到**: 验证FFmpeg 已安装并在PATH
* **权限错误**: 使用 ``pip install --user`` 或虚拟环境

以后的步骤
----------

After installation, proceed to the :doc:`tutorials` section to start using CodeVideoRenderer.