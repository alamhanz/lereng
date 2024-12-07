import os
import shutil

import geopandas as gpd
import pandas as pd

PATH_ABS = os.path.dirname(os.path.abspath(__file__))
PATH_MATERIALS = os.path.join(PATH_ABS, "materials")
PATH_MAPS = os.path.join(PATH_ABS, "materials", "indonesia_maps")
PATH_SAMPLE = os.path.join(PATH_ABS, "sample")


class chrmap:
    def __init__(self):
        # Load SHP file
        self.shp_indo = {}
        for m in os.listdir(PATH_MAPS):
            dtemp = gpd.read_file(os.path.join(PATH_MAPS, m))
            dtemp.columns = [c.lower() for c in dtemp.columns]
            self.shp_indo[m.split("-")[0].lower()] = dtemp

    def insert(self, data, level="provinsi", metric=None, path="temp_viz"):
        data.columns = [c.lower() for c in data.columns]
        data["numbers"] = data[metric]

        # Merge SHP and DataFrame on shp_file_name
        geojson = self.shp_indo[level].merge(
            data[[level, "numbers"]], left_on=level, right_on=level
        )
        # geojson = geojson.set_geometry("geometry")
        # bounds = geojson.total_bounds
        # min_longitude, min_latitude, max_longitude, max_latitude = bounds
        # 11 Bengkulu ()
        # 18 Jawa Timur (35)

        geojson = geojson.dropna()
        # geojson = geojson[
        #     ~(geojson.provinsi.isin(["Jawa Timur", "Maluku Utara", "Maluku"]))
        # ]
        # geojson = geojson[:10]
        print(geojson)

        geojson.to_file(os.path.join(path, "map_with_data.geojson"), driver="GeoJSON")
        print(f"save in {os.path.join(path, 'map_with_data.geojson')}")

        # Copy template as well
        for i in ["html", "js"]:
            shutil.copy(
                os.path.join(PATH_MATERIALS, f"lereng_viz.{i}"),
                os.path.join(path, f"lereng_viz.{i}"),
            )


def datasample(name):
    return pd.read_csv(os.path.join(PATH_SAMPLE, name))
