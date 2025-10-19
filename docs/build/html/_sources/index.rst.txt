.. CodeVideoRenderer documentation master file, created by
   sphinx-quickstart on Thu Oct 16 19:07:38 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CodeVideoRenderer
=================

This library is used to generate videos of input code, with the camera following the movement of the cursor.

-------------------------------------------------------------------------------------------------------------------

Latest Version: ``v1.0.7.post1``

Python Version Requirement: ``>=3.9``

Python Dependencies: ``manim>=0.17.0``, ``pydantic>=2.0``

Third-party Software Dependencies: |ffmpeg|_  |miktex|_

.. _ffmpeg: https://ffmpeg.org/
.. _miktex: https://miktex.org/download

.. |ffmpeg| image:: _static/images/FFmpeg.png
    :width: 80
    :align: middle
    :alt: FFmpeg

.. |miktex| image:: _static/images/MikTex.png
    :width: 30
    :align: middle
    :alt: MikTex

.. important::
    Use ``manim`` for animation rendering, please ensure ``manim`` can run normally before using.

Command-line Installation
*************************

.. code-block:: bash

    pip install CodeVideoRenderer

Contact Us
**********

.. note::
    If you find any issues, please send an email to `my email <mailto:zhuchongjing_pypi@163.com>`_ . Welcome to find bugs and fix them, we will fix them as soon as possible.

Index
*****

.. toctree::
   :maxdepth: 2
   
   CodeVideo
   render
