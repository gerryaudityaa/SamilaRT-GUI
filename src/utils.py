import random
import math
import uuid
import os
from samila import GenerativeImage, Projection

def generate_image(seed, projection, folder_name, filename):
    gradient = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
                'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys',
                'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r',
                'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r',
                'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy',
                'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1',
                'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r']

    def f1(x, y):
        result = random.uniform(-1,1) * x**3  - math.sin(y**2) + abs(y-x)
        return result
    def f2(x, y):
        result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 9*x
        return result
    def f3(x, y):
        result = random.uniform(-1,1) * x**3  - math.sin(y**2) + abs(y-x)
        return result
    def f4(x, y):
        result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 9*x
        return result

    g1 = GenerativeImage(f1, f2)
    g2 = GenerativeImage(f3, f4)
    g1.generate(seed=seed)
    g2.generate(seed=seed)
    g1.plot(bgcolor="black", projection=projection)
    fig1 = g1.fig
    ax = fig1.get_axes()[0]
    ax.scatter(
        g1.data2,
        g1.data1,
        alpha=0.06,
        cmap=random.choice(gradient),
        c=g1.data2,
        s=0.06,
    )
    ax.scatter(
        g2.data2,
        g2.data1,
        alpha=0.06,
        cmap=random.choice(gradient),
        c=g2.data2,
        s=0.06
    )

    image_path = os.path.join(folder_name, f"{filename}.png")
    g1.save_image(file_adr=image_path, depth=2)
    return image_path

def save_config(folder_name, filename, seed, projection):
    config_file_path = os.path.join(folder_name, f"{filename}_config.txt")
    with open(config_file_path, "w") as config_file:
        config_file.write(f"Seed: {seed}\n")
        config_file.write(f"Projection: {projection}\n")