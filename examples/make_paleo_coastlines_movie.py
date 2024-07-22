#!/usr/bin/env python3
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import moviepy.editor as mpy

from gwspy import coastlines

OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def main():
    for time in range(0, 141, 10):
        get_basemap_with_coastlines(time=time)
        plt.title(f"{time} Ma")
        save_fig(f"paleo-coastlines-{time}-Ma.png")

    frame_list = [
        f"{OUTPUT_DIR}/paleo-coastlines-{time}-Ma.png" for time in range(0, 141, 10)
    ]
    # print(frame_list)
    clip = mpy.ImageSequenceClip(frame_list, fps=4)

    clip.write_videofile(
        f"{OUTPUT_DIR}/coastlines.mp4",
        codec="libx264",
        # audio_codec='aac',
        ffmpeg_params=["-s", "1440x720", "-pix_fmt", "yuv420p"],
    )  # LOOK HERE!!!! give image size here(the numbers must divide by 2)
    print("video has been created!")


def get_basemap_with_coastlines(model="Muller2019", crs=ccrs.Robinson(), time=140):
    coastlines_shapely = coastlines.get_paleo_coastlines(
        time=time, model=model, format="shapely", min_area=500
    )

    fig = plt.figure(figsize=(12, 6), dpi=120)
    ax = plt.axes(projection=crs)

    ax.set_global()
    ax.gridlines()

    ax.add_geometries(
        coastlines_shapely,
        crs=ccrs.PlateCarree(),
        facecolor="grey",
        edgecolor="red",
        alpha=0.5,
    )
    return ax


def save_fig(filename):
    output_file = f"{OUTPUT_DIR}/{Path(filename).stem}.png"
    plt.gcf().savefig(output_file, dpi=120, bbox_inches="tight")  # transparent=True)
    print(f"Done! The {output_file} has been saved.")
    plt.close(plt.gcf())


if __name__ == "__main__":
    main()
