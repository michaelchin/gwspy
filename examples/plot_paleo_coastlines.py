#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt
from common import OUTPUT_DIR, get_basemap_with_coastlines, save_fig


def main(show=True):
    time = 100
    get_basemap_with_coastlines(time=100)
    plt.title(f"{time} Ma")
    if show:
        plt.show()
    else:
        save_fig(__file__)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "save":
        main(show=False)
    else:
        main(show=True)
