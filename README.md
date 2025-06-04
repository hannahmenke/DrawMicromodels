# DrawMicromodels

This repository generates micromodel images of circles arranged on an offset grid.

The new `draw_micromodels.py` script extracts the logic from the original
notebook and refactors it for clarity and efficiency. It demonstrates
how to build the circle grid using NumPy, renders the figure without
writing an image to disk, computes porosity directly from the figure
canvas, and stores everything in a compressed HDF5 file using context
managers.

Before running the script, install the dependencies with the setup
script:

```bash
./setup.sh
```

Then run the program with Python 3:

```bash
python3 draw_micromodels.py
```
