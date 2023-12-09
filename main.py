from RandomMandala import random_mandala, figure_to_image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm
from PIL import Image, ImageOps
from mpl_toolkits.axes_grid1 import ImageGrid
import random



fig = matplotlib.pyplot.figure(figsize=(20, 20), dpi=320)
k = 1
random.seed(716)
for i in range(36):
    rs=list(range(1,random.choice([3,4,5,6])+1))
    rs.sort()
    rs.reverse()

    fig = random_mandala(connecting_function="bezier_fill",
                         color_mapper=matplotlib.cm.gist_earth,
   						 symmetric_seed=True,
                         radius=rs,
                         rotational_symmetry_order=random.choice([3,4,5,6,7]),
                         number_of_elements=random.choice([2,3,4]),
                         figure=fig,
                         location=(6, 6, k))
    ax = fig.axes[-1]
    ax.set_axis_off()
    k = k + 1

fig.tight_layout()
plt.show()
plt.close(fig)