import sys

sys.path.insert(0, "../examples/")
import reconstruct_shapely_points


def test():
    reconstruct_shapely_points.main(show=False)
