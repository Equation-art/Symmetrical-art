from PaperCutRun import random_papercut,multi_layer
import matplotlib.pyplot as plt
import matplotlib.cm
import random
import matplotlib.style as mplstyle
mplstyle.use('fast')

seed = 10747890316970060

# 创建大图
fig_large = plt.figure(figsize=(10, 50), dpi=120)

# 调整 k 的初始值
k = 1

# 获取多层图案的颜色配置
display_1, display_2, display_3, default_fig, default_color = multi_layer()

# 循环绘制多个图案
for fc1 in [display_1, display_2, display_3, default_fig, default_color, ["olive", "gold", "red"]]:
    # 使用 random_papercut 创建图案
    random.seed(seed)

    # 在大图中创建子图
    ax = fig_large.add_subplot(5, 1, int(k))
    ax.patch.set_facecolor('orange')
    ax.patch.set_alpha(1.0)
    ax.axis('off')  # 隐藏坐标轴

    # 绘制图案
    fig_large = random_papercut(radius=[150, 120, 90],
                                connecting_function="bezier-fill",
                                symmetric_seed=False,
                                face_color=fc1,
                                radius_of_elements=30,
                                num_of_axis=20,
                                figure=fig_large,
                                location=int(k))

    # 在大图中显示图案
    k += 1

# 显示大图
plt.show()
plt.close(fig_large)
