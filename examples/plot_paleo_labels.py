#!/usr/bin/env python3

import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

from gwspy import coastlines, paleoearth

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_paleo_labels.py


def main(show=True):
    time = 100
    labels = paleoearth.get_paleo_labels(time=time, model="Merdith2021")
    coastlines_shapely = coastlines.get_paleo_coastlines(
        time=time, model="Merdith2021", format="shapely"
    )

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    ax.gridlines()

    ax.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="lightgrey",
        edgecolor="lightgrey",
        alpha=1,
    )

    for name, lon, lat in zip(labels["names"], labels["lons"], labels["lats"]):
        plt.text(
            lon,
            lat,
            name,
            va="baseline",
            family="monospace",
            weight="bold",
            color="red",
            transform=ccrs.PlateCarree(),
        )

    plt.plot(labels["lons"], labels["lats"], "o", transform=ccrs.PlateCarree())
    plt.title(f"{time} Ma", fontsize=20)

    if show:
        plt.show()
    else:
        output_file = f"{OUTPUT_DIR}/{Path(__file__).stem}.png"
        fig.savefig(output_file, dpi=120, bbox_inches="tight")
        print(f"Done! The {output_file} has been saved.")
        plt.close(fig)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
