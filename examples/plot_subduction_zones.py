#!/usr/bin/env python3

import sys

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.insert(0, "../src/")
from common import OUTPUT_DIR, get_basemap_with_coastlines, save_fig

from gplates_ws_proxy import plate_model, subduction_teeth

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


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
