import random
from typing import Optional, Union

import matplotlib
import matplotlib.cm
import matplotlib.colors
import matplotlib.figure
import matplotlib.pyplot
import numpy
from PaperCut import PaperCut
# 导入必要的库

# ===========================================================
# 实用工具函数
# ===========================================================
def _is_radius_number(obj): # 检查对象是否为正数（浮点数或整数）
    return isinstance(obj, float) or isinstance(obj, int) and obj > 0


def _is_radius_list(obj):# 检查对象是否为正数列表
    return isinstance(obj, (list, tuple)) and all([_is_radius_number(x) for x in obj])


def _is_list_of_tuples(obj): # 检查对象是否为元组列表
    return isinstance(obj, list) and all([isinstance(x, tuple) for x in obj])


def _resize(obj, new_shape):# 根据新的形状调整对象的大小
    if _is_list_of_tuples(obj):
        res = numpy.resize(list(range(len(obj))), new_shape)
        res = [obj[i] for i in res]
    else:
        res = numpy.resize(obj, new_shape)
    return res


# ===========================================================
#

def multi_layer(
    display_fig="0.0",
    hide_fig="1.0",
    display_1=None,
    display_2=None,
    display_3=None,
    default_fig=None,
    default_color=None,
):
    if display_1 is None:
        display_1 = [hide_fig, hide_fig, display_fig]
    if display_2 is None:
        display_2 = [hide_fig, display_fig, hide_fig]
    if display_3 is None:
        display_3 = [display_fig, hide_fig, hide_fig]
    if default_fig is None:
        default_fig = ["0.8", "0.6", "0.2"]
    if default_color is None:
        default_color = ["#5D8AA8", "#E0E0E0", "#88B04B"]  # 海军蓝，灰色，橄榄绿

    return [display_1, display_2, display_3, default_fig, default_color]


def random_papercut(n_rows=1,
                   n_columns=1,
                   radius=1,
                   num_of_axis=7,
                   connecting_function="random",
                   radius_of_elements=6,
                   symmetric_seed=True,
                   face_color=("0.2", "0.6", "0.8"),
                   edge_color=("0.2", "0.6", "0.8"),
                   alpha = None,
                   color_mapper: matplotlib.colors.Colormap = None,
                   figure: Optional[matplotlib.figure.Figure] = None,
                   location=None,
                   **kwargs,

):
    # 定义一个函数用于生成随机剪纸图案
    """Generates random papercuts.

    If 'n_rows' and 'n_columns' are None a figure object with one axes object is returned.

    If the argument 'radius' is a list of positive floats, then a "multi-papercut" is created
    with the papercuts corresponding to each number in the radius list being overlain.

    :type n_rows: int|None
    :param n_rows: Number of rows in the result figure.

    :type n_columns: int|None
    :param n_columns: Number of columns in the result figure.

    :type radius: int|list|tuple
    :param radius: Radius for the papercuts, a number or a list of numbers.
    If a list of numbers then the papercuts are overlain.

    :type num_of_axis: float|int|str|list|tuple|None
    :param num_of_axis: Number of copies of the seed segment that comprise the papercut.

    :type connecting_function: str|None
    :param connecting_function: Connecting function, one of "line", "fill", "bezier", "bezier_fill", "random", or None.
    If 'random' or None a random choice of the rest of values is made.

    :type radius_of_elements: int|str|None
    :param radius_of_elements: Controls how may graphics elements are in the seed segment.

    :type symmetric_seed: bool|str|None
    :param symmetric_seed: Specifies should the seed segment be symmetric or not.
    If 'random' of None random choice between True and False is made.

    :type face_color: str|list|tuple
    :param face_color: Face (fill) color.

    :type edge_color: str|list|tuple
    :param edge_color: Edge (line) color.

    :type alpha: float|None
    :param alpha: Opacity (alpha) float between 0 and 1.

    :type color_mapper: matplotlib.colors.Colormap|None
    :param color_mapper: Color mapper object.

    :type figure: matplotlib.pyplot.Figure|None
    :param figure: Figure to add the random papercut to.

    :type location: tuple|None
    :param location: Location spec to add the random papercut to.

    :type kwargs: **dict
    :param kwargs: Arguments for matplotlib.pyplot.figure .

    :rtype fig: matplotlib.figure.Figure
    :return fig: A figure (object of the class matplotlib.figure.Figure .)
    """

    # 验证 symmetric_seed 参数
    if face_color is None:
        face_color = ["0.2", "0.6", "0.8"]
    if not (isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or
            isinstance(symmetric_seed, bool) or symmetric_seed is None):
        raise TypeError("""The argument 'symmetric_seed' is expected to be
             a Boolean, 'random', or None.""")

    # 验证 num_of_axis 参数
    if not (isinstance(num_of_axis, str) and num_of_axis.lower() == "random" or
            isinstance(num_of_axis, (int, float)) and num_of_axis >= 1.0 or
            num_of_axis is None or
            isinstance(num_of_axis, (list, tuple))):
        raise TypeError("""The argument 'num_of_axis' is expected to be
             a number greater than 1, 'random', or None.""")

    local_connecting_function = connecting_function
    if connecting_function is None:
        local_connecting_function = "fill"

    # 验证 radius 参数
    if not (_is_radius_number(radius) or _is_radius_list(radius)):
        raise TypeError("The argument 'radius' is expected to be a positive number or a list of positive numbers.")

    # 验证 radius_of_elements 参数
    if not (isinstance(radius_of_elements, str) and radius_of_elements.lower() == "automatic" or
            isinstance(radius_of_elements, int) and radius_of_elements > 0 or
            radius_of_elements is None or
            isinstance(radius_of_elements, list)):
        raise TypeError("""The argument 'radius_of_elements' is expected to be
             a positive integer, 'automatic', or None.""")

    local_radius_of_elements = "automatic" if radius_of_elements is None else radius_of_elements

    # 验证 n_rows 参数
    if not (isinstance(n_rows, int) and n_rows > 0 or n_rows is None):
        raise TypeError("The argument 'n_rows' is expected to be a positive integer or None.")

    # 验证 n_columns 参数
    if not (isinstance(n_columns, int) and n_columns > 0 or n_columns is None):
        raise TypeError("The argument 'n_columns' is expected to be a positive integer or None.")

    local_n_rows = 1 if n_rows is None else n_rows
    local_n_columns = 1 if n_columns is None else n_columns

    # 验证 face color 参数
    local_face_color = face_color
    if isinstance(face_color, (list, tuple)) and _is_radius_number(radius):
        local_face_color = face_color[0]

    # 验证 edge color 参数
    local_edge_color = edge_color
    if isinstance(edge_color, (list, tuple)) and _is_radius_number(radius):
        local_edge_color = edge_color[0]

    # 验证 alpha 参数
    local_alpha = alpha
    if not (isinstance(alpha, (int, float)) and 0 <= alpha <= 1 or alpha is None):
        raise TypeError("The argument 'alpha' is expected to be a number between 0 and 1 or None.")

    # 根据参数生成剪纸图案
    if figure is not None and location is not None: # 如果提供了 figure 和 location，直接在指定位置绘制剪纸图案

        ax = figure.add_subplot(*location)

        if isinstance(radius, (list, tuple)):
            rm_func = _random_papercut_multi
        else:
            rm_func = _random_papercut_single

        return rm_func(figure=figure,
                       axes=ax,
                       location=location,
                       n_rows=local_n_rows,
                       n_columns=local_n_columns,
                       radius=radius,
                       num_of_axis=num_of_axis,
                       connecting_function=local_connecting_function,
                       radius_of_elements=local_radius_of_elements,
                       symmetric_seed=symmetric_seed,
                       face_color=local_face_color,
                       edge_color=local_edge_color,
                       alpha=local_alpha,
                       color_mapper=color_mapper,
                       **kwargs)

    else:
        # 如果未提供 figure 或 location，创建新的 figure 并绘制剪纸图案
        return _random_papercuts_figure(n_rows=local_n_rows,
                                       n_columns=local_n_columns,
                                       radius=radius,
                                       num_of_axis=num_of_axis,
                                       connecting_function=local_connecting_function,
                                       radius_of_elements=local_radius_of_elements,
                                       symmetric_seed=symmetric_seed,
                                       face_color=local_face_color,
                                       edge_color=local_edge_color,
                                       alpha=local_alpha,
                                       color_mapper=color_mapper,
                                       **kwargs)


# ===========================================================
# 随机剪纸图案的图形
# ===========================================================
def _random_papercuts_figure(n_rows=None,
                            n_columns=None,
                            radius=1,
                            num_of_axis: Union[int, list, tuple, str, None] = 6,
                            connecting_function: Optional[str] = "fill",
                            radius_of_elements: Union[int, str, None] = 6,
                            symmetric_seed: Union[bool, str, None] = True,
                            face_color="0.2",
                            edge_color="0.2",
                            alpha=None,
                            color_mapper: matplotlib.colors.Colormap = None,
                            **kwargs):
    """Makes a figure with random papercuts."""
    # 创建一个 matplotlib 图形对象
    fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)
    # 遍历行和列，创建每个子图的剪纸图案
    for i in range(n_rows):
        for j in range(n_columns):
            # 定义子图的位置
            locationSpec = (n_rows, n_columns, i * n_columns + j + 1)

            if isinstance(radius, (list, tuple)):
                rm_func = _random_papercut_multi
            else:
                rm_func = _random_papercut_single
            # 调用相应函数创建剪纸图案
            rm_func(figure=fig,
                    axes=None,
                    location=locationSpec,
                    radius=radius,
                    num_of_axis=num_of_axis,
                    connecting_function=connecting_function,
                    radius_of_elements=radius_of_elements,
                    symmetric_seed=symmetric_seed,
                    face_color=face_color,
                    edge_color=edge_color,
                    alpha=alpha,
                    color_mapper=color_mapper)
    # 返回包含剪纸图案的图形
    return fig


# ===========================================================
# 创建一个包含多个随机剪纸图案的图形
# ===========================================================
def _random_papercut_multi(figure=None,
                          axes=None,
                          location=None,
                          radius=None,
                          num_of_axis: Union[int, list, tuple, str, None] = 6,
                          connecting_function: Optional[str] = "fill",
                          radius_of_elements: Union[int, str] = 6,
                          symmetric_seed: Union[bool, str, None] = True,
                          face_color="0.2",
                          edge_color="0.2",
                          alpha=None,
                          color_mapper: matplotlib.colors.Colormap = None,
                          **kwargs):
    """Makes a random multi-papercut."""
    # 如果未提供 radius，则设置默认值
    if radius is None:
        radius = [6, 4, 2]

    # 创建或获取图形对象
    fig = figure
    if figure is None:
        # fig: matplotlib.pyplot.Figure = matplotlib.figure.Figure(**kwargs)
        fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    # 创建或获取子图位置
    locationSpec = location
    if location is None:
        locationSpec = (1, 1, 1)

    # 创建或获取子图对象
    ax = axes
    if axes is None:
        ax = fig.add_subplot(*locationSpec)

    # 为不同的半径调整 num_of_axis 参数的长度
    rotSymOrders = numpy.resize(num_of_axis, len(radius))
    # 设置颜色映射器或调整颜色
    if color_mapper is None:
        faceColors = _resize(face_color, len(radius))
        edgeColors = _resize(edge_color, len(radius))
    else:
        faceColors = [color_mapper(random.random()) for i in range(len(radius))]
        edgeColors = [color_mapper(random.random()) for i in range(len(radius))]
    # 遍历每个半径，创建剪纸图案
    for i in range(len(radius)):
        r = radius[i]
        fc = faceColors[i]
        ec = edgeColors[i]
        rso = rotSymOrders[i]
        _random_papercut_single(figure=fig,
                               axes=ax,
                               location=locationSpec,
                               radius=r,
                               num_of_axis=rso,
                               connecting_function=connecting_function,
                               radius_of_elements=radius_of_elements,
                               bezier_radius_factor=0.,
                               symmetric_seed=symmetric_seed,
                               face_color=fc,
                               edge_color=ec,
                               alpha=alpha,
                               color_mapper=None)
    # 返回包含多个剪纸图
    return fig


# ===========================================================
# 创建一个包含单个随机剪纸图案的图形
# ===========================================================
def _random_papercut_single(figure=None,
                           axes=None,
                           location=None,
                           radius=1,
                           num_of_axis: Union[int, list, str, None] = 6,
                           connecting_function: Optional[str] = "fill",
                           radius_of_elements: Union[int, str] = 6,
                           bezier_radius_factor: float = 0.5,
                           symmetric_seed: Union[bool, str, None] = True,
                           face_color="0.2",
                           edge_color="0.2",
                           alpha=None,
                           color_mapper: matplotlib.colors.Colormap = None,
                           **kwargs):
    """Makes a random papercut."""

    # 创建或获取图形对象
    fig = figure
    if figure is None:
        fig: matplotlib.pyplot.Figure = matplotlib.pyplot.figure(**kwargs)

    # 创建或获取子图对象
    ax = axes

    # 创建或获取子图位置
    locationSpec = location
    if location is None:
        locationSpec = (1, 1, 1)

    # 设置旋转对称性的顺序
    if isinstance(num_of_axis, str) and num_of_axis.lower() == "random" or \
            num_of_axis is None:
        rso = random.sample([3, 4, 5, 6, 7, 12], 1)[0]
    else:
        rso = num_of_axis

    rso = rso[0] if isinstance(rso, list) else rso

    # 设置种子对称性
    if isinstance(symmetric_seed, str) and symmetric_seed.lower() == "random" or symmetric_seed is None:
        ssb = random.random() > 0.3
    else:
        ssb = symmetric_seed

    # 设置元素数量
    local_radius_of_elements = 6 if isinstance(radius_of_elements, str) else radius_of_elements

    # 确定角度
    angle = 2 * numpy.pi / rso
    if ssb:
        angle = angle / 2

    # 生成种子段
    rPaper = (PaperCut(figure=fig, axes=ax)
                .make_seed_segment(radius=radius,
                                   angle=angle,
                                   radius_of_elements=local_radius_of_elements)
                .make_seed_symmetric(ssb))

    # 设置连接函数
    conFunc = connecting_function.lower()
    if conFunc == 'random':
        conFunc = random.sample(['line', 'bezier', 'fill', 'bezier_fill'], 1)[0]

    # 设置颜色
    local_edge_color = edge_color
    local_face_color = face_color
    if color_mapper is not None:
        local_edge_color = color_mapper(random.random())
        local_face_color = color_mapper(random.random())

    # 根据连接函数类型旋转和放置剪纸图案
    if conFunc in {"fill", "polygon"}:

        rPaper.rotate_and_fill(face_color=face_color,
                                 edge_color=edge_color,
                                 location=locationSpec,
                                 ax=ax)

    elif conFunc == "line":

        rPaper.rotate_and_fill(face_color=None,
                                 edge_color=edge_color,
                                 location=locationSpec,
                                 ax=ax)

    elif conFunc in {"bezier", "bezier_fill", "bezier-fill", "bezier fill", "bezierfill"} and \
            isinstance(bezier_radius_factor, (int, float)) and bezier_radius_factor > 0:

        rot_and_place_func = "rotate_and_bezier" if conFunc == "bezier" else "rotate_and_bezier_fill"

        getattr(rPaper, rot_and_place_func)(face_color=face_color,
                                              edge_color=edge_color,
                                              location=locationSpec,
                                              ax=ax)

        local_ax = rPaper.take_axes()

        (rPaper
         .make_seed_segment(radius=radius * bezier_radius_factor,
                            angle=numpy.pi / rso,
                            radius_of_elements=local_radius_of_elements)
         .make_seed_symmetric(symmetric_seed))

        getattr(rPaper, rot_and_place_func)(face_color=face_color,
                                              edge_color=edge_color,
                                              location=locationSpec,
                                              alpha=alpha,
                                              ax=local_ax)

    elif conFunc == "bezier":

        rPaper.rotate_and_bezier(face_color=face_color,
                                   edge_color=edge_color,
                                   location=locationSpec,
                                   alpha=alpha,
                                   ax=ax)

    elif conFunc in {"bezier_fill", "bezier-fill", "bezier fill", "bezierfill"}:

        rPaper.rotate_and_bezier_fill(face_color=face_color,
                                        edge_color=edge_color,
                                        location=locationSpec,
                                        alpha=alpha,
                                        ax=ax)

    else:
        raise TypeError("""The argument 'connecting_function' is expected to be one of 
        'fill', 'line', 'bezier', 'bezier_fill', 'random', or None.""")

    return fig
