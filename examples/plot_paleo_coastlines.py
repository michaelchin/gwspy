#!/usr/bin/env python3
from common import OUTPUT_DIR, get_basemap_with_coastlines, save_fig


def main():
    get_basemap_with_coastlines()
    save_fig(__file__)


if __name__ == "__main__":
    main()
