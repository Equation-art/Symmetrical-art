from PaperCutRun import random_papercut
import matplotlib.pyplot as plt
import matplotlib.cm
import random

fig = matplotlib.pyplot.figure(figsize=(10, 10), dpi=120)

k = 1

a = "0.0"
b = "1.0"
c = ["0.8", "0.6", "0.2"]
d= ["olive", "gold", "red"]
for fc1 in [[b, b, a],[b, a, b],[a, b, b],c,d]:
    random.seed(310)

    fig = random_papercut(radius=[19, 10, 6],
                         connecting_function="bezier_fill",
                         symmetric_seed=True,
                         face_color=fc1,
                         radius_of_elements=190,
                         num_of_axis=8,
                         figure=fig,
                         location=(2, 3, k))
    ax = fig.axes[-1]
    ax.set_title(str(fc1))
    k = k + 1

plt.show()
plt.close(fig)
