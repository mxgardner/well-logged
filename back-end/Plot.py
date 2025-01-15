import io
from typing import Union

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage import measure

from blockhead.util import create_scale_space, default_synthetic, populate_interval_tree
from blockhead.visual import default_display

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

facies_colors = [
    "#F4D03F",
    "#F5B041",
    "#DC7633",
    "#6E2C00",
    "#1B4F72",
    "#2E86C1",
    "#AED6F1",
    "#A569BD",
    "#196F3D",
]


def make_facies_log_plot(logs, facies_colors):
    # make sure logs are sorted by depth
    logs = logs.sort_values(by="Depth")
    cmap_facies = colors.ListedColormap(
        facies_colors[0 : len(facies_colors)], "indexed"
    )

    ztop = logs.Depth.min()
    zbot = logs.Depth.max()

    cluster = np.repeat(np.expand_dims(logs["Facies"].values, 1), 100, 1)

    f, ax = plt.subplots(nrows=1, ncols=6, figsize=(8, 12))
    ax[0].plot(logs.GR, logs.Depth, "-g")
    ax[1].plot(logs.ILD_log10, logs.Depth, "-")
    ax[2].plot(logs.DeltaPHI, logs.Depth, "-", color="0.5")
    ax[3].plot(logs.PHIND, logs.Depth, "-", color="r")
    ax[4].plot(logs.PE, logs.Depth, "-", color="black")
    im = ax[5].imshow(
        cluster, interpolation="none", aspect="auto", cmap=cmap_facies, vmin=1, vmax=9
    )

    divider = make_axes_locatable(ax[5])
    cax = divider.append_axes("right", size="20%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label(
        (17 * " ").join(
            [" SS ", "CSiS", "FSiS", "SiSh", " MS ", " WS ", " D  ", " PS ", " BS "]
        )
    )
    cbar.set_ticks(range(0, 1))
    cbar.set_ticklabels("")

    for i in range(len(ax) - 1):
        ax[i].set_ylim(ztop, zbot)
        ax[i].invert_yaxis()
        ax[i].grid()
        ax[i].locator_params(axis="x", nbins=3)

    ax[0].set_xlabel("GR")
    ax[0].set_xlim(logs.GR.min(), logs.GR.max())
    ax[1].set_xlabel("ILD_log10")
    ax[1].set_xlim(logs.ILD_log10.min(), logs.ILD_log10.max())
    ax[2].set_xlabel("DeltaPHI")
    ax[2].set_xlim(logs.DeltaPHI.min(), logs.DeltaPHI.max())
    ax[3].set_xlabel("PHIND")
    ax[3].set_xlim(logs.PHIND.min(), logs.PHIND.max())
    ax[4].set_xlabel("PE")
    ax[4].set_xlim(logs.PE.min(), logs.PE.max())
    ax[5].set_xlabel("Facies")

    ax[1].set_yticklabels([])
    ax[2].set_yticklabels([])
    ax[3].set_yticklabels([])
    ax[4].set_yticklabels([])
    ax[5].set_yticklabels([])
    ax[5].set_xticklabels([])
    f.suptitle("Well: %s" % logs.iloc[0]["Well Name"], fontsize=14, y=0.94)
    return f


def make_scale_space_plot(log_df, column="GR"):

    values = log_df[column]

    values = values[~np.isnan(values)]

    scale_space = create_scale_space(
        values, min_scale=5, max_scale=2000, num_scales=100
    )

    contours = measure.find_contours(scale_space["second"], 0)
    interval_tree = populate_interval_tree(contours)

    fig = default_display(values, scale_space, interval_tree)
    return fig


@app.post("/plot-logs/")
async def upload_csv(file: UploadFile = File(...)):
    # Read the CSV file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # Process the data (example: generate a simple plot)
    # fig, ax = plt.subplots()
    # df.plot(ax=ax)

    fig = make_facies_log_plot(df, facies_colors)

    # Save the plot to an SVG
    svg_io = io.StringIO()
    plt.savefig(svg_io, format="svg")
    svg_io.seek(0)

    # Return the SVG image
    return Response(content=svg_io.getvalue(), media_type="image/svg+xml")


@app.post("/scale-space/")
async def scale_space(file: UploadFile = File(...)):
    # Read the CSV file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # Process the data (example: generate a simple plot)
    # fig, ax = plt.subplots()
    # df.plot(ax=ax)

    fig = make_scale_space_plot(df)

    # Save the plot to an SVG
    svg_io = io.StringIO()
    plt.savefig(svg_io, format="svg")
    svg_io.seek(0)

    # Return the SVG image
    return Response(content=svg_io.getvalue(), media_type="image/svg+xml")

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)