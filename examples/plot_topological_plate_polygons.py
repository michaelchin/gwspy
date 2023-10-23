import sys

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.insert(0, "../src/")
from common import OUTPUT_DIR, save_fig

from gplates_ws_proxy import PlateModel

# dev test
# export GWS_URL=http://localhost:18000/
# micromamba run -n gplates-ws-example ./plot_topological_plate_polygons.py


def main():
    model = PlateModel("Muller2019")
    time = 10
    topology_10 = model.get_topology(time)

    polygons = topology_10.get_plate_polygons(return_format="shapely")

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=ccrs.Robinson())

    ax.set_global()
    ax.gridlines()

    ax.add_geometries(
        polygons,
        crs=ccrs.PlateCarree(),
        facecolor="lightgrey",
        edgecolor="blue",
        alpha=0.5,
    )
    plt.title(f"{time} Ma")
    # plt.show()
    save_fig(__file__)


if __name__ == "__main__":
    main()
