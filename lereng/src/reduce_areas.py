import os

import geopandas as gpd
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))


def shapefile_sample():
    # geodf = gpd.read_file(os.path.join(path, "maps", "shp", "Provinsi", "Provinsi.shp"))
    geodf = gpd.read_file(os.path.join("maps", "shp", "Provinsi", "Provinsi.shp"))
    geodf["rand"] = np.random.randint(1, 100, len(geodf))
    return geodf


all_levels = ["Provinsi", "Kab_Kota", "Kecamatan"]
all_levels_name = ["provinsi", "kabupaten_kota", "kecamatan"]
all_name = dict(zip(all_levels, all_levels_name))
for lvl in all_levels:
    geodf = gpd.read_file(os.path.join("maps", lvl, f"{lvl}.shp"))
    geodf["geometry"] = geodf["geometry"].simplify(
        # tolerance=0.001, preserve_topology=True
        tolerance=0.001,
        preserve_topology=True,
    )

    # Save to GeoJSON
    geodf.to_file(
        f"lereng/materials/indonesia_maps/{all_name[lvl]}-light.geojson",
        driver="GeoJSON",
    )
