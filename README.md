# GPlates Web Service Python Client/Proxy

![build badge](https://github.com/michaelchin/gplates-python-proxy/actions/workflows/build-doc.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/gwspy.svg)](https://badge.fury.io/py/gwspy)

This Python package allows users to access [GPlates Web Service](https://gwsdoc.gplates.org/) more easily via simple Python programming interface.

### Installation

`pip install gwspy`

### How to use

The following Python code reconstructs three locations to 100Ma with Muller2019 reconstruction model.

```python
  # pip install gwspy shapely
  import shapely
  from gwspy import PlateModel, reconstruct_shapely_points

  lats = [50, 10, 50]
  lons = [-100, 160, 100]
  points = [shapely.Point(x, y) for x, y in zip(lons, lats)]

  model = PlateModel("Muller2019")
  paleo_points = reconstruct_shapely_points(model, points, 100)
  print(paleo_points)
```

### GPlates Web Service server

By default, https://gws.gplates.org is used. You can use .env file to specify your service URL. Alternertively, you can `export GWS_URL=https://your-service-url` in a terminal.

See [env.template](src/gwspy/env.template) and [setup GWS server with Docker](https://github.com/GPlates/gplates-web-service/tree/master/docker#-quick-start).

### Dependencies

- [requests](https://pypi.org/project/requests/)
- [shapely](https://pypi.org/project/shapely/)

### API reference

API reference can be found at https://michaelchin.github.io/gplates-python-proxy/.

### Examples

👉 [reconstruct_shapely_points.py](https://github.com/michaelchin/gplates-python-proxy/blob/main/examples/reconstruct_shapely_points.py)

The red dots are present-day locations. The blue dots are paleo-locations at 100Ma.

![reconstruct_shapely_points](https://raw.githubusercontent.com/michaelchin/gplates-python-proxy/main//examples/output/reconstruct_shapely_points.png)

👉 [plot_subduction_zones.py](https://github.com/michaelchin/gplates-python-proxy/blob/main/examples/plot_subduction_zones.py)

![plot_subduction_zones](https://raw.githubusercontent.com/michaelchin/gplates-python-proxy/main/examples/output/plot_subduction_zones.png)

👉 [plot_topological_plate_polygons.py](https://github.com/michaelchin/gplates-python-proxy/blob/main/examples/plot_topological_plate_polygons.py)

![plot_topological_plate_polygons](https://raw.githubusercontent.com/michaelchin/gplates-python-proxy/main/examples/output/plot_topological_plate_polygons.png)

[All Examples](https://github.com/michaelchin/gplates-python-proxy/blob/main/examples/readme.md)
