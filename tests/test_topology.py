from utils import logger

from gplates_ws_proxy import PlateModel

model = PlateModel("Muller2019")
time = 10
topology_10 = model.get_topology(time)


def test_plate_polygon_names():
    for name in topology_10.get_plate_polygon_names():
        logger.info(name)


def test_plate_boundaries_types():
    for type in topology_10.get_plate_boundary_types():
        logger.info(type)


if __name__ == "__main__":
    test_plate_polygon_names()
    test_plate_boundaries_types()
