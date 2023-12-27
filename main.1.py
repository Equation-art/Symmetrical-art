from PaperCutRun import random_papercut, multi_layer
import matplotlib.pyplot as plt
import random
import matplotlib.style as mplstyle

mplstyle.use('fast')

seed = 10747890316970060

k = 1

display_1, display_2, display_3, default_fig, default_color = multi_layer()

for fc1 in [display_1, display_2, display_3, default_fig, default_color, ["olive", "gold", "red"]]:
    # 为每个 fc1 创建一个新的 Figure 对象
    fig = plt.figure(figsize=(192, 108), dpi=10)  # x,y乘上dpi就是像素

    # 使用 random_papercut 创建图案
    random.seed(seed)
    fig = random_papercut(radius=[150, 120, 90],
                          connecting_function="bezier-fill",
                          symmetric_seed=True,
                          face_color=fc1,
                          radius_of_elements=10,#改改这个
                          num_of_axis=10,#改改这个
                          figure=fig,
                          location=(1, 1, 1))  # (列，行，第几个)

    # 设置整个 Figure 的背景色和透明度
    fig.patch.set_facecolor('orange')
    fig.patch.set_alpha(1.0)

    # 获取当前 Axes 对象
    ax = plt.gca()


    # 设置图形的标题
    #plt.title(str(fc1))

    # 隐藏坐标轴
    ax.axis('off')

    # 显示图形
    plt.show()
    # 显示图形
    plt.show()

    # 保存图形，设置dpi参数
    fig.savefig('temp{}.svg'.format(fc1), transparent=False)  # Set the dpi here

    fig.savefig('temp{}.png'.format(fc1), transparent=False)  # Set the dpi here
    # 关闭当前图形对象
    plt.close()
