#!/usr/bin/env python3
import io
import sys

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from common import OUTPUT_DIR, save_fig

from gplates_ws_proxy import PlateModel


def main(show=True):
    fig = plt.figure(figsize=(12, 6), dpi=120)

    # plot 1
    ax1 = fig.add_subplot(221, projection=ccrs.PlateCarree())
    ax1.set_global()
    ax1.gridlines()

    model = PlateModel("Muller2022")
    coastlines_shapely = model.get_coastlines(
        time=100, extent=[-90, 90, -40, 40], min_area=10, format="shapely"
    )

    ax1.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="blue",
        edgecolor="none",
        alpha=0.5,
    )
    ax1.set_title(f"{100} Ma")

    # plot 2
    ax2 = fig.add_subplot(222, projection=ccrs.Robinson())
    ax2.set_extent([-100, 100, -50, 50], crs=ccrs.Geodetic())
    ax2.gridlines()

    model = PlateModel("Muller2022")
    coastlines_shapely = model.get_coastlines(time=10, min_area=10, format="shapely")

    ax2.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="green",
        edgecolor="none",
        alpha=0.5,
    )
    ax2.set_title(f"{10} Ma")

    # plot 3
    ax3 = fig.add_subplot(223, projection=ccrs.Mollweide())
    ax3.set_global()
    ax3.gridlines()

    model = PlateModel("Muller2022")
    coastlines_shapely = model.get_coastlines(
        time=10, min_area=70 * 1000, format="shapely"
    )

    ax3.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="green",
        edgecolor="none",
        alpha=0.5,
    )
    ax3.set_title(f"min area 70000 km2")

    # plot 4
    ax4 = fig.add_subplot(224, projection=ccrs.Robinson())
    ax4.set_global()
    ax4.gridlines()
    model = PlateModel("Muller2022")
    coastlines_png = model.get_coastlines(
        time=200, format="png", facecolor="lime", edgecolor="red"
    )
    # print(type(coastlines_png))
    data = plt.imread(io.BytesIO(coastlines_png), format="png")
    ax4.imshow(
        data, origin="upper", transform=ccrs.PlateCarree(), extent=[-180, 180, -90, 90]
    )
    ax4.set_title(f"200 Ma")

    fig.subplots_adjust(
        bottom=0.05, top=0.95, left=0.1, right=0.9, wspace=0.02, hspace=0.05
    )

    if show:
        plt.show()
    else:
        save_fig(__file__)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
