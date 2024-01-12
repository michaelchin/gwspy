#!/usr/bin/env python3

import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from gplates_ws_proxy import coastlines, plate_model, subduction_teeth

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_subduction_zones.py


def plot_teeth(ax, lons, lats, polarity):
    teeth = subduction_teeth.get_subduction_teeth_in_degrees(
        lons,
        lats,
        base_length=2,
        spacing=1,
        height=2,
        polarity=polarity,
        central_meridian=0,
    )
    for tooth in teeth:
        x = [t["lon"] for t in tooth]
        y = [t["lat"] for t in tooth]
        # print(x)
        ax.fill(x, y, transform=ccrs.PlateCarree())


def main(show=True):
    time = 0
    model_name = "Merdith2021"

    ax = get_basemap_with_coastlines(model=model_name, time=time)

    model = plate_model.PlateModel(model_name)

    subduction_zones = model.get_subduction_zones(time)

    for feature in subduction_zones["features"]:
        geom = feature["geometry"]
        polarity = subduction_teeth.Polarity.UNKNOWN
        _polarity = feature["properties"]["polarity"]
        if _polarity.lower() == "right":
            polarity = subduction_teeth.Polarity.RIGHT
        elif _polarity.lower() == "left":
            polarity = subduction_teeth.Polarity.LEFT

        if geom["type"] == "LineString":
            lats = [lon_lat[1] for lon_lat in geom["coordinates"]]
            lons = [lon_lat[0] for lon_lat in geom["coordinates"]]
            ax.plot(lons, lats, transform=ccrs.PlateCarree())
            plot_teeth(ax, lons, lats, polarity)

        elif geom["type"] == "MultiLineString":
            for line in geom["coordinates"]:
                lats = [lon_lat[1] for lon_lat in line]
                lons = [lon_lat[0] for lon_lat in line]
                ax.plot(lons, lats, transform=ccrs.PlateCarree())
                plot_teeth(ax, lons, lats, polarity)

    plt.title(f"{time} Ma", fontsize=20)

    if show:
        plt.show()
    else:
        save_fig(__file__)


def get_basemap_with_coastlines(model="Muller2019", crs=ccrs.Robinson(), time=140):
    coastlines_shapely = coastlines.get_paleo_coastlines(
        time=time, model=model, format="shapely"
    )

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=crs)

    ax.set_global()
    ax.gridlines()

    ax.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="grey",
        edgecolor="none",
        alpha=0.5,
    )
    return ax


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
