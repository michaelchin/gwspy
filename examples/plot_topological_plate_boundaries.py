#!/usr/bin/env python3
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, shape

from gwspy import PlateModel

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_plate_boundaries.py


def main(show=True):
    model = PlateModel("Muller2019")
    time = 10
    topology_10 = model.get_topology(time)

    _lines = topology_10.get_plate_boundaries()
    colors = []
    feature_types = []
    polylines = []
    color_map = {}
    for feature in _lines["features"]:
        s = shape(feature["geometry"])
        polylines.append(s)
        f_type = feature["properties"]["type"]
        feature_types.append(f_type)
        if f_type not in color_map:
            cc = list(np.random.choice(range(256), size=3) / 256)
            color_map[f_type] = cc
        else:
            cc = color_map[f_type]
        colors.append(cc)
        # if f_type == "gpml:TopologicalNetwork":
        #    colors.append("green")

    print(set(feature_types))

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

    # plot the lines
    for line, c, t in zip(polylines, colors, feature_types):
        if isinstance(line, MultiLineString):
            for g in line.geoms:
                ax.plot(
                    *g.xy, transform=ccrs.PlateCarree(), color=c, label=t, linewidth=0.7
                )
        else:
            ax.plot(
                *line.xy, transform=ccrs.PlateCarree(), color=c, label=t, linewidth=0.7
            )
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
        bbox_to_anchor=(1.14, 0.6),
    )
    plt.setp(legend.get_title(), fontsize="xx-small")

    plt.title(f"{time} Ma (Muller2019)")

    fig.text(
        0.5,
        0.03,
        "topological plate boundaries with random colours for each feature type",
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
