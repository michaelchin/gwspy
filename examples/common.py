import sys
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

sys.path.insert(0, "../src/")


from gplates_ws_proxy import coastlines

OUTPUT_DIR = "output"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


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
