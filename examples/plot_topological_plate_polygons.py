#!/usr/bin/env python3
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import shapely
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, shape

from gwspy import PlateModel

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_plate_polygons.py

model_name = "cao2024"


def main(show=True):
    model = PlateModel(model_name)
    time = 140
    topology_100 = model.get_topology(time)

    # LOOK HERE!!!!
    # plot polygon without edges first
    # and then get the polygon edges as lines and  plot the edges
    # this is to get rid of the vertical line along the dateline
    _polygons = topology_100.get_plate_polygons()
    _lines = topology_100.get_plate_polygons(as_lines=True)

    pid_color_map = {}
    pids = []
    polygons = []
    fill_colors = []
    for feature in _polygons["features"]:
        # print(feature["properties"]["name"])
        if feature["properties"]["type"] != "gpml:TopologicalClosedPlateBoundary":
            continue
        s = shape(feature["geometry"])
        if isinstance(s, Polygon) or isinstance(s, MultiPolygon):
            polygons.append(s.buffer(0))
            pids.append(feature["properties"]["pid"])
            if feature["properties"]["pid"] in pid_color_map:
                fill_colors.append(pid_color_map[feature["properties"]["pid"]])
            else:
                cc = list(np.random.choice(range(256), size=3) / 256)
                pid_color_map[feature["properties"]["pid"]] = cc
                fill_colors.append(cc)

    lines = []
    colors = []
    feature_types = []
    for feature in _lines["features"]:
        s = shape(feature["geometry"])
        f_type = feature["properties"]["type"]
        if f_type != "gpml:TopologicalClosedPlateBoundary":
            continue

        lines.append(s)
        colors.append("black")
        feature_types.append(f_type)

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

    pids_to_show = [
        919,
        901,
        902,
        101,
        301,
        201,
        802,
        701,
        714,
        715,
        534,
        780,
        380,
        609,
        801,
        926,
    ]
    # fill the polygons with grey
    for p, c, pid in zip(polygons, fill_colors, pids):
        ax.add_geometries(
            [p],
            crs=ccrs.PlateCarree(),
            facecolor=c,
            edgecolor="none",
            alpha=0.5,
        )
        center = p.representative_point()
        if pid in pids_to_show:
            ax.text(center.x, center.y, pid, transform=ccrs.PlateCarree())

    # plot the lines
    for line, c, t in zip(lines, colors, feature_types):
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
    handles = []
    pid_keys = list(pid_color_map.keys())
    pid_keys.sort()
    for pc in pid_keys:
        p = mpatches.Patch(color=pid_color_map[pc], label=pc)
        handles.append(p)
    legend = plt.legend(
        handles=handles,
        title="Plate IDs",
        prop={"size": 6},
        loc="lower right",
        bbox_to_anchor=(1.1, 0.3),
    )

    plt.setp(legend.get_title(), fontsize="xx-small")
    plt.title(f"{time} Ma ({model_name})")

    fig.text(
        0.5,
        0.03,
        "The topological plate polygons are filled with random colours.",
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
