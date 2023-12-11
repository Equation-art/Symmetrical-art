##贝塞尔曲线模块
####贝塞尔曲线的助手

有关使用该类查找交点的示例， 请参阅曲线-曲线交点Curve。
贝塞尔曲线类 。曲线(节点,度, * ,复制= True ,验证= True ) 
基地：Base  表示贝塞尔曲线。

class bezier.curve.Curve(nodes, degree, *, copy=True, verify=True)
Bases: Base

表示一个贝塞尔曲线.

我们用这个传统的定义: 贝塞尔曲线是从 <math
xmlns="http://www.w3.org/1998/Math/MathML">
  <mi>s</mi> <mo>&#x2208;</mo><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">[</mo> <mn>0</mn><mo>,</mo> <mn>1</mn> <mo data-mjx-texclass="CLOSE">]</mo> </mrow></math>到点的凸组合 <math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub> <mi>v</mi><mn>0</mn></msub><mo>,</mo><msub><mi>v</mi> <mn>1</mn> </msub> <mo>,</mo> <mo>&#x2026;</mo> <mo>,</mo> <msub><mi>v</mi><mi>n</mi></msub></math>某些向量空间中的映射：
  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>B</mi><mo stretchy="false">(</mo><mi>s</mi><mo stretchy="false">)</mo><mo>=</mo><munderover><mo data-mjx-texclass="OP">&#x2211;</mo> <mrow data-mjx-texclass="ORD"><mi>j</mi><mo>=</mo><mn>0</mn></mrow><mi>n</mi></munderover><mrow data-mjx-texclass="ORD"><mrow data-mjx-texclass="OPEN"><mo minsize="2.047em" maxsize="2.047em">(</mo></mrow><mfrac linethickness="0"><mi>n</mi><mi>j</mi></mfrac><mrow data-mjx-texclass="CLOSE"><mo minsize="2.047em" maxsize="2.047em">)</mo></mrow></mrow> <msup><mi>s</mi> <mi>j</mi></msup><mo stretchy="false">(</mo><mn>1</mn><mo>&#x2212;</mo><mi>s</mi><msup><mo stretchy="false">)</mo><mrow data-mjx-texclass="ORD"> <mi>n</mi><mo>&#x2212;</mo><mi>j</mi></mrow> </msup><mo>&#x22C5;</mo><msub> <mi>v</mi><mi>j</mi></msub></math>

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_constructor.png)
>>> import bezier
>>> import numpy as np
>>> nodes = np.asfortranarray([
...     [0.0, 0.625, 1.0],
...     [0.0, 0.5  , 0.5],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> curve
<Curve (degree=2, dimension=2)>

#####参数：
              *nodes (SequenceSequencenumbers.Number) – 曲线中的节点。必须可转换为浮点值的 2D NumPy 数组，其中列代表每个节点，而行是环境空间的维度。
              *Degree ( int ) – 曲线的阶数。假设这正确对应于 的数量nodes。from_nodes()如果尚未计算度数，则使用 。
              *copy ( bool ) – 指示在存储之前是否应复制节点的标志。默认为，因为调用者可以在传入后True自由变异。
              *verify ( bool ) – 指示是否应根据节点数量验证度数的标志。默认为True.

    
    
类方法 from_nodes(nodes, copy=True)¶
从节点创建一个Curve。



根据nodes形状计算degree。

#####参数：
       *nodes (SequenceSequencenumbers.Number)  – 曲线中的节点。必须可转换为浮点值的 2D NumPy 数组，其中列代表每个节点，而行是环境空间的维度。

        *copy ( bool ) – 表示节点在存储前是否应被复制的标志。默认为 True，因为调用者可以在传入节点后自由更改节点。

#####返回:
       构建的曲线。


#####返回类型：
       Curve



property length¶
当前曲线的长度。

计算长度通过:
###### <center>$\int_{B([0,1])}$1dx=$\int$$||B'(s)||_2$ds</center>


返回:
当前曲线长度.

返回类型:
float浮点型

#####copy()
复制当前曲线长度.

Returns:
复制的曲线长度.

Return type:
Curve

#####evaluate(s)
沿着曲线<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>B</mi><mo stretchy="false">(</mo><mi>s</mi><mo stretchy="false">)</mo></math>计算。
此方法充当 （部分）locate()的倒数。

请参阅evaluate_multi()了解更多详情
![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_evaluate.png)
>>> nodes = np.asfortranarray([
...     [0.0, 0.625, 1.0],
...     [0.0, 0.5  , 0.5],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> curve.evaluate(0.75)
array([[0.796875],
       [0.46875 ]])


#####参数：
       s ( float ) – 沿曲线的参数。
#####返回：
       曲线上的点（作为一个包含两个维度的NumPy 数组的单列）
#####返回类型：
       numpy.ndarray   


####evaluate_multi(s_vals)
计算B（s）对于沿曲线的多个点。

这是通过修改后的霍纳方法（针对每个s值进行向量化）来完成的。

>>> nodes = np.asfortranarray([
...     [0.0, 1.0],
...     [0.0, 2.0],
...     [0.0, 3.0],
... ])
>>> curve = bezier.Curve(nodes, degree=1)
>>> curve
<Curve (degree=1, dimension=3)>
>>> s_vals = np.linspace(0.0, 1.0, 5)
>>> curve.evaluate_multi(s_vals)
array([[0.  , 0.25, 0.5 , 0.75, 1.  ],
       [0.  , 0.5 , 1.  , 1.5 , 2.  ],
       [0.  , 0.75, 1.5 , 2.25, 3.  ]])
######参数：s_vals ( numpy.ndarray ) – 沿曲线的参数（作为一维数组）。
######返回：曲线上的点。作为二维 NumPy 数组，列对应于每个s 值，行对应于维度。
######返回类型：numpy.ndarray

####evaluate_hodograph(s)¶
计算切向量<math xmlns="http://www.w3.org/1998/Math/MathML"><msup><mi>B</mi><mo data-mjx-alternate="1">&#x2032;</mo></msup><mo stretchy="false">(</mo><mi>s</mi><mo stretchy="false">)</mo></math>沿着曲线。
![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_evaluate_hodograph.png)


>>> nodes = np.asfortranarray([
...     [0.0, 0.625, 1.0],
...     [0.0, 0.5  , 0.5],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> curve.evaluate_hodograph(0.75)
array([[0.875],
       [0.25 ]])

######参数：s ( float ) – 沿曲线的参数。

######返回：沿曲线的切向量（作为具有单列的二维 NumPy 数组）。

######返回类型：numpy.ndarray

######plot(num_pts, color=None, alpha=None, ax=None)¶
绘制当前曲线。


#####参数：
        *num_pts ( int ) – 要绘制的点数。
        *color (OptionalTuplefloat, float, float) -RGB 配置文件的颜色。
        *alpha (Optionalfloat) –颜色的 Alpha 通道。
        *ax (Optionalmatplotlib.artist.Artist) –matplotlib 轴对象，用于添加绘图。

######返回：
       包含绘图的轴。这可能是新创建的轴。
######返回类型：
       matplotlib.artist.Artist
######增加：
        如果曲线的维度不是2。
####subdivide()¶
       分割曲线B（s）分成左右两半。

取区间<math xmlns="http://www.w3.org/1998/Math/MathML"><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">[</mo><mn>0</mn><mo>,</mo><mn>1</mn><mo data-mjx-texclass="CLOSE">]</mo></mrow></math>并将曲线分成 <math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>B</mi><mn>1</mn></msub><mo>=</mo><mi>B</mi><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">(</mo><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">[</mo><mn>0</mn><mo>,</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo data-mjx-texclass="CLOSE">]</mo></mrow><mo data-mjx-texclass="CLOSE">)</mo></mrow></math>和 <math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>B</mi><mn>2</mn></msub><mo>=</mo><mi>B</mi><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">(</mo><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">[</mo><mfrac><mn>1</mn> <mn>2</mn> </mfrac><mo>,</mo><mn>1</mn><mo data-mjx-texclass="CLOSE">]</mo></mrow><mo data-mjx-texclass="CLOSE">)</mo></mrow></math>。为了做到这一点，还重新参数化曲线，因此生成的左半部分和右半部分都有新节点。

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_subdivide.png)
>>> nodes = np.asfortranarray([
...     [0.0, 1.25, 2.0],
...     [0.0, 3.0 , 1.0],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> left, right = curve.subdivide()
>>> left.nodes
array([[0.   , 0.625, 1.125],
       [0.   , 1.5  , 1.75 ]])
>>> right.nodes
array([[1.125, 1.625, 2.   ],
       [1.75 , 2.   , 1.   ]])

#####返回：
       左右子曲线。

#####返回类型：
       TupleCurve,Curve

#####intersect(other,strategy=IntersectionStrategy.GEOMETRIC, verify=True)
找到与另一条曲线的交点。

有关更多详细信息，请参见[ Curve-Curve Intersection ](https://bezier.readthedocs.io/en/latest/algorithms/curve-curve-intersection.html)

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_intersect.png)

../../_images/curve_intersect.png
>>> nodes1 = np.asfortranarray([
...     [0.0, 0.375, 0.75 ],
...     [0.0, 0.75 , 0.375],
... ])
>>> curve1 = bezier.Curve(nodes1, degree=2)
>>> nodes2 = np.asfortranarray([
...     [0.5, 0.5 ],
...     [0.0, 0.75],
... ])
>>> curve2 = bezier.Curve(nodes2, degree=1)
>>> intersections = curve1.intersect(curve2)
>>> 3.0 * intersections
array([[2.],
       [2.]])
>>> s_vals = intersections[0, :]
>>> curve1.evaluate_multi(s_vals)
array([[0.5],
       [0.5]])

#####参数：
*other ( Curve ) – 与之相交的其他曲线。

*strategy (OptionalIntersectionStrategy) – 要使用的相交算法。默认为几何算法。

*verify (Optionalbool) – 表示在验证输入和电流曲线假设时是否需要格外谨慎。可以禁用以加快执行时间。默认为 True。

#####返回：
2 x N发生交叉点的s- 和- 参数数组（可能为空）。

#####返回类型：
[numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

#####增加：
*[TypeError](https://docs.python.org/3/library/exceptions.html#TypeError) – 如果其他不是曲线（且验证=True）。

*[NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – 如果至少有一条曲线不是二维的（且验证=True）。
*[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError) – 如果策略不是有效的 IntersectionStrategy。

#####self_intersections(strategy=IntersectionStrategy.GEOMETRIC, verify=True)
找到曲线与自身相交的点。

对于一般位置的曲线，不会有自交：

>>> nodes = np.asfortranarray([
...     [0.0, 1.0, 0.0],
...     [0.0, 1.0, 2.0],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> curve.self_intersections()
array([], shape=(2, 0), dtype=float64)


不过，有些曲线确实存在自交。考虑一条具有<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mi>B</mi><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">(</mo><mfrac><mrow><mn>3</mn><mo>&#x2212;</mo><msqrt><mn>5</mn></msqrt></mrow><mn>6</mn></mfrac><mo data-mjx-texclass="CLOSE">)</mo></mrow><mo>=</mo><mi>B</mi><mrow data-mjx-texclass="INNER"><mo data-mjx-texclass="OPEN">(</mo><mfrac><mrow><mn>3</mn><mo>+</mo><msqrt><mn>5</mn></msqrt></mrow><mn>6</mn></mfrac><mo data-mjx-texclass="CLOSE">)</mo></mrow></math>

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_self_intersect2.png)
>>> nodes = np.asfortranarray([
...     [0.0, -1.0, 1.0, -0.75 ],
...     [2.0,  0.0, 1.0,  1.625],
... ])
>>> curve = bezier.Curve(nodes, degree=3)
>>> self_intersections = curve.self_intersections()
>>> sq5 = np.sqrt(5.0)
>>> expected = np.asfortranarray([
...     [3 - sq5],
...     [3 + sq5],
... ]) / 6.0
>>> max_err = np.max(np.abs(self_intersections - expected))
>>> binary_exponent(max_err)
-53

有些曲线（有点病态）可以有多个自交点，不过可能的自交点数量在很大程度上受到度数的限制。例如，这条六度曲线就有两个自交点：
![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_self_intersect3.png)
>>> nodes = np.asfortranarray([
...     [-300.0, 227.5 ,  -730.0,    0.0 ,   730.0, -227.5 , 300.0],
...     [ 150.0, 953.75, -2848.0, 4404.75, -2848.0,  953.75, 150.0],
... ])
>>> curve = bezier.Curve(nodes, degree=6)
>>> self_intersections = curve.self_intersections()
>>> 6.0 * self_intersections
array([[1., 4.],
       [2., 5.]])
>>> curve.evaluate_multi(self_intersections[:, 0])
array([[-150., -150.],
       [  75.,   75.]])
>>> curve.evaluate_multi(self_intersections[:, 1])
array([[150., 150.],
       [ 75.,  75.]])

#####参数：
*strategy (OptionalIntersectionStrategy) –  要使用的交集算法。默认为几何。

*verify (Optionalbool) – 表示在验证当前曲线的假设时是否需要格外谨慎。可以禁用以加快执行时间。默认为 True。

#####返回：
2 x N发生自相交的s1- 和-s2 参数数组（可能为空）。对于每一对我们有<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>s</mi><mn>1</mn></msub><mo>&#x2260;</mo><msub><mi>s</mi><mn>2</mn></msub></math>和<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>B</mi><mo stretchy="false">(</mo><msub><mi>s</mi><mn>1</mn></msub><mo stretchy="false">)</mo><mo>=</mo><mi>B</mi><mo stretchy="false">(</mo><msub><mi>s</mi><mn>2</mn> </msub><mo stretchy="false">)</mo></math>。


#####返回类型：
[numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

#####增加：
*[NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError) –如果曲线不是二维的（且 verify=True）。
*[NotImplementedError ](https://docs.python.org/3/library/exceptions.html#NotImplementedError)-如果战略不是几何的。


####elevate()¶
返回当前曲线的升高度版本。

通过转换当前节点来做到这一点<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>v</mi><mn>0</mn></msub><mo>,</mo><mo>&#x2026;</mo><mo>,</mo><msub><mi>v</mi><mi>n</mi></msub></math>到新节点<math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mi>w</mi><mn>0</mn></msub><mo>,</mo><mo>&#x2026;</mo><mo>,</mo><msub> <mi>w</mi><mrow data-mjx-texclass="ORD"><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msub></math>
 
$w_0$=$v_0$
$w_j$=$j\over n+1$$v_{j-1}$+$n+1-j\over n+1$$v_j$
$w_{n+1}$=$v_n$

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_elevate.png)
>>> nodes = np.asfortranarray([
...     [0.0, 1.5, 3.0],
...     [0.0, 1.5, 0.0],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> elevated = curve.elevate()
>>> elevated
<Curve (degree=3, dimension=2)>
>>> elevated.nodes
array([[0., 1., 2., 3.],
       [0., 1., 1., 0.]])

#####返回：
度数升高的曲线。

#####返回类型：
Curve

####reduce_()
返回当前曲线的度数缩减版本。

通过转换当前节点来做到这一点$v_0$...$v_n$到新节点$w_0$...$w_{n-1}$对应于反转elevate()过程。
这使用了高程矩阵的伪逆。 例如，当从 2 级提升到 3 级时，矩阵$E_2$由此公式得到：
v=[$v_0$  $v_1$  $v_2$]-->[$v_0$  ${v_o+2v_1} \over 3$  ${2v_1+v_2}   \over 3$]=$1\over 3$v$\left[\begin{matrix}3&1&0&0\\0&2&2&0\\0&0&1&3\end{matrix}\right]$

（右）伪逆由下式给出

  $R_2$=$E^T_2$ $(E_2 E^T_2)^{-1}$=$1\over 20$$\left[\begin{matrix}19&-5&1\\3&15&-3\\-3&15&3\\1&-5&19\end{matrix}\right]$
 >>警告:
虽然度提升法保留了起点和终点节点，但度缩减法并不能保证这一点。相反，生成的节点是最小二乘法意义上的 "最佳 "节点（在求解正则方程时）。
 
 
![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_reduce.png)
>>> nodes = np.asfortranarray([
...     [-3.0, 0.0, 1.0, 0.0],
...     [ 3.0, 2.0, 3.0, 6.0],
... ])
>>> curve = bezier.Curve(nodes, degree=3)
>>> reduced = curve.reduce_()
>>> reduced
<Curve (degree=2, dimension=2)>
>>> reduced.nodes
array([[-3. ,  1.5,  0. ],
       [ 3. ,  1.5,  6. ]])
在当前曲线未升高的情况下

![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_reduce_approx.png)
>>> nodes = np.asfortranarray([
...     [0.0, 1.25, 3.75, 5.0],
...     [2.5, 5.0 , 7.5 , 2.5],
... ])
>>> curve = bezier.Curve(nodes, degree=3)
>>> reduced = curve.reduce_()
>>> reduced
<Curve (degree=2, dimension=2)>
>>> reduced.nodes
array([[-0.125,  2.5  ,  5.125],
       [ 2.125,  8.125,  2.875]])


#####返回：
度数减少的曲线。
#####返回类型：
曲线

####specialize(start, end)¶
将曲线专门化为给定的子区间。



![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_specialize.png)
n>>> nodes = np.asfortranarray([
...     [0.0, 0.5, 1.0],
...     [0.0, 1.0, 0.0],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> new_curve = curve.specialize(-0.25, 0.75)
>>> new_curve.nodes
array([[-0.25 ,  0.25 ,  0.75 ],
       [-0.625,  0.875,  0.375]])

这是  [subdivide()](https://bezier.readthedocs.io/en/latest/python/reference/bezier.curve.html#bezier.curve.Curve.subdivide)的通用版本subdivide()，甚至可以匹配该方法的输出：

>>> left, right = curve.subdivide()
>>> also_left = curve.specialize(0.0, 0.5)
>>> np.all(also_left.nodes == left.nodes)
True
>>> also_right = curve.specialize(0.5, 1.0)
>>> np.all(also_right.nodes == right.nodes)
True
#####参数：
 *start ( float ) – 我们正在研究的区间的起点。
*end ( float ) – 我们正在专门处理的区间的终点。

#####返回：
新的特殊处理过的曲线。

#####返回类型：
曲线



####locate(point)¶
在当前曲线上找到一个点。
接出B（s）=p中的s。
.

此方法充当（部分）evaluate()的倒数。
$$
\boxed{注意：
只有在当前曲线没有自交的情况下，才能保证唯一解。本代码假定（但不检查）这一点为真。}$$
![markdown](https://bezier.readthedocs.io/en/latest/_images/curve_locate.png)


>>>nodes = np.asfortranarray([
    [0.0, -1.0, 1.0, -0.75 ],
    [2.0,  0.0, 1.0,  1.625],
...])
>>> nodes = np.asfortranarray([
...     [0.0, -1.0, 1.0, -0.75 ],
...     [2.0,  0.0, 1.0,  1.625],
... ])
>>> curve = bezier.Curve(nodes, degree=3)
>>> point1 = np.asfortranarray([
...     [-0.09375 ],
...     [ 0.828125],
... ])
>>> curve.locate(point1)
0.5
>>> point2 = np.asfortranarray([
...     [0.0],
...     [1.5],
... ])
>>> curve.locate(point2) is None
True
>>> point3 = np.asfortranarray([
...     [-0.25 ],
...     [ 1.375],
... ])
>>> curve.locate(point3) is None
Traceback (most recent call last):
  ...
ValueError: 参数之间不够接近

#####参数：
point (numpy.ndarray) – 曲线上的（D x 1）,其中D是其维度。
#####返回：
如果该点不在 上curve，参数值（s) 对应于point或None
#####返回类型：
Optionalfloat

#####增加：
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError) –如果点的尺寸与当前曲线的尺寸不一致。


####to_symbolic()
转换为一个SymPy矩阵来表示B（s）

$$
\boxed{注意：这个方法需要SymPy}$$


>>> nodes = np.asfortranarray([
...     [0.0, -1.0, 1.0, -0.75 ],
...     [2.0,  0.0, 1.0,  1.625],
... ])
>>> curve = bezier.Curve(nodes, degree=3)
>>> curve.to_symbolic()
Matrix([
[               -3*s*(3*s - 2)**2/4],
[-(27*s**3 - 72*s**2 + 48*s - 16)/8]])

#####返回：
曲线B（s）

#####返回类型：
sympy.Matix

####implicitize()¶
隐含曲线
$$
\boxed{注意：这个方法需要SymPy}$$



>>> nodes = np.asfortranarray([
...     [0.0, 1.0, 1.0],
...     [2.0, 0.0, 1.0],
... ])
>>> curve = bezier.Curve(nodes, degree=2)
>>> curve.implicitize()
9*x**2 + 6*x*y - 20*x + y**2 - 8*y + 12

#####返回：
定义曲线的函数$R^2$通过f(x,y)=0.

#####返回类型：
sympy.Expr


#####增加：
[ValueError](https://docs.python.org/3/library/exceptions.html#ValueError) – 如果曲线的尺寸不是2。
#####property dimension¶
形状所处的维度。
例如，如果形状位于$R^3$,那么维度为3.

类型：[int](https://docs.python.org/3/library/functions.html#int)整型

#####property nodes
定义当前形状的节点。

类型：[numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)