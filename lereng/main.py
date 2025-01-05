import os
import shutil

import geopandas as gpd
import pandas as pd

PATH_ABS = os.path.dirname(os.path.abspath(__file__))
PATH_MATERIALS = os.path.join(PATH_ABS, "materials")
PATH_MAPS = os.path.join(PATH_ABS, "materials", "indonesia_maps")
PATH_SAMPLE = os.path.join(PATH_ABS, "sample")


class chrmap:

    def __init__(self, level="provinsi"):
        # Load SHP file
        self.level = level
        self.shp_indo = {}
        for m in os.listdir(PATH_MAPS):
            lvl = m.split("-")[0].lower()
            if level == lvl:
                dtemp = gpd.read_file(os.path.join(PATH_MAPS, m))
                dtemp.columns = [c.lower() for c in dtemp.columns]
                self.shp_indo[lvl] = dtemp

        if len(self.shp_indo) == 0:
            raise ValueError("level options: `provinsi, kecamatan, kabupaten_kota`")

    def insert(self, data, metric, path="temp_viz"):
        data.columns = [c.lower() for c in data.columns]
        data["numbers"] = data[metric]
        level_name = "kab_kota" if self.level == "kabupaten_kota" else self.level

        # Merge SHP and DataFrame on shp_file_name
        geojson = self.shp_indo[self.level].merge(
            data[[level_name, "numbers"]], on=level_name, how="left"
        )

        # Show only province that matter
        geojson["area_name"] = geojson[level_name]
        if self.level != "provinsi":
            geojson["null_numbers"] = geojson["numbers"].isnull()
            df_null = geojson.groupby("kode_prov").agg(
                count_n=("null_numbers", "sum"),
                count_all=("null_numbers", "count"),
            )
            df_null["pct_n"] = df_null["count_n"] / df_null["count_all"]
            used_kode_prov = df_null[df_null["pct_n"] <= 0.005].index.tolist()

            geojson = geojson[geojson.kode_prov.isin(used_kode_prov)]

        geojson.to_file(os.path.join(path, "map_with_data.geojson"), driver="GeoJSON")

        # Copy template as well
        for i in ["html", "js"]:
            shutil.copy(
                os.path.join(PATH_MATERIALS, f"lereng_viz.{i}"),
                os.path.join(path, f"lereng_viz.{i}"),
            )


def datasample(name):
    return pd.read_csv(os.path.join(PATH_SAMPLE, name))
