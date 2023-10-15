#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import shapely

sys.path.insert(0, "../src/")
from common import OUTPUT_DIR

from gplates_ws_proxy import PlateModel, reconstruct_shapely_points

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./reconstruct_shapely_points.py


def main():
    lats = [50, 10, 50]
    lons = [-100, 160, 100]

    points = [shapely.Point(x, y) for x, y in zip(lons, lats)]

    model = PlateModel("Muller2019")
    paleo_points = reconstruct_shapely_points(model, points, 100)
    print(paleo_points)

    # plot the points
    crs = ccrs.Robinson(central_longitude=0.0, globe=None)
    fig = plt.figure(figsize=(12, 6), dpi=120)
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

    # plt.show()
    output_file = f"{OUTPUT_DIR}/{Path(__file__).stem}.png"
    fig.savefig(output_file)
    plt.close()
    print(f"Done! The {output_file} has been saved .")


if __name__ == "__main__":
    main()
