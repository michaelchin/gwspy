from importer import *
from shapely import Point


def test_reconstruct_points():
    lats = [50, 10, 50]
    lons = [-100, 160, 100]

    points = [Point(x, y) for x, y in zip(lons, lats)]

    model = gplates.PlateModel("Muller2019")
    paleo_points = gplates.reconstruct_shapely_points(model, points, 100)
    print(paleo_points)

    paleo_points = model.reconstruct(lats, lons, 100)
    print(paleo_points)
