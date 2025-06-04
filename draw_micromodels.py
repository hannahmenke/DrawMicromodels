import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.backends.backend_agg import FigureCanvasAgg
import h5py


def generate_offset_grid(x_dim, y_dim, stride, offset, x_dev=0, y_dev=0,
                          rad=6, rad_dev=0):
    """Generate coordinates for an offset grid of circles using NumPy."""
    rows = np.arange(0, x_dim + offset, stride)
    cols = np.arange(0, y_dim + offset, stride)
    coords = []

    for idx, j in enumerate(rows):
        if idx % 2 == 0:
            xs1 = j + np.random.randint(-x_dev, x_dev + 1, size=cols.shape)
            ys1 = cols + np.random.randint(-y_dev, y_dev + 1, size=cols.shape)
            xs2 = j + np.random.randint(-x_dev, x_dev + 1, size=cols.shape)
            ys2 = cols + stride + np.random.randint(-y_dev, y_dev + 1, size=cols.shape)
        else:
            xs1 = j + offset + np.random.randint(-x_dev, x_dev + 1, size=cols.shape)
            ys1 = cols + offset + np.random.randint(-y_dev, y_dev + 1, size=cols.shape)
            xs2 = j - offset + np.random.randint(-x_dev, x_dev + 1, size=cols.shape)
            ys2 = cols - offset + np.random.randint(-y_dev, y_dev + 1, size=cols.shape)

        xs = np.concatenate([xs1, xs2])
        ys = np.concatenate([ys1, ys2])
        rs = rad + np.random.randint(-rad_dev, rad_dev + 1, size=xs.shape)
        coords.append(np.stack([xs, ys, rs], axis=1))

    grid = np.concatenate(coords, axis=0)
    return grid[:, 0], grid[:, 1], grid[:, 2]


def draw_circles(x, y, r, x_dim, y_dim):
    """Render circles into a binary numpy array and compute porosity."""
    fig, ax = plt.subplots()
    ax.set_xlim((0, x_dim))
    ax.set_ylim((0, y_dim))
    ax.set_aspect("equal")
    ax.axis("off")

    for xi, yi, ri in zip(x, y, r):
        circle = patch.Circle((xi, yi), ri, color="black", fill=True, linewidth=0)
        ax.add_artist(circle)

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    width, height = canvas.get_width_height()
    img = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape((height, width, 3))
    binary = (img[:, :, 0] == 0).astype(np.uint8)
    porosity = binary.mean()
    plt.close(fig)
    return binary, porosity


def save_to_hdf5(filename, x, y, r, binary, metadata):
    """Write coordinates and image data to an HDF5 file."""
    with h5py.File(filename, "w") as g:
        g.create_dataset("x_coor", data=x * 10, dtype="float", compression="gzip")
        g.create_dataset("y_coor", data=y * 10, dtype="float", compression="gzip")
        g.create_dataset("rad", data=r * 10, dtype="uint16", compression="gzip")
        g.create_dataset("binary_image", data=binary, dtype="uint8", compression="gzip")
        for key, value in metadata.items():
            g.attrs[key] = value


def main():
    rad = 6
    stride = 20
    offset = 10
    x_dim = 2400
    y_dim = 2400
    x_dev = 6
    y_dev = 6
    rad_dev = 3

    x, y, r = generate_offset_grid(x_dim, y_dim, stride, offset,
                                   x_dev=x_dev, y_dev=y_dev,
                                   rad=rad, rad_dev=rad_dev)

    binary, porosity = draw_circles(x, y, r, x_dim, y_dim)

    metadata = {
        "porosity": porosity,
        "rad": rad * 10,
        "stride": stride * 10,
        "offset": offset * 10,
        "xdevmax": x_dev * 10,
        "ydevmax": y_dev * 10,
        "raddevmax": rad_dev * 10,
    }
    output_file = os.path.join(os.getcwd(), "image_output.hdf5")
    save_to_hdf5(output_file, x, y, r, binary, metadata)


if __name__ == "__main__":
    main()
