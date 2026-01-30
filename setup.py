from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='codevideorenderer',
    version='1.1.1',
    author='Zhu Chongjing',
    author_email='zhuchongjing_pypi@163.com',
    description='A Python library for rendering code videos',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'manim>=0.19.1',
        'rich>=13.0.0',
        'numpy',
        'proglog',
        'moviepy',
        'pillow',
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)