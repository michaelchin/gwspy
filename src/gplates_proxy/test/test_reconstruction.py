from importer import *
from shapely import Point

lats = [50, 10, 50]
lons = [-100, 160, 100]

r = gplates.get_paleo_coordinates(lats, lons, 100, model="PALEOMAP")
print(r)

points = [Point(x, y) for x, y in zip(lons, lats)]
r = gplates.reconstruct_shapely_points(points, 100, model="PALEOMAP")
print(r)
