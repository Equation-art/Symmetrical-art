from PIL import ImageOps
from mpl_toolkits.axes_grid1 import ImageGrid

from PaperCut import figure_to_image
from PaperCutRun import random_papercut,multi_layer
import matplotlib.pyplot as plt
import matplotlib.cm
import random
import matplotlib.style as mplstyle
mplstyle.use('fast')

papercut_images = []

# 创建循环
random.seed(443435345)
for i in range(64):
    # 创建一个新的 Figure 对象
    fig2 = random_papercut(n_rows=None,
                          n_columns=None,
                          radius=[8, 6, 3],
                          num_of_axis=6,
                          symmetric_seed=True,
                          connecting_function='random',
                          face_color="0.")
    fig2.tight_layout()

    # 把图形转换为图像
    papercut_images = papercut_images + [figure_to_image(fig2)]

    # 释放内存
    plt.close(fig2)

# Invert image colors
papercut_images2 = [ImageOps.invert(img) for img in papercut_images]

# 二值化
papercut_images3 = [im.convert('1') for im in papercut_images2]

# 制作网格
fig3 = plt.figure(figsize=(24., 24.))
grid = ImageGrid(fig3, 111,
                 nrows_ncols=(8, 8),
                 axes_pad=0.02,
                 )

for ax, img in zip(grid, papercut_images3):
    ax.imshow(img)
    ax.set(xticks=[], yticks=[])

plt.show()
fig3.savefig('grid.svg',transparent=True)