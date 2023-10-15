#!/usr/bin/env python3

import matplotlib.pyplot as plt
import moviepy.editor as mpy
from common import OUTPUT_DIR, get_basemap_with_coastlines, save_fig


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


if __name__ == "__main__":
    main()
