import os

import geopandas as gpd
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))


def shapefile_sample():
    geodf = gpd.read_file(os.path.join(path, "maps", "shp", "Provinsi", "Provinsi.shp"))
    geodf["rand"] = np.random.randint(1, 100, len(geodf))
    return geodf


all_levels = ["Provinsi", "Kab_Kota", "Kecamatan"]
for lvl in all_levels:
    geodf = gpd.read_file(os.path.join(path, "maps", "shp", lvl, f"{lvl}.shp"))
    print(geodf.sample(5)[lvl.upper()])

    geodf["geometry"] = geodf["geometry"].simplify(
        tolerance=0.01, preserve_topology=True
    )

    # Save to GeoJSON
    geodf.to_file(f"materials/{lvl}-light.geojson", driver="GeoJSON")
