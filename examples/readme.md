Use the following commands to create a running environment

    `conda create --name gplates-ws-example -c conda-forge cartopy matplotlib moviepy shapely jupyter requests`

    `conda activate gplates-ws-example`

    `pip install gplates-ws-proxy`

You may use the environment.yml to create the conda env as well.

    `conda env create -f environment.yml`

### Reconstruct locations

👉 [reconstruct locations](reconstruct_shapely_points.py)

The red dots are present-day locations. The blue dots are paleo-locations at 100Ma.

![reconstruct_shapely_points](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/382818ab-3742-4660-9602-6579c39dc737)

👉 [reconstruct locations](examples/reconstruct_shapely_points.py)

The red dots are present-day locations. The blue dots are paleo-locations at 100Ma.

![reconstruct_shapely_points](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/382818ab-3742-4660-9602-6579c39dc737)

👉 [paleo-coastlines](examples/plot_paleo_coastlines.py)

![plot_paleo_coastlines](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/0b07c599-5cfd-4a0d-b528-9a278d24c79f)

👉 [subduction zones](examples/plot_subduction_zones.py)

![plot_subduction_zones](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5b491f47-38df-4dd4-80c6-ded0e17fe965)

👉[plot_topological_features](examples/plot_topological_features.py)

![plot_topological_features](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5d3a173d-e959-4fc2-9d65-8967b4b2c349)

👉[plot_topological_plate_polygons](examples/plot_topological_plate_polygons.py)

![plot_topological_plate_polygons](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/9e4de24c-78d3-4e20-8cb1-c23de970dcef)

👉[plot_topological_plate_boundaries](examples/plot_topological_plate_boundaries.py)

![plot_topological_plate_boundaries](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/81829c90-f0ae-4e0b-9b92-42f92b187ea3)

👉 [paleo-labels](examples/plot_paleo_labels.py)

![plot_paleo_labels](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5e3a1f6b-e1d7-4d9f-b2f8-967e530d3a8e)


### Plot paleo-coastlines

👉 [paleo-coastlines movie](paleo-coastlines.ipynb)

![paleo-coastlines movie](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/11113728-967a-445c-9941-7b82523138ea)

### Plot paleo-labels

👉 [paleo-labels](plot_paleo_labels.py)

![plot_paleo_labels](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5e3a1f6b-e1d7-4d9f-b2f8-967e530d3a8e)

### Plot subduction zones

👉 [plot_subduction_zones.py](plot_subduction_zones.py)

![plot_subduction_zones](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5b491f47-38df-4dd4-80c6-ded0e17fe965)

