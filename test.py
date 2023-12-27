import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def twig_seed(radius, angle, n=5, shift_offset=0.3, shift_factor=1 / 3, shift_range=(0.5, 2), inversions=2):
    ps = np.column_stack([np.cos(np.linspace(0, 2 * np.pi, n + 1)[:-1]), np.sin(np.linspace(0, 2 * np.pi, n + 1)[:-1])])
    ps = np.random.uniform(0.95, 1.05, size=ps.shape) * ps
    ps2 = ps * np.array([np.cos(angle), np.sin(angle)])
    fs = np.sort(
        np.linalg.norm(ps2 - ps, axis=1) * shift_offset + shift_factor * np.random.uniform(*shift_range, size=n))

    if isinstance(inversions, int):
        for _ in range(inversions):
            inds = np.random.choice(range(len(fs)), 2)
            fs[inds] = fs[inds[::-1]]
    elif inversions in ['Random', 'RandomSample']:
        np.random.shuffle(fs)
    elif inversions in ['Reverse', 'ReverseSort']:
        fs = np.sort(fs)[::-1]

    t = np.column_stack([(1 - ps[:, 0]), ps[:, 1]])
    t = np.column_stack([t, (1 - ps2[:, 0]), ps2[:, 1]])
    t = np.column_stack([t, fs])

    lines = [((t[i, 0], t[i, 1]), (t[i, 2], t[i, 3])) for i in range(n)]
    lines.append(((0, 0), (1, 0)))

    return lines


def snowflake(blur=True, effect=True):
    fig, ax = plt.subplots(figsize=(4, 4))
    lines = twig_seed(1, np.random.uniform(0, 2 * np.pi), n=np.random.randint(4, 12))

    patches = [Polygon(line, closed=None, edgecolor='black', linewidth=2) for line in lines]
    collection = PatchCollection(patches)
    ax.add_collection(collection)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    if blur:
        fig.canvas.draw()
        img = np.asarray(fig.canvas.renderer.buffer_rgba())
        img = np.mean(img[:, :, :3], axis=2)
        img = plt.imshow(img, cmap='gray', extent=(ax.get_xlim() + ax.get_ylim()))
        img.set_alpha(0.5)

    if effect:
        fig.canvas.draw()
        img = np.asarray(fig.canvas.renderer.buffer_rgba())
        img = np.mean(img[:, :, :3], axis=2)
        img = plt.imshow(img, cmap='gray', extent=(ax.get_xlim() + ax.get_ylim()))
        img.set_alpha(0.5)

    plt.close(fig)
    return fig

# Use Agg backend for non-interactive use
plt.switch_backend('Agg')

# Example usage:
np.random.seed(11)
figs = [snowflake(blur=True, effect=False) for _ in range(40)]
plt.figure(figsize=(16, 10))
for i, fig in enumerate(figs, start=1):
    plt.subplot(5, 8, i)
    plt.imshow(fig.canvas.renderer.buffer_rgba(), cmap='gray', extent=(plt.gca().get_xlim() + plt.gca().get_ylim()))
    plt.axis('off')

plt.tight_layout()
plt.savefig('snowflakes.png')  # Save the figure to 'snowflakes.png'

