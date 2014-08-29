from django.contrib.gis.geos import Polygon
from api.models import AggregateGridCell


def create_cells():

    zoom_levels = (
        # (13, 0.008333),
        # (14, 0.004167),
        (15, 0.002222),
        (16, 0.001111),
        (17, 0.000556)
    )

    bounds_min_x = 144.93
    bounds_min_y = -37.83
    bounds_max_x = 144.97
    bounds_max_y = -37.8

    for zoom in zoom_levels:

        level = zoom[0]
        i = zoom[1]

        x = bounds_min_x

        while x < bounds_max_x + i:
            y = bounds_min_y

            while y < bounds_max_y + i:
                cell = AggregateGridCell()
                cell.zoom_level = level
                cell.geom = Polygon((
                    (x, y),
                    (x, y + i),
                    (x + i, y + i),
                    (x + i, y),
                    (x, y)
                ))

                cell.save()
                y += i

            x += i