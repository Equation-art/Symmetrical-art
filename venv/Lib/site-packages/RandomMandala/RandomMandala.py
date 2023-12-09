import math              # 导入数学函数库
import random        # 导入随机数生成库

import PIL      # 导入 Python Imaging Library，用于图像处理
import bezier       # 导入用于生成贝塞尔曲线的库
import matplotlib# 导入用于数据可视化的库 matplotlib
import matplotlib.backends.backend_agg# 导入 matplotlib 的 Agg backend，用于渲染图像
from matplotlib.lines import Line2D# 从 matplotlib 导入 Line2D 用于绘制线型对象
from matplotlib.patches import PathPatch# 从 matplotlib 导入 PathPatch 用于绘制路径型图形
import numpy# 导入用于数值计算的库 numpy



# ===========================================================
#  定义一个函数，将 matplotlib 的 figure 对象转换为 PIL 图像
# ===========================================================
# Following documentation here:
#    https://matplotlib.org/stable/gallery/user_interfaces/canvasagg.html
def figure_to_image(figure):
    """Convert a Matplotlib figure into a PIL image.

    :param figure: A figure (object of the class matplotlib.figure.Figure .)
    :return res: A Python Imaging Library (PIL) image.
    """
    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(figure)# 创建一个 figure 的 Agg canvas

    canvas.draw()# 将 matplotlib 的 figure 渲染到 canvas 上
    rgba = numpy.asarray(canvas.buffer_rgba())# 获取渲染后的 RGBA 值
    res = PIL.Image.fromarray(rgba)# 将 RGBA 数组转换为 PIL Image
    res = res.convert('RGB')# 将图像从 RGBA 转换为 RGB

    return res# 返回转换后的 PIL Image 对象

# 定义一个类 RandomMandala，用于创建曼陀罗图案
class RandomMandala:
    _figure = None# 存储 matplotlib figure 对象
    _axes = None# 存储 matplotlib axes 对象
    _radius: float = 10# 存储生成曼陀罗图案时的半径
    _angle: float = numpy.pi / 6# 存储生成曼陀罗图案时的角度
    _keep_grid_points: bool = False # 存储是否保留网格点的标志
    _seed_points = None      # 存储种子点
    _sym_seed_points = None  # 存储对称种子点
    _symmetric = False  # 存储是否应用对称性的标志
    _points = None  # 存储点集
    _alpha = None  # 存储透明度
    _value = None  # 存储类的当前值

    # ===========================================================
    # 类的初始化方法
    # ===========================================================
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._figure = args[0]   # 如果提供，则将第一个参数设为 figure
        if len(args) > 1:
            self._axes = args[1]     # 如果提供，则将第二个参数设为 axes
        if 'figure' in kwargs:
            self._figure = kwargs['figure'] # 从关键字参数设置 figure
        if 'axes' in kwargs:
            self._axes = kwargs['axes']     # 从关键字参数设置 axes

    # ===========================================================
    # 以下是一系列的设置器和获取器方法
    # ===========================================================
    def set_figure(self, arg):
        self._figure = arg
        return self

    def set_axes(self, arg):
        self._axes = arg
        return self

    def set_seed_points(self, arg):
        self._seed_points = arg
        return self

    def set_points(self, arg):
        self._points = arg
        return self

    def set_angle(self, arg):
        self._angle = arg
        return self

    def set_symmetric(self, arg):
        self._symmetric = arg
        return self

    def set_alpha(self, arg):
        self._alpha = arg
        return self

    def set_value(self, arg):
        self._value = arg
        return self

    # ===========================================================
    # Takers
    # ===========================================================
    def take_figure(self):
        return self._figure

    def take_axes(self):
        return self._axes

    def take_seed_points(self):
        return self._seed_points

    def take_points(self):
        return self._points

    def take_angle(self):
        return self._angle

    def take_symmetric(self):
        return self._symmetric

    def take_alpha(self):
        return self._alpha

    def take_value(self):
        return self._value

    # ===========================================================
    # 定义创建随机种子
    # ===========================================================
    def make_seed_segment(self,
                          radius: float = 10.,
                          angle=numpy.pi / 6,
                          number_of_elements: int = 10,
                          keep_grid_points=False):

        t1 = [radius * r * math.cos(angle) for r in numpy.arange(0, 1, 1 / number_of_elements)]# 计算并存储每个点的 x 坐标
        t2 = [radius * r * math.sin(angle) for r in numpy.arange(0, 1, 1 / number_of_elements)]# 计算并存储每个点的 y 坐标

        b = [(radius * r, 0) for r in numpy.arange(0, 1, 1 / number_of_elements)]# 在基线上创建等间距点

        t = list(zip(t1, t2)) + b# 将顶部和底部的点合并
        self._radius = radius# 设置类中的半径属性
        self._angle = angle# 设置类中的角度属性
        self._keep_grid_points = keep_grid_points# 设置是否保持网格点
        self._seed_points = random.sample(t, len(t))# 从所有点中随机选择，形成种子点集
        self._sym_seed_points = None# 初始化对称种子点为 None
        self._symmetric = False# 设置对称性为 False
        self._value = self._seed_points# 将种子点集设为当前值

        return self

    # ===========================================================
    # 定义创建对称种子段的方法
    # ===========================================================
    def make_seed_symmetric(self, arg=None):
        if isinstance(arg, bool) and not arg:
            return self
        self._sym_seed_points = [(x[0], -x[1]) for x in self._seed_points]# 创建对称种子点
        self._symmetric = True# 设置对称性为 True
        self._value = self._sym_seed_points# 将对称种子点设为当前值
        return self

    # ===========================================================
    # 定义将点转换为贝塞尔曲线节点的方法
    # ===========================================================
    def to_nodes(self, points):
        nodes = numpy.array(points).transpose()# 转换并转置点集为 numpy 数组
        self._value = nodes# 将节点设为当前值
        return self

    # ===========================================================
    # 定义将点转换为贝塞尔曲线的方法
    # ===========================================================
    def to_bezier_curve(self, points):
        nodes = numpy.array(points).transpose()# 转换并转置点集为 numpy 数组

        curve = bezier.Curve.from_nodes(nodes)# 从节点创建贝塞尔曲线
        self._value = curve # 将贝塞尔曲线设为当前值
        return self

    # ===========================================================
    # 定义旋转和填充图形的方法
    # ===========================================================
    def rotate_and_fill(self,
                        face_color="0.2",
                        edge_color=None,
                        location=111,
                        ax=None):
        # Make figure and axes
        if ax is None:# 如果没有提供 ax
            if self._figure is None:# 如果没有提供 figure
                fig, local_ax = matplotlib.pyplot.subplots()# 创建新的图形和轴
            else:
                fig = self._figure
                if isinstance(location, tuple):
                    local_ax = fig.add_subplot(*location)# 如果位置是元组形式，使用元组形式添加子图
                else:
                    local_ax = fig.add_subplot(location)# 使用单一整数形式添加子图
        else:
            local_ax = ax# 使用提供的 ax
            fig = self._figure# 使用提供的 figure


        # Determine rotation angle and seed nodes
        alpha = self._angle# 获取旋转角度
        nodes = self._seed_points# 获取种子点

        if self._symmetric:# 如果应用对称
            alpha = 2 * alpha# 角度加倍
            nodes = nodes + self._sym_seed_points# 合并种子点和对称种子点

        nodes = numpy.array(nodes).transpose()# 转换并转置节点为 numpy 数组

        # 定义旋转矩阵
        rotMat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        # First nodes and plot
        if face_color is None:# 如果没有指定填充颜色
            local_ax.plot(nodes[0], nodes[1], color=edge_color)# 仅绘制边缘
        else:
            local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)# 填充颜色和绘制边缘

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / alpha)):# 对于每次旋转
            nodes = numpy.dot(rotMat, nodes)# 应用旋转矩阵
            if face_color is None:# 如果没有指定填充颜色
                local_ax.plot(nodes[0], nodes[1], color=edge_color)# 仅绘制边缘
            else:
                local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)# 填充颜色和绘制边缘

        # Just mandala plot
        local_ax.set_aspect('equal')# 设置图形的宽高比为相等
        local_ax.axis('off')# 关闭坐标轴

        # Set figure, axes, value
        self._figure = fig # 保存图形
        self._axes = local_ax# 保存轴
        self._value = local_ax# 保存轴的值

        return self

    # ===========================================================
    # Rotate and bezier
    # ===========================================================
    def rotate_and_bezier(self,
                          face_color="0.2",
                          edge_color="0.2",
                          alpha=None,
                          location=111,
                          ax=None):
        # Make figure and axes
        if ax is None:# 如果没有提供轴
            if self._figure is None:# 如果没有现有的图形
                fig, local_ax = matplotlib.pyplot.subplots()# 创建新的图形和轴
            else:
                fig = self._figure# 使用现有的图形
                if isinstance(location, tuple):# 如果位置是元组形式
                    local_ax = fig.add_subplot(*location)# 创建子图
                else:
                    local_ax = fig.add_subplot(location)# 创建子图
        else:
            local_ax = ax# 使用提供的轴
            fig = self._figure# 使用现有的图形

        # Determine rotation angle and seed nodes
        my_angle = self._angle# 获取旋转角度
        nodes = numpy.array(self._seed_points).transpose()# 获取种子节点

        if self._symmetric: # 如果是对称模式
            my_angle = 2 * my_angle# 旋转角度翻倍

        # Rotation matrix
        rotMat = [[math.cos(my_angle), -math.sin(my_angle)], [math.sin(my_angle), math.cos(my_angle)]]# 创建旋转矩阵

        # First nodes and plot
        curve = bezier.Curve.from_nodes(nodes)# 从节点创建贝塞尔曲线
        _ = curve.plot(num_pts=256, color=edge_color, ax=local_ax)# 绘制贝塞尔曲线

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / my_angle)):# 对于每次旋转
            nodes = numpy.dot(rotMat, nodes)# 应用旋转矩阵
            curve = bezier.Curve.from_nodes(nodes)# 从旋转后的节点创建新的贝塞尔曲线
            _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)# 绘制贝塞尔曲线

        # Symmetric case
        if self._symmetric:# 如果是对称模式
            nodes = numpy.array(self._sym_seed_points).transpose()# 获取对称种子节点
            curve = bezier.Curve.from_nodes(nodes)# 从对称种子节点创建贝塞尔曲线
            _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)# 绘制贝塞尔曲线
            for i in range(1, math.floor(2 * numpy.pi / my_angle)): # 对于每次旋转
                nodes = numpy.dot(rotMat, nodes)# 应用旋转矩阵
                curve = bezier.Curve.from_nodes(nodes)# 从旋转后的节点创建新的贝塞尔曲线
                _ = curve.plot(num_pts=256, ax=local_ax, color=edge_color)# 绘制贝塞尔曲线

        # Just mandala plot
        local_ax.set_aspect('equal')# 设置图形的宽高比为相等
        local_ax.axis('off')# 关闭坐标轴

        if alpha is not None:# 如果设置了透明度
            for item in local_ax.get_children():# 遍历所有图形元素
                if isinstance(item, Line2D):# 如果是线条
                    item.set_alpha(alpha)# 设置透明度
                if isinstance(item, PathPatch):# 如果是路径补丁
                    item.set_alpha(alpha)# 设置透明度

        # Set figure, axes, value
        self._figure = fig# 保存图形
        self._axes = local_ax# 保存轴
        self._value = local_ax# 保存轴的值

        return self

    # ===========================================================
    # Rotate and fill bezier polygon
    # ===========================================================
    def rotate_and_bezier_fill(self,
                               face_color=(0.01, 0.01, 0.01),
                               edge_color=(0.01, 0.01, 0.01),
                               pts_per_edge=24,
                               alpha=None,
                               location=111,
                               ax=None):

        # Make figure and axes
        if ax is None:# 如果没有提供轴
            if self._figure is None:# 如果没有现有的图形
                fig, local_ax = matplotlib.pyplot.subplots()# 创建新的图形和轴
            else:
                fig = self._figure# 使用现有的图形
                if isinstance(location, tuple):# 如果位置是元组形式
                    local_ax = fig.add_subplot(*location)# 创建子图
                else:
                    local_ax = fig.add_subplot(location)# 创建子图
        else:
            fig = self._figure# 使用现有的图形
            local_ax = ax# 使用提供的轴

        # Determine rotation angle and seed nodes
        my_angle = self._angle# 获取旋转角度
        if self._symmetric:# 如果是对称模式
            my_angle = 2 * my_angle# 旋转角度翻倍


        nodes1 = numpy.array(self._seed_points).transpose()# 获取第一组种子节点
        if len(self._seed_points) < 4:# 如果种子节点数量小于4
            nodes1con = numpy.array([self._seed_points[-1], self._seed_points[0]]).transpose()# 创建连接的节点
        else:
            nodes1con = numpy.array([self._seed_points[-1],
                                     # self._seed_points[-2],
                                     # self._seed_points[1],
                                     self._seed_points[0]]).transpose()# 创建连接的节点


        # Rotation matrix
        rotMat = [[math.cos(my_angle), -math.sin(my_angle)], [math.sin(my_angle), math.cos(my_angle)]]# 创建旋转矩阵

        # First nodes and plot
        curve1 = bezier.Curve.from_nodes(nodes1)# 从第一组节点创建贝塞尔曲线
        curve1con = bezier.Curve.from_nodes(nodes1con)# 从连接的节点创建贝塞尔曲线
        curved_poly = bezier.CurvedPolygon(curve1, curve1con)# 定义一个 CurvedPolygon 对象，使用提供的曲线和控制点。

        _ = curved_poly.plot(pts_per_edge=pts_per_edge, ax=local_ax, color=face_color) # 绘制曲线多边形

        # Incremental rotation and plotting
        for i in range(1, math.floor(2 * numpy.pi / my_angle)):# 对于每次旋转
            nodes1 = numpy.dot(rotMat, nodes1)# 应用旋转矩阵
            nodes1con = numpy.dot(rotMat, nodes1con)# 应用旋转矩阵
            curve1 = bezier.Curve.from_nodes(nodes1)# 从旋转后的节点创建新的贝塞尔曲线
            curve1con = bezier.Curve.from_nodes(nodes1con)# 从旋转后的连接节点创建新
            curved_poly = bezier.CurvedPolygon(curve1, curve1con)# 定义一个 CurvedPolygon 对象，使用提供的曲线和控制点。
            _ = curved_poly.plot(pts_per_edge=pts_per_edge, ax=local_ax, color=face_color)# 使用指定数量的点每边和颜色绘制 CurvedPolygon。

        if self._symmetric:# 检查曼德拉是否对称。
            self._figure = fig  # 存储当前的图形和坐标轴。
            self._axes = local_ax
            self._symmetric = False# 禁用对称性以进行进一步处理。
            self._angle = 2 * self._angle # 将角度翻倍以进行旋转。
            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points # 交换用于对称的种子点。
            # 旋转曼德拉并填充颜色。
            self.rotate_and_bezier_fill(face_color=face_color,
                                        edge_color=edge_color,
                                        pts_per_edge=pts_per_edge,
                                        ax=local_ax)
            # 将种子点切换回其原始值。
            self._sym_seed_points, self._seed_points = self._seed_points, self._sym_seed_points
            # 重新启用对称性并恢复原始角度。
            self._symmetric = True
            self._angle = self._angle / 2

        # 将坐标轴的纵横比设置为“相等”并关闭坐标轴显示。
        local_ax.set_aspect('equal')
        local_ax.axis('off')
        # 为图中的线和路径设置 alpha（透明度）。
        if alpha is not None:
            for item in local_ax.get_children():
                if isinstance(item, Line2D):
                    item.set_alpha(alpha)
                if isinstance(item, PathPatch):
                    item.set_alpha(alpha)

        # Proper scaling
        # local_ax.set_xscale("linear")
        # print(self._radius)
        # local_ax.set_xlim([-self._radius, self._radius])
        # local_ax.set_ylim([-self._radius, self._radius])

        # 设置 RandomMandala 对象的图形、坐标轴和值属性。
        self._figure = fig
        self._axes = local_ax
        self._value = local_ax
        # 返回修改后的 RandomMandala 对象。
        return self

    # ===========================================================
    # 检查 RandomMandala 对象中是否有图形，并将其作为图像返回。
    # ===========================================================
    def to_image(self):
        if not isinstance(self._figure, matplotlib.pyplot.Figure):
            raise AttributeError("对象中没有图形。")

        return figure_to_image(self._figure)
