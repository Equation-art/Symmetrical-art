from PaperCutRun import random_papercut,multi_layer
import matplotlib.pyplot as plt
import matplotlib.cm
import random

fig = matplotlib.pyplot.figure(figsize=(10, 50), dpi=120)
k = 1

display_1, display_2, display_3, default_fig, default_color = multi_layer()

for fc1 in [display_1,display_2,display_3,default_fig,default_color]:
    random.seed(310)

    fig = random_papercut(radius=[19, 10, 6],
                         connecting_function="bezier-fill",
                         symmetric_seed=True,
                         face_color=fc1,
                         radius_of_elements=19,
                         num_of_axis=8,
                         figure=fig,
                         location=(5, 1, k))#(列，行，第几个)
    ax = fig.axes[-1]
    ax.set_title(str(fc1))
    k = k + 1

plt.show()
plt.close(fig)
