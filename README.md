# GPlates Web Service Python Client/Proxy

![build badge](https://github.com/michaelchin/gplates-python-proxy/actions/workflows/build-doc.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/gplates-ws-proxy.svg)](https://badge.fury.io/py/gplates-ws-proxy)

This Python package allows users to access [GPlates Web Service](https://gwsdoc.gplates.org/) more easily via simple Python programming interface.

### Installation

`pip install gplates-ws-proxy`

### How to use

The following Python code reconstructs three locations to 100Ma with Muller2019 reconstruction model.

```python
  # pip install gplates-ws-proxy shapely
  import shapely
  from gplates_ws_proxy import PlateModel, reconstruct_shapely_points

  lats = [50, 10, 50]
  lons = [-100, 160, 100]
  points = [shapely.Point(x, y) for x, y in zip(lons, lats)]

  model = PlateModel("Muller2019")
  paleo_points = reconstruct_shapely_points(model, points, 100)
  print(paleo_points)
```

### GPlates Web Service server

By default, https://gws.gplates.org is used. You can use .env file to specify your service URL. Alternertively, you can `export GWS_URL=https://your-service-url` in a terminal.

See [env.template](src/gplates_ws_proxy/env.template) and [setup GWS server with Docker](https://github.com/GPlates/gplates-web-service/tree/master/docker#-quick-start).

### Dependencies

- [requests](https://pypi.org/project/requests/)
- [shapely](https://pypi.org/project/shapely/)

### API reference

API reference can be found at https://michaelchin.github.io/gplates-python-proxy/.

### Examples

👉 [paleo-coastlines movie](examples/paleo-coastlines.ipynb)

![paleo-coastlines movie](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/11113728-967a-445c-9941-7b82523138ea)

👉 [paleo-labels](examples/plot_paleo_labels.py)

![plot_paleo_labels](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5e3a1f6b-e1d7-4d9f-b2f8-967e530d3a8e)

👉 [subduction zones](examples/plot_subduction_zones.py)

![plot_subduction_zones](https://github.com/michaelchin/gplates-python-proxy/assets/2688316/5b491f47-38df-4dd4-80c6-ded0e17fe965)

[All Examples](examples/readme.md)
