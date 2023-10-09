#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely
from cartopy.feature import ShapelyFeature
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon

sys.path.insert(0, "../../")
from gplates_proxy import PlateModel


def main():
    lats = [50, 10, 50]
    lons = [-100, 160, 100]

    points = [shapely.Point(x, y) for x, y in zip(lons, lats)]

    model = PlateModel("Muller2019")
    paleo_points = model.reconstruct(points, 100)
    print(paleo_points)

    # plot the map
    crs = ccrs.Robinson(central_longitude=0.0, globe=None)

    fig = plt.figure(figsize=(12, 8), dpi=120)
    ax = plt.axes(projection=crs)
    ax.gridlines()
    ax.set_global()
    ax.coastlines()

    for idx, p in enumerate(paleo_points):
        ax.text(p.x, p.y, str(idx) + "P", transform=ccrs.PlateCarree(), fontsize=20)

    for idx, p in enumerate(points):
        ax.text(p.x, p.y, str(idx), transform=ccrs.PlateCarree(), fontsize=20)

    ax.scatter(
        [point.x for point in paleo_points],
        [point.y for point in paleo_points],
        transform=ccrs.PlateCarree(),
    )

    ax.scatter(
        [point.x for point in points],
        [point.y for point in points],
        color="red",
        transform=ccrs.PlateCarree(),
    )

    fig.savefig(
        f"reconstruct-points.png",
        format="png",
        # bbox_inches="tight",
        dpi=96,
    )
    plt.close()


if __name__ == "__main__":
    main()
