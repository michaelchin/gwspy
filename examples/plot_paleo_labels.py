#!/usr/bin/env python3

import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
MODEL_NAME = "Merdith2021"

from gwspy import coastlines, paleoearth

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_paleo_labels.py


def plot_labels(show=True, time=100, output_file=None):
    labels = paleoearth.get_paleo_labels(time=time, model=MODEL_NAME)
    coastlines_shapely = coastlines.get_paleo_coastlines(
        time=time, model=MODEL_NAME, format="shapely"
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

    for name, lon, lat, type in zip(
        labels["names"], labels["lons"], labels["lats"], labels["types"]
    ):
        if type in ["continent"]:
            text_color = "green"
            marker = "o"
        elif type in ["craton"]:
            text_color = "red"
            marker = "s"
        elif type in ["shield"]:
            text_color = "purple"
            marker = "^"
        else:
            text_color = "blue"
            marker = "*"
        ax.text(
            lon + 2,
            lat,
            name,
            va="center_baseline",
            ha="left",
            weight="light",
            size="x-small",
            color=text_color,
            transform=ccrs.PlateCarree(),
        )
        ax.plot(
            lon,
            lat,
            marker,
            color=text_color,
            markersize=3,
            transform=ccrs.PlateCarree(),
        )

    blue_star = mlines.Line2D(
        [], [], color="blue", marker="*", linestyle="None", markersize=5, label="Oceans"
    )
    red_square = mlines.Line2D(
        [], [], color="red", marker="s", linestyle="None", markersize=5, label="Cratons"
    )
    purple_triangle = mlines.Line2D(
        [],
        [],
        color="purple",
        marker="^",
        linestyle="None",
        markersize=5,
        label="Shields",
    )
    green_circle = mlines.Line2D(
        [],
        [],
        color="green",
        marker="o",
        linestyle="None",
        markersize=5,
        label="Continents",
    )

    plt.legend(
        handles=[blue_star, red_square, green_circle, purple_triangle],
        loc="lower right",
        prop={"size": 6},
    )

    plt.title(f"{time} Ma", fontsize=20)

    if show:
        plt.show()
    else:
        if not output_file:
            output_file = f"{OUTPUT_DIR}/{Path(__file__).stem}.png"
        fig.savefig(output_file, dpi=120)
        print(f"Done! The {output_file} has been saved.")
        plt.close(fig)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        plot_labels(show=False)
    elif len(sys.argv) == 2 and sys.argv[1] == "save_all":
        Path(f"{OUTPUT_DIR}/paleo-labels").mkdir(parents=True, exist_ok=True)
        for time in range(0, 1001, 10):
            plot_labels(
                show=False,
                time=time,
                output_file=f"{OUTPUT_DIR}/paleo-labels/{MODEL_NAME}_{time}Ma.png",
            )
    else:
        plot_labels(show=True)
