from PaperCutRun import random_papercut,multi_layer
import matplotlib.pyplot as plt
import matplotlib.cm
import random
import matplotlib.style as mplstyle
mplstyle.use('fast')

seed = 330

fig_small = plt.figure(figsize=(10, 10), dpi=120)
fig_large = plt.figure(figsize=(10, 50), dpi=120)
k = 1

display_1, display_2, display_3, default_fig, default_color = multi_layer()

for fc1 in [display_1, display_2, display_3, default_fig, default_color]:
    # 为每个 fc1 创建一个新的 Figure 对象
    fig = plt.figure(figsize=(10, 10), dpi=120)
    # 使用 random_papercut 创建图案
    random.seed(seed)
    fig = random_papercut(radius=[19, 10, 6],
                          connecting_function="bezier-fill",
                          symmetric_seed=True,
                          face_color=fc1,
                          radius_of_elements=19,
                          num_of_axis=8,
                          figure=fig,
                          location=(1, 1, 1))  # (列，行，第几个)

    # 设置图形的标题
    ax = fig.axes[-1]
    ax.set_title(str(fc1))

    # 显示图形
    plt.show()
    plt.close()
for fc1 in [display_1, display_2, display_3, default_fig, default_color]:
    random.seed(seed)
    fig_large = random_papercut(radius=[19, 10, 6],
                                connecting_function="bezier-fill",
                                symmetric_seed=True,
                                face_color=fc1,
                                radius_of_elements=19,
                                num_of_axis=8,
                                figure=fig_large,
                                location=(5, 1, k))
    ax_large = fig_large.axes[-1]
    ax_large.set_title(str(fc1))
    k += 1
plt.show()
plt.close(fig_large)
