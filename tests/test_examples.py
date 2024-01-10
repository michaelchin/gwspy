import sys

sys.path.insert(0, "../examples/")
import plot_paleo_coastlines
import plot_paleo_labels
import plot_subduction_zones
import plot_topological_features
import plot_topological_plate_boundaries
import plot_topological_plate_polygons
import reconstruct_shapely_points


def test():
    reconstruct_shapely_points.main(show=False)
    plot_topological_plate_polygons.main(show=False)
    plot_topological_plate_boundaries.main(show=False)
    plot_topological_features.main(show=False)
    plot_subduction_zones.main(show=False)
    plot_paleo_labels.main(show=False)
    plot_paleo_coastlines.main(show=False)
