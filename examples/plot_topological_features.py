#!/usr/bin/env python3
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import MultiLineString

from gwspy import PlateModel

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_features.py


def plot_lines(ax, lines, color="blue", label=""):
    for line in lines:
        if isinstance(line, MultiLineString):
            for g in line.geoms:
                ax.plot(
                    *g.xy,
                    transform=ccrs.PlateCarree(),
                    color=color,
                    label=label,
                    linewidth=0.7,
                )
        else:
            ax.plot(
                *line.xy,
                transform=ccrs.PlateCarree(),
                color=color,
                label=label,
                linewidth=0.7,
            )


model_name = "Cao2024"


def main(show=True):
    model = PlateModel(model_name)
    time = 1000
    topology_10 = model.get_topology(time)

    mid_ocean_ridge = topology_10.get_features("MidOceanRidge", return_format="shapely")
    transform = topology_10.get_features("Transform", return_format="shapely")
    fault = topology_10.get_features("Fault", return_format="shapely")
    subduction = topology_10.get_features("SubductionZone", return_format="shapely")

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        color="grey",
        alpha=0.5,
        linestyle="--",
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 7, "color": "gray"}
    gl.ylabel_style = {"size": 7, "color": "gray"}

    plot_lines(ax, mid_ocean_ridge, color="red", label="mid-ocean ridge")
    plot_lines(ax, transform, color="red", label="transform")
    plot_lines(ax, fault, color="orange", label="fault")
    plot_lines(ax, subduction, label="subduction zone")

    # plot the legend
    handles, labels = ax.get_legend_handles_labels()
    unique = [
        (h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]
    ]
    legend = plt.legend(
        *zip(*unique),
        title="Feature Types",
        prop={"size": 6},
        loc="lower right",
        bbox_to_anchor=(1.0, 0.9),
    )
    plt.setp(legend.get_title(), fontsize="xx-small")

    plt.title(f"{time} Ma ({model_name})")

    fig.text(
        0.5,
        0.03,
        "selected topological features",
        ha="center",
    )
    if show:
        plt.show()
    else:
        save_fig(__file__)


def save_fig(filename):
    output_file = f"{OUTPUT_DIR}/{Path(filename).stem}.png"
    plt.gcf().savefig(output_file, dpi=120, bbox_inches="tight")  # transparent=True)
    print(f"Done! The {output_file} has been saved.")
    plt.close(plt.gcf())


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
