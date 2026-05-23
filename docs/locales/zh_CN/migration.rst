迁移指南
===============

本指南帮助您从旧版本的 CodeVideoRendererer升级。

迁移到 1.2.x
------------------

1.2.x版本引入了断开 API 更改。 从 1.1.x 或更早升级时遵循下面的章节。

函数命名公约
^^^^^^^^^^^^^^^^^^^^^^^^^^

所有公共功能和类已从 **snake_case** 切换到 1.2.1 的 **camelCase** 。

.. 列表表：
   :header-rows: 1
   :widths: 50 50

   * - 老(1.1.x及更早)
     - 新(1.2.x)
   * - ``type_checker``
     - ``typeChecker``

如果你直接从 ``CodeVideoRender.utils`` 调用实用功能，请相应地更新你的代码。

移除工具
^^^^^^^^^^^^^^^^^

以下函数已从 ``utils.py`` 中被移除：

* ``checkType``
* ``typeChecker``

如果你自己的代码依赖于这些函数，则替换为 ``typecececked`` (CodeVideoRender现在内部使用) 或实现你自己的类型检查。

基本用法无需操作
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you only use the high-level :class:`~.CameraFollowCursorCV` API (as shown in :doc:`tutorials`), no code changes are required—the breaking changes affect internal utilities and direct imports from ``utils.py``.
