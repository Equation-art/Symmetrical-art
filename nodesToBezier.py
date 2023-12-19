import numpy
import matplotlib.pyplot as plt
import math
import bezier
import random

class SeedGenerator:
    def __init__(self):
        self._radius = None
        self._angle = None
        self._keep_grid_points = None
        self._seed_points = None
        self._sym_seed_points = None
        self._symmetric = None
        self._value = None

    def make_seed_segment(self,
                          radius: float = 20.,
                          angle=numpy.pi / 4,
                          radius_of_elements: int = 10,
                          keep_grid_points=False):

        t1 = [5*radius * r * math.cos(angle) for r in numpy.arange(0, 1, 1 / radius_of_elements)]# 计算并存储每个点的 x 坐标
        t2 = [5*radius * r * math.sin(angle) for r in numpy.arange(0, 1, 1 / radius_of_elements)]# 计算并存储每个点的 y 坐标
        '''
        numpy.arange(0, 1, 1 / radius_of_elements): 这个函数创建一个数值范围从0到1，步长为 1 / radius_of_elements 的数组。它表示后续计算中的变量 'r'。
        5 * radius * r * math.cos(angle): 这是用于计算一个点的 x 坐标的公式。它涉及到半径、当前 'r' 的值，以及角度的余弦值（可能在你的代码的其他地方定义为 'angle'）。
        列表推导式 [5 * radius * r * math.cos(angle) for r in numpy.arange(0, 1, 1 / radius_of_elements)]: 
        这通过迭代由 numpy.arange 生成的数组中的每个 'r' 值构建一个列表。对于每个 'r'，它使用指定的公式计算相应的 x 坐标。
        '''

        b = [(5*radius * r, 0) for r in numpy.arange(0, 1, 1 / radius_of_elements)]# 在基线上创建等间距点

        t = list(zip(t1, t2)) + b# 将顶部和底部的点合并
        self._radius = radius# 设置类中的半径属性
        #在Python中，self 是对类实例的引用。它是类中实例方法的第一个参数，表示对象实例本身。
        #_radius：这是类的实例变量。变量名前的下划线（_radius）通常表示这是一个内部变量，建议在类外部不直接访问。
        #radius：这是要赋给 _radius 变量的值。通常，radius 是一个传递给类构造函数或其他方法的参数。
        #self._radius = radius 这行代码的作用是将类实例的 _radius 变量设置为传入的 radius 值。这是在对象创建过程中或对象生命周期中初始化或更新对象状态的常见操作。
        self._angle = angle# 设置类中的角度属性
        self._keep_grid_points = keep_grid_points# 设置是否保持网格点
        self._seed_points = random.sample(t, len(t))# 从所有点中随机选择，形成种子点集
        self._sym_seed_points = None# 初始化对称种子点为 None
        self._symmetric = False# 设置对称性为 False
        self._value = self._seed_points# 将种子点集设为当前值

        return self

    def make_seed_symmetric(self, arg=None):
        # 这是一个方法的定义，名为 make_seed_symmetric。它接受一个参数 arg，默认值为 None。该方法似乎属于某个类，因为它有 self 参数，表示它是一个实例方法。
        if isinstance(arg, bool) and not arg:  # 这一行检查参数 arg 是否为布尔类型且为 False。
            # 如果是，它直接返回当前实例 self，即返回调用这个方法的对象。
            # 这是为了提供一种选择，让用户可以选择是否执行对称性操作。
            return self
        self._sym_seed_points = [(x[0], -x[1]) for x in self._seed_points]  # 创建对称种子点
        # 这一行创建了对称的种子点。它通过对 _seed_points 中的每个点 (x[0], x[1]) 进行处理，
        # 创建一个新的点 (x[0], -x[1])，
        # 将其添加到 _sym_seed_points 列表中。
        # 这样就获得了关于 x 轴对称的点集。
        self._symmetric = True  # 设置对称性为 True
        # 这一行将实例变量 _symmetric 设置为 True，表示对象现在是对称的。
        self._value = self._sym_seed_points  # 将对称种子点设为当前值
        # 这一行将对象的 _value 属性设置为对称种子点 _sym_seed_points。存在类中。
        return self

    def to_nodes(self, points):
        # 它接受一个参数 ，points点集。
        nodes = numpy.array(points).transpose()  # 转换并转置点集为 numpy 数组
        # 这一行将传入的点集 points 转换成一个 NumPy 数组，
        # 并进行转置操作。numpy.array(points) 将点集转换为 NumPy 数组，
        # 然后 transpose() 方法对数组进行转置操作，即交换行和列。
        self._value = nodes  # 将节点设为当前值
        return self

    def to_bezier_curve(self, points):
        nodes = numpy.array(points).transpose()  # 转换并转置点集为 numpy 数组
        # 这一行将传入的点集 points 转换成一个 NumPy 数组，
        # 并进行转置操作。numpy.array(points)
        # 将点集转换为 NumPy 数组，然后 transpose() 方法对数组进行转置操作，即交换行和列。
        curve = bezier.Curve.from_nodes(nodes)  # 从节点创建贝塞尔曲线
        # 这一行使用 bezier 模块的 Curve.from_nodes 方法，
        # 从转置后的节点数组 nodes 创建一个贝塞尔曲线对象，
        # 并将其赋值给变量 curve。
        self._value = curve  # 将贝塞尔曲线设为当前值
        return self

    def plot_points(self, points, title):
        x, y = zip(*points)
        plt.scatter(x, y)
        plt.title(title)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()

# 创建类的实例
seed_generator = SeedGenerator()

# 生成种子点集
seed_generator.make_seed_segment()
seed_points = seed_generator._value

# 绘制种子点集
seed_generator.plot_points(seed_points, 'Seed Points')

# 创建对称种子点集
seed_generator.make_seed_symmetric()
sym_seed_points = seed_generator._value

# 绘制对称种子点集
seed_generator.plot_points(sym_seed_points, 'Symmetric Seed Points')

# 转换为贝塞尔曲线节点
seed_generator.to_nodes(seed_points)
nodes = seed_generator._value

# 绘制贝塞尔曲线节点
seed_generator.plot_points(nodes.transpose(), 'Bezier Curve Nodes')

# 转换为贝塞尔曲线
seed_generator.to_bezier_curve(seed_points)
curve = seed_generator._value

# 绘制贝塞尔曲线
curve.plot(num_pts=256, color="blue")
plt.title('Bezier Curve')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
