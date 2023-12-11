import threading
from PaperCutRun import random_papercut, multi_layer
import matplotlib.pyplot as plt
import random

def generate_papercut(fc1, figure, location, lock):
    # 使用 random_papercut 创建图案
    fig = random_papercut(radius=[19, 10, 6],
                          connecting_function="bezier-fill",
                          symmetric_seed=True,
                          face_color=fc1,
                          radius_of_elements=19,
                          num_of_axis=8,
                          figure=figure,
                          location=location)
    with lock:
        ax = fig.axes[-1]
        ax.set_title(str(fc1))
        plt.show()
        plt.close(fig)

# 获取 multi_layer 函数的输出
display_1, display_2, display_3, default_fig, default_color = multi_layer()

# 设置种子以确保结果的一致性
random.seed(310)

# 创建一个锁，用于同步对 Matplotlib 对象的访问
lock = threading.Lock()

# 创建和启动线程
threads = []
k = 1
for fc1 in [display_1, display_2, display_3, default_fig, default_color]:
    fig = plt.figure(figsize=(50, 50), dpi=120)
    t = threading.Thread(target=generate_papercut, args=(fc1, fig, (1, 1, 1), lock))
    threads.append(t)
    t.start()
    k += 1

# 等待所有线程完成
for t in threads:
    t.join()
