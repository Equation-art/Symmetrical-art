import math
import numpy as np
import matplotlib.pyplot as plt

def make_seed_segment(radius_of_elements=10):
    radius = 20.
    angle = np.pi / 10

    t1 = [5 * radius * r * math.cos(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]
    t2 = [5 * radius * r * math.sin(angle) for r in np.arange(0, 1, 1 / radius_of_elements)]

    b = [(5 * radius * r, 0) for r in np.arange(0, 1, 1 / radius_of_elements)]

    t = list(zip(t1, t2)) + b

    return t

# 调用 make_seed_segment 方法生成种子点
seed_points = make_seed_segment()

# 绘制所有点的位置
x_values, y_values = zip(*seed_points)
plt.scatter(x_values, y_values, color='blue')
plt.title('Positions of Seed Points')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()
