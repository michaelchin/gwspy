#!/usr/bin/env python3
import sys

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.insert(0, "../src/")
from common import OUTPUT_DIR, save_fig
from shapely.geometry import MultiLineString

from gplates_ws_proxy import PlateModel

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
    polygons = topology_10.get_plate_polygons(return_format="shapely")
    lines = topology_10.get_plate_polygons(return_format="shapely", as_lines=True)

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    ax.gridlines()

    ax.add_geometries(
        polygons,
        crs=ccrs.PlateCarree(),
        facecolor="lightgrey",
        edgecolor="none",
        alpha=0.5,
    )

    for line in lines:
        if isinstance(line, MultiLineString):
            for g in line.geoms:
                ax.plot(*g.xy, transform=ccrs.PlateCarree(), color="blue")
        else:
            ax.plot(*line.xy, transform=ccrs.PlateCarree(), color="blue")

    plt.title(f"{time} Ma")
    if show:
        plt.show()
    else:
        save_fig(__file__)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
