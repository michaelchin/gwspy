#!/bin/bash

source ~/.init_mamba

micromamba activate gplates-ws-example

./plot_paleo_cities.py save

./reconstruct_shapely_points.py save

./plot_topological_plate_polygons.py save

./plot_topological_plate_boundaries.py save

./plot_subduction_zones.py save

./plot_topological_features.py save

./plot_paleo_labels.py save

./plot_paleo_coastlines.py save