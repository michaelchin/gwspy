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
# micromamba run -n gplates-ws-example ./plot_topological_features.py


def plot_lines(ax, lines, color="blue"):
    for line in lines:
        if isinstance(line, MultiLineString):
            for g in line.geoms:
                ax.plot(*g.xy, transform=ccrs.PlateCarree(), color=color)
        else:
            ax.plot(*line.xy, transform=ccrs.PlateCarree(), color=color)


def main(show=True):
    model = PlateModel("Muller2019")
    time = 10
    topology_10 = model.get_topology(time)

    mid_ccean_ridge = topology_10.get_features("MidOceanRidge", return_format="shapely")
    transform = topology_10.get_features("Transform", return_format="shapely")
    fault = topology_10.get_features("Fault", return_format="shapely")
    subduction = topology_10.get_features("SubductionZone", return_format="shapely")

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    ax.gridlines()

    plot_lines(ax, mid_ccean_ridge, color="red")
    plot_lines(ax, transform, color="black")
    plot_lines(ax, fault, color="yellow")
    plot_lines(ax, subduction)

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
