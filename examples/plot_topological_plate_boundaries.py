#!/usr/bin/env python3
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, shape

from gwspy import PlateModel, coastlines

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_plate_boundaries.py

model_name = "Cao2024"


def main(show=True):
    model = PlateModel(model_name)
    time = 1000
    topology_100 = model.get_topology(time)

    _lines = topology_100.get_plate_boundaries()
    colors = []
    feature_types = []
    polylines = []
    color_map = {
        "MidOceanRidge": "red",
        "Transform": "red",
        "SubductionZone": "blue",
    }
    for feature in _lines["features"]:
        s = shape(feature["geometry"])
        polylines.append(s)
        f_type = feature["properties"]["type"]

        if f_type not in color_map:
            cc = "grey"
            feature_types.append("other")
            # cc = list(np.random.choice(range(256), size=3) / 256)
            # color_map[f_type] = cc
        else:
            feature_types.append(f_type)
            cc = color_map[f_type]
        colors.append(cc)
        # if f_type == "gpml:TopologicalNetwork":
        #    colors.append("green")

    print(set(feature_types))

    coastlines_shapely = coastlines.get_paleo_coastlines(
        time=time, model=model_name, format="shapely"
    )

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        color="black",
        alpha=0.5,
        linestyle="--",
    )
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 7, "color": "gray"}
    gl.ylabel_style = {"size": 7, "color": "gray"}

    ax.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="lightgrey",
        edgecolor="none",
        alpha=0.5,
    )

    # plot the lines
    for line, c, t in zip(polylines, colors, feature_types):
        if isinstance(line, MultiLineString):
            for g in line.geoms:
                ax.plot(
                    *g.xy, transform=ccrs.PlateCarree(), color=c, label=t, linewidth=1
                )
        else:
            ax.plot(
                *line.xy, transform=ccrs.PlateCarree(), color=c, label=t, linewidth=1
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
        bbox_to_anchor=(1.08, 0.8),
    )
    plt.setp(legend.get_title(), fontsize="xx-small")

    plt.title(f"{time} Ma ({model_name})")

    fig.text(
        0.5,
        0.03,
        "The topological plate boundaries are plotted as line segments.",
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
