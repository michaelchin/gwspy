from shapely import Point
from utils import logger

import gwspy


def test_reconstruct_points():
    lats = [50, 10, 50]
    lons = [-100, 160, 100]

    points = [Point(x, y) for x, y in zip(lons, lats)]

    model = gwspy.PlateModel("Muller2019")
    paleo_points = gwspy.reconstruct_shapely_points(model, points, 100)
    print(paleo_points)

    paleo_points = model.reconstruct(lats, lons, 100)
    print(paleo_points)
