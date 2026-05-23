示例相册
===============

这个画廊展示了各种在 CodeVideoRenderer 操作中的例子，这显示了不同的使用案例和配置。

.. seealso::

    * :doc:`tutorials` for step-by-step guides
    * :doc:`reference` for detailed API documentation
    * :doc:`installation` for setup instructions

基本实例
--------------

简单的 Python 函数
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    从 CodeVideoRenderer 导入摄像机跟随CursorCV

    代码 = ''
    def fibonacci(n):
        """计算nth Fibonacci number"""
        如果n <= 1：
            返回 n
        return fibonacci(n-1) + fibonacci(n-2)

    # 示例用法
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")
    '''

    视频 = 摄像机跟随CursorCV(
        代码=('string', 代码),
        language='python',
        formatter_style='github-dark',
        video_name='Fibonacci示例'
    )
    video.render()

JavaScript 示例
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   js_code = '''
   funct debounce(func, wait)
       允许超时；
       return function executedFunction(...gs)
           const later = () =>
               清除超时(超时)；
               func(...args);
           };
           清除超时(超时)；
           超时= setTimeout(稍后等待)；
       };
   }

   // 使用示例
   const debuncedSearch = debounce(searchfunction, 300)；
   '''

   视频 = 摄像机跟随CursorCV(
       code=('string', js_code),
       language='javascript',
       格式化样式='monokai'
   )
   video.render()

中间示例
---------------------

基于文件的动画
^^^^^^^^^^^^^^^^^^^^

从现有文件生成动画代码：

.. code-block:: python

   视频 = 摄像机跟随CursorCV(
       code=('file', 'src/algorithm.py'),
       language='python',
       video_name='算法实现'
   )
   video.render()

自定义输入速度
^^^^^^^^^^^^^^^^^^^

模拟不同的编码风格：

.. code-block:: python

    # 快速输入(专家代码)
    video_fast = 摄像机跟随CursorCV(
        代码=('string', 'code'),
        language='python',
        间隔范围=(0.03, 0.06)
    )

    # 慢打字(学习/教学)
    video_llow = 摄像机跟随CursorCV(
        代码=('string', 'code'),
        language='python',
        间隔范围=(0.2, 0.4)
    )

高级示例
-----------------

多语言演示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

显示不同编程语言的代码：

.. code-block:: python

    语言示例= [
        ('python', 'print("Hello, World!")'),
        ('javascript', 'console.log("Hello, World!");'),
        ('java', 'System.out.println("Hello, World!");'),
        ('cpp', 'printf("Hello, World!");')
    ]

    对于lang, 语言代码示例：
        视频 = 摄像机跟随CursorCV(
            代码=('string', 代码),
            语言=lang,
            video_name=f'{lang}_example'
        )
        video.render()

自定义样式
^^^^^^^^^^^^^^

实验不同语法高亮主题：

.. code-block:: python

    styles = ['github-dark', 'monokai', 'solarized-dark', 'dracula']

    风格风格的风格：
        视频 = 摄像机跟随CursorCV(
            代码=('string', 'example_code'),
            language='python',
            格式化样式=样式
            video_name=f'style_{style}'
        )
        video.render()

世界实物使用案件
--------------------

算法解释
^^^^^^^^^^^^^^^^^^^^^

演示排序算法：

.. code-block:: python

    sorting_code = '''
    def quicksort(arr):
        if len(arr) <= 1:
            返回 arr
        pivot = arr[len(arr) // 2]
        左键 = [x大于x键值时的x为x为arr]
        中间=[x为x，如果x===键值则为arr中的x]
        right = [x for x in arr if x > keot]
        返回快捷排序(左) + 中 + 快捷排序(右)

    # 示例用法
    数字 = [3、6、8、10、1、2、1]
    sorted_number = quicksort(数字)
    '''

    视频 = 摄像机跟随CursorCV(
        代码=('string', sorting_code),
        language='python',
        video_name='QuicksortDemo'
    )
    video.render()

代码审查演示
^^^^^^^^^^^^^^^^^^^^^^^^^

显示之前/之后的代码改进：

.. code-block:: python

    # 原代码
    original = ''
    def 计算总计 (items):
        总计 = 0
        项目中的项目：
            总计 += item.价格
        返回总计
    '''

    video_before = 摄像机跟随CursorCV(
        代码=('string', 原始),
        language='python',
        video_name='CodeReviewBefore'
    )
    video_before.render()

    # 改进代码
    改进 = ''
    从输入导入列表
    从 dataclasses 导入基准图

    @dataclass
    class Item:
        价格：浮点数

    def calculate_total(items: List[Item]) -> float:
        """计算项目的总价格。"""
        返回 sum(item.price for items)
    '''

    video_after = 摄像机跟随CursorCV(
        代码=('string', 改进),
        language='python',
        video_name='CodeReviewAfter'
    )
    video_after .render()

视频输出
------------

上述所有示例在调用 ``render()`` 之后生成一个 MP4 文件。 默认输出位置遵循Manim的协议：

.. 代码块：文本

   ./media/videos/1080p60/{video_name}.mp4

确切的子目录取决于Manim的质量设置。 You control the file name via the ``video_name`` parameter passed to :class:`~.CameraFollowCursorCV`.

视频输出示例
---------------------

生成的视频将具有以下功能：

* **平滑打字动画** 具有现实的时间
* **语法高亮** 适合于每种语言
* **相机移动** 自然跟随光标
* **专业外观** 适合于演示。
