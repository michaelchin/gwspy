from utils import logger

from gwspy import PlateModel, utils

model = PlateModel("Muller2019")
time = 10
topology_10 = model.get_topology(time)

logger.info(utils.get_cfg())


def test_plate_polygon_names():
    msg = []
    for name in topology_10.get_plate_polygon_names():
        msg.append(name)
    logger.info(msg)


def test_plate_boundaries_types():
    msg = []
    for type in topology_10.get_plate_boundary_types():
        msg.append(type)
    logger.info(msg)


if __name__ == "__main__":
    test_plate_polygon_names()
    test_plate_boundaries_types()
