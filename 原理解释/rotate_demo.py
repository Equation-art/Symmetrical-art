import numpy as np
import matplotlib.pyplot as plt
import math


def rotate_and_fill_demo(seed_points, symmetric_seed_points, rotation_count=1, face_color="0.8", edge_color="0.2"):
    fig, axs = plt.subplots(1, rotation_count + 1, figsize=(5 * (rotation_count + 1), 5))

    axs[0].scatter(*zip(*seed_points), color=edge_color)
    axs[0].set_title("Original")

    nodes = np.array(seed_points).transpose()

    alpha = 0  # 初始化累积旋转角度

    for i in range(1, rotation_count + 1):
        alpha += np.pi / 4  # 累积旋转角度
        rot_mat = np.array([[math.cos(alpha), -math.sin(alpha)], [math.sin(alpha), math.cos(alpha)]])
        nodes = np.dot(rot_mat, nodes)
        axs[i].fill(nodes[0], nodes[1], fc=face_color, ec=edge_color)
        axs[i].set_title(f"Rotation {i}")

    plt.show()


# 示例用法
radius = 20.
angle = np.pi / 4
radius_of_elements = 10

t1 = [5 * radius * r * math.cos(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
t2 = [5 * radius * r * math.sin(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
b = [(5 * radius * r, 0) for r in np.arange(0, 1, 1 / radius_of_elements)]

seed_points = list(zip(t1, t2)) + b
symmetric_seed_points = [(x[0], -x[1]) for x in seed_points]

rotate_and_fill_demo(seed_points, symmetric_seed_points, rotation_count=3)
