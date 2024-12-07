import os

import geopandas as gpd
import pandas as pd

PATH_MAPS = os.path.join("materials", "indonesia_maps")


class chrmap:
    def __init__(self):
        pass

    def insert(self, data, level="provinsi"):
        # Load SHP file
        self.shp_indo = {}
        for m in os.listdir(PATH_MAPS):
            self.shp_indo[m.split("-")[0].lower()] = gpd.read_file(
                os.path.join(PATH_MAPS, m)
            )

        # Merge SHP and DataFrame on shp_file_name
        geojson = self.shp_indo["level"].merge(
            data, left_on="shp_file_name", right_on="shp_file_name"
        )

        # Export to GeoJSON
        geojson.to_file("map_with_data.geojson", driver="GeoJSON")
