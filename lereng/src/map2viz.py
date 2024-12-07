import os

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))
lvl = "Provinsi"
geodf_shp = gpd.read_file(os.path.join(path, "maps", "shp", lvl, f"{lvl}.shp"))

region_value = {"Sulawesi Tengah": 100, "Sulawesi Selatan": 120, "Sulawesi Barat": 80}
region_list = region_value.keys()
geodf_shp2 = geodf_shp[geodf_shp.PROVINSI.isin(region_list)]

geodf_shp2["reg_value"] = geodf_shp2.PROVINSI.apply(lambda x: region_value[x])
geodf_shp2 = geodf_shp2.rename(columns={"PROVINSI": "regional_name"})
geodf_shp2.to_file("materials/map_testing.geojson", driver="GeoJSON")
print(geodf_shp2)
