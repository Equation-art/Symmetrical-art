``贝塞尔``
==========

    贝塞尔曲线，三角形和高级对象的助手。

|linux-build| |macos-build| |windows-build| |coverage|

|pypi| |versions|

|docs| |zenodo| |JOSS|

.. |eacute| unicode:: U+000E9 .. LATIN SMALL LETTER E WITH ACUTE
   :trim:

这个库可提供：

* 支持贝塞尔曲线
* 支持贝塞尔三角形

深入了解一下吧！

.. image:: https://raw.githubusercontent.com/dhermes/bezier/main/docs/images/triangles6Q_and_7Q.png
   :align: center

为什么是贝塞尔？
------------------

贝塞尔曲线（和三角形，等等）是一个使用伯恩斯坦原理的参数曲线：


.. image:: https://raw.githubusercontent.com/dhermes/bezier/main/docs/images/bernstein_basis.png
   :align: center

将曲线定义为一个线性组合：

.. image:: https://raw.githubusercontent.com/dhermes/bezier/main/docs/images/bezier_defn.png
   :align: center

这是基于权重的总和为1的事实：

.. image:: https://raw.githubusercontent.com/dhermes/bezier/main/docs/images/sum_to_unity.png
   :align: center

可以通过考虑三个、四个等等，将其推广到更高阶。
权重和为1的非负权重（在上述式子中我们有两个非负权重 ``s`` 和 ``1-s``）。

由于它们形式简单，贝塞尔曲线：

* 很容易将几何对象建模为参数曲线，三角形，等等；
* 可以通过 `de Casteljau's algorithm`_ (德卡斯特里奥算法)进行高效且数值稳定的计算；

* 可以将凸优化技术运用于多种算法（例如：曲线-曲线相交），因为曲线（或三角形等）是这个原理的凸组合

许多的应用--以及它们的发展历史--在"The Bernstein polynomial basis: A centennial `retrospective`_"中有叙述，
例如；

* 通过使用名为`NURBS`_的几何形状函数来表示数据，对几何模型进行有限元方法(`FEM`_)辅助物理分析

* 用于动态系统的robust control（鲁棒控制）;利用凸性创建曲面

.. _retrospective: https://dx.doi.org/10.1016/j.cagd.2012.03.001
.. _Bernstein basis: https://en.wikipedia.org/wiki/Bernstein_polynomial
.. _de Casteljau's algorithm: https://en.wikipedia.org/wiki/De_Casteljau%27s_algorithm
.. _FEM: https://en.wikipedia.org/wiki/Finite_element_method
.. _NURBS: https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline

安装
------------------

``贝塞尔`` Python 安装包可以通过 `pip`_ 安装：

.. code-block:: console

   $ python     -m pip install --upgrade bezier
   $ python3.11 -m pip install --upgrade bezier
   $ # To install optional dependencies, e.g. SymPy
   $ python     -m pip install --upgrade bezier[full]

安装纯Python版本（即没有二进制扩展）：

.. code-block:: console

   $ BEZIER_NO_EXTENSION=true \
   >   python   -m pip install --upgrade bezier --no-binary=bezier

``贝塞尔`` 是开源的，所以你可以从 `Github`_ 中获取代码并从源码中安装。

.. _pip: https://pip.pypa.io
.. _GitHub: https://github.com/dhermes/bezier/

入门
------------------

例如，创建一个曲线：

.. code-block:: python

   >>> import bezier
   >>> import numpy as np
   >>> nodes1 = np.asfortranarray([
   ...     [0.0, 0.5, 1.0],
   ...     [0.0, 1.0, 0.0],
   ... ])
   >>> curve1 = bezier.Curve(nodes1, degree=2)

还可以确定两条曲线的交点：

.. code-block:: python

   >>> nodes2 = np.asfortranarray([
   ...     [0.0, 0.25,  0.5, 0.75, 1.0],
   ...     [0.0, 2.0 , -2.0, 2.0 , 0.0],
   ... ])
   >>> curve2 = bezier.Curve.from_nodes(nodes2)
   >>> intersections = curve1.intersect(curve2)
   >>> intersections
   array([[0.31101776, 0.68898224, 0. , 1. ],
          [0.31101776, 0.68898224, 0. , 1. ]])
   >>> s_vals = np.asfortranarray(intersections[0, :])
   >>> points = curve1.evaluate_multi(s_vals)
   >>> points
   array([[0.31101776, 0.68898224, 0. , 1. ],
          [0.42857143, 0.42857143, 0. , 0. ]])


然后我们就可以画出这些曲线（以及它们的交点）:

.. code-block:: python

   >>> import seaborn
   >>> seaborn.set()
   >>>
   >>> ax = curve1.plot(num_pts=256)
   >>> _ = curve2.plot(num_pts=256, ax=ax)
   >>> lines = ax.plot(
   ...     points[0, :], points[1, :],
   ...     marker="o", linestyle="None", color="black")
   >>> _ = ax.axis("scaled")
   >>> _ = ax.set_xlim(-0.125, 1.125)
   >>> _ = ax.set_ylim(-0.0625, 0.625)

.. image:: https://raw.githubusercontent.com/dhermes/bezier/main/docs/images/curves1_and_13.png
   :align: center

想要API-level文件，请查询贝塞尔Python `package`_ 文件。

开发
------------------

如果想要添加功能或者运行功能测试，请查看 `DEVELOPMENT doc`_ 以获取更多关于如何开始的信息。

引用
------------------

对于使用``贝塞尔``的出版物，可以引用 `JOSS paper`_ 。可使用下述BibTeX条目：

.. code-block:: rest

   @article{Hermes2017,
     doi = {10.21105/joss.00267},
     url = {https://doi.org/10.21105%2Fjoss.00267},
     year = {2017},
     month = {Aug},
     publisher = {The Open Journal},
     volume = {2},
     number = {16},
     pages = {267},
     author = {Danny Hermes},
     title = {Helper for B{\'{e}}zier Curves, Triangles, and Higher Order Objects},
     journal = {The Journal of Open Source Software}
   }

该库的一个 **特定** 版本可以通过Zenodo DOI引用；查看完整的 `list by version`_ 。

.. _JOSS paper: https://joss.theoj.org/papers/10.21105/joss.00267
.. _list by version: https://zenodo.org/search?page=1&size=20&q=conceptrecid:%22838307%22&sort=-version&all_versions=True

许可
---

``贝塞尔`` 在 Apache 2.0许可下可使用。 查看 `the LICENSE`_ 获取更多细节信息。


.. _Curves: https://bezier.readthedocs.io/en/latest/python/reference/bezier.curve.html
.. _Triangles: https://bezier.readthedocs.io/en/latest/python/reference/bezier.triangle.html
.. _package: https://bezier.readthedocs.io/en/latest/python/reference/bezier.html
.. _DEVELOPMENT doc: https://github.com/dhermes/bezier/blob/main/DEVELOPMENT.rst
.. _the LICENSE: https://github.com/dhermes/bezier/blob/main/LICENSE

.. |docs| image:: https://readthedocs.org/projects/bezier/badge/?version=latest
   :target: https://bezier.readthedocs.io/en/latest/
   :alt: Documentation Status
.. |linux-build| image:: https://github.com/dhermes/bezier/workflows/Linux/badge.svg?branch=main&event=push
   :target: https://github.com/dhermes/bezier/actions?query=workflow%3ALinux
   :alt: Linux Build (GitHub Actions)
.. |macos-build| image:: https://github.com/dhermes/bezier/workflows/macOS/badge.svg?branch=main&event=push
   :target: https://github.com/dhermes/bezier/actions?query=workflow%3AmacOS
   :alt: macOS Build (GitHub Actions)
.. |windows-build| image:: https://github.com/dhermes/bezier/workflows/Windows/badge.svg?branch=main&event=push
   :target: https://github.com/dhermes/bezier/actions?query=workflow%3AWindows
   :alt: Windows Build (GitHub Actions)
.. |pypi| image:: https://img.shields.io/pypi/v/bezier.svg
   :target: https://pypi.org/project/bezier/
   :alt: PyPI Latest
.. |versions| image:: https://img.shields.io/pypi/pyversions/bezier.svg
   :target: https://pypi.org/project/bezier/
   :alt: Package Versions
.. |coverage| image:: https://coveralls.io/repos/github/dhermes/bezier/badge.svg
   :target: https://coveralls.io/github/dhermes/bezier
   :alt: Code Coverage
.. |zenodo| image:: https://zenodo.org/badge/73047402.svg
   :target: https://zenodo.org/badge/latestdoi/73047402
   :alt: Zenodo DOI for ``bezier``
.. |JOSS| image:: https://joss.theoj.org/papers/10.21105/joss.00267/status.svg
   :target: https://dx.doi.org/10.21105/joss.00267
   :alt: "Journal of Open Source Science" DOI for ``bezier``
