#!/usr/bin/env python3

import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.insert(0, "../src/")
from common import OUTPUT_DIR, get_basemap_with_coastlines, save_fig

from gplates_ws_proxy import plate_model

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_subduction_zones.py


def main():
    time = 10
    model_name = "Merdith2021"

    ax = get_basemap_with_coastlines(model=model_name, time=time)

    model = plate_model.PlateModel(model_name)

    subduction_zones = model.get_subduction_zones(time)

    for feature in subduction_zones["features"]:
        geom = feature["geometry"]
        if geom["type"] == "LineString":
            lats = [lon_lat[1] for lon_lat in geom["coordinates"]]
            lons = [lon_lat[0] for lon_lat in geom["coordinates"]]
            ax.plot(lons, lats, transform=ccrs.PlateCarree())
        elif geom["type"] == "MultiLineString":
            for line in geom["coordinates"]:
                lats = [lon_lat[1] for lon_lat in line]
                lons = [lon_lat[0] for lon_lat in line]
                ax.plot(lons, lats, transform=ccrs.PlateCarree())

    plt.title(f"{time} Ma", fontsize=20)

    # plt.show()
    save_fig(__file__)


if __name__ == "__main__":
    main()
