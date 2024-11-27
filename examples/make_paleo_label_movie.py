#!/usr/bin/env python3

from pathlib import Path

import moviepy.editor as mpy
from plot_paleo_labels import plot_labels

MODEL_NAME = "Merdith2021"
OUTPUT_DIR = "paleo_label_movie"
Path(OUTPUT_DIR + "/images").mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    frame_list = []
    for time in range(0, 101, 10):
        fn = f"{OUTPUT_DIR}/images/{MODEL_NAME}_{time}Ma.png"
        plot_labels(
            show=False,
            time=time,
            output_file=fn,
        )
        frame_list.append(fn)

    frame_list.reverse()
    # print(frame_list)
    clip = mpy.ImageSequenceClip(frame_list, fps=4)

    clip.write_videofile(
        f"{OUTPUT_DIR}/paleo-labels.mp4",
        codec="libx264",
        # audio_codec='aac',
        ffmpeg_params=["-s", "1440x720", "-pix_fmt", "yuv420p"],
    )  # LOOK HERE!!!! give image size here(the numbers must divide by 2)
    print("video has been created!")
