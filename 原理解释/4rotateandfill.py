import numpy as np
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
        self._figure = None
        self._axes = None

    def make_seed_segment(self, radius: float = 20., angle=np.pi / 4, radius_of_elements: int = 10, keep_grid_points=False):
        t1 = [5 * radius * r * math.cos(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
        t2 = [5 * radius * r * math.sin(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
        b = [(5 * radius * r, 0) for r in np.arange(0, 1, 1 / radius_of_elements)]

        t = list(zip(t1, t2)) + b
        self._radius = radius
        self._angle = angle
        self._keep_grid_points = keep_grid_points
        self._seed_points = random.sample(t, len(t))
        self._sym_seed_points = None
        self._symmetric = False
        self._value = self._seed_points

        return self

    def make_seed_symmetric(self, arg=None):
        if isinstance(arg, bool) and not arg:
            return self
        self._sym_seed_points = [(x[0], -x[1]) for x in self._seed_points]
        self._symmetric = True
        self._value = self._sym_seed_points
        return self

    def to_nodes(self, points):
        nodes = np.array(points).transpose()
        self._value = nodes
        return self

    def to_bezier_curve(self, points):
        nodes = np.array(points).transpose()
        curve = bezier.Curve.from_nodes(nodes)
        self._value = curve
        return self

    def rotate_and_fill(self, face_color="0.2", edge_color=None, location=111, ax=None):
        if ax is None:
            if self._figure is None:
                fig, local_ax = plt.subplots()
            else:
                fig = self._figure
                if isinstance(location, tuple):
                    local_ax = fig.add_subplot(*location)
                else:
                    local_ax = fig.add_subplot(location)
        else:
            local_ax = ax
            fig = self._figure

        alpha = self._angle
        nodes = self._seed_points

        if self._symmetric:
            alpha = 2 * alpha
            nodes = nodes + self._sym_seed_points

        nodes = np.array(nodes).transpose()

        rot_mat = [[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]]

        if face_color is None:
            local_ax.plot(nodes[0], nodes[1], color=edge_color)
        else:
            local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        for i in range(1, math.floor(2 * np.pi / alpha)):
            nodes = np.dot(rot_mat, nodes)
            if face_color is None:
                local_ax.plot(nodes[0], nodes[1], color=edge_color)
            else:
                local_ax.fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)

        local_ax.set_aspect('equal')
        local_ax.axis('off')

        self._figure = fig
        self._axes = local_ax
        self._value = local_ax

        return self

# 示例用法
seed_generator = SeedGenerator()
seed_generator.make_seed_segment()
#可以自由注释下面三行任意一行玩一玩
seed_generator.make_seed_symmetric()
seed_generator.to_nodes(seed_generator._value)
seed_generator.to_bezier_curve(seed_generator._value)
seed_generator.rotate_and_fill(face_color="0.8", edge_color="0.2", location=111)
plt.show()
