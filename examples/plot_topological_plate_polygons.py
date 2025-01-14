#!/usr/bin/env python3
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, shape

from gwspy import PlateModel

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_plate_polygons.py


def main(show=True):
    model = PlateModel("Muller2019")
    time = 10
    topology_10 = model.get_topology(time)

    # LOOK HERE!!!!
    # plot polygon without edges first
    # and then get the polygon edges as lines and  plot the edges
    # this is to get rid of the vertical line along the dateline
    _polygons = topology_10.get_plate_polygons()
    _lines = topology_10.get_plate_polygons(as_lines=True)

    # print(_polygons)

    polygons = []
    for feature in _polygons["features"]:
        # if feature["properties"]["type"] != "gpml:TopologicalClosedPlateBoundary":
        #    continue
        s = shape(feature["geometry"])
        if isinstance(s, Polygon) or isinstance(s, MultiPolygon):
            polygons.append(s.buffer(0))

    lines = []
    colors = []
    feature_types = []
    for feature in _lines["features"]:
        s = shape(feature["geometry"])
        lines.append(s)
        f_type = feature["properties"]["type"]
        if f_type == "gpml:TopologicalNetwork":
            colors.append("green")
        elif f_type == "gpml:TopologicalClosedPlateBoundary":
            colors.append("blue")
        elif f_type == "gpml:TopologicalSlabBoundary":
            colors.append("yellow")
        elif f_type == "gpml:OceanicCrust":
            colors.append("orange")
        else:
            colors.append("red")

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

    # fill the polygons with grey
    ax.add_geometries(
        polygons,
        crs=ccrs.PlateCarree(),
        facecolor="grey",
        edgecolor="none",
        alpha=0.5,
    )

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
    handles, labels = ax.get_legend_handles_labels()
    unique = [
        (h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]
    ]
    legend = plt.legend(
        *zip(*unique),
        title="Feature Types",
        prop={"size": 6},
        loc="lower right",
        bbox_to_anchor=(1.1, 0.9),
    )
    plt.setp(legend.get_title(), fontsize="xx-small")
    plt.title(f"{time} Ma (Muller2019)")

    fig.text(
        0.5,
        0.03,
        "topological closed plate boundary and network",
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
