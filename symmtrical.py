import math
import numpy as np
import matplotlib.pyplot as plt

class YourClass:
    def __init__(self):
        self._radius = None
        self._angle = None
        self._keep_grid_points = None
        self._seed_points = None
        self._sym_seed_points = None
        self._symmetric = False
        self._value = None

    def make_seed_segment(self, radius_of_elements=10):
        self._radius = 20.
        self._angle = np.pi / 10

        t1 = [5 * self._radius * r * math.cos(self._angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
        t2 = [5 * self._radius * r * math.sin(self._angle) for r in np.arange(0, 1, 1 / radius_of_elements)]

        b = [(5 * self._radius * r, 0) for r in np.arange(0, 1, 1 / radius_of_elements)]

        self._seed_points = list(zip(t1, t2)) + b
        self._value = self._seed_points

        return self

    def make_seed_symmetric(self, arg=None):
        if isinstance(arg, bool) and not arg:
            return self
        self._sym_seed_points = [(x[0], -x[1]) for x in self._seed_points]
        self._symmetric = True
        self._value = self._sym_seed_points

        return self

    def plot_seed_points(self):
        # 绘制种子点
        seed_points = self._value  # 使用 _value 属性绘制，根据是否对称选择不同的点集
        x, y = zip(*seed_points)
        plt.scatter(x, y, label='Seed Points', color='blue')

        # 绘制圆
        circle = plt.Circle((0, 0), 5 * self._radius, fill=False, color='red', linestyle='dotted', label='Circle')
        plt.gca().add_patch(circle)

        # 绘制 x 轴上的点
        x_points = [point[0] for point in seed_points[len(seed_points) // 2:]]
        plt.scatter(x_points, [0] * len(x_points), label='X-axis Points', color='green')

        plt.legend()
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Seed Points and Circle')
        plt.axis('equal')  # 保持坐标轴比例相等
        plt.show()

# 创建类实例
your_instance = YourClass()
# 调用方法
your_instance.make_seed_segment().make_seed_symmetric()
# 调用绘图方法
your_instance.plot_seed_points()
