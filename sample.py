import os

import geopandas as gpd
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))


def shapefile_sample():
    geodf = gpd.read_file(os.path.join(path, "maps", "Provinsi", "Provinsi.shp"))
    geodf["rand"] = np.random.randint(1, 100, len(geodf))
    return geodf


geodf = gpd.read_file(os.path.join(path, "maps", "Provinsi", "Provinsi.shp"))
print(geodf.sample(5)["PROVINSI"])
prov = set(geodf["PROVINSI"].unique().tolist())

geodf = gpd.read_file(os.path.join(path, "maps", "Kab_Kota", "Kab_kota.shp"))
print(geodf.sample(5)[["KAB_KOTA", "PROVINSI"]])
kab_kot = set(geodf["KAB_KOTA"].unique().tolist())
prov2 = set(geodf["PROVINSI"].unique().tolist())
print(prov2 - prov)


geodf = gpd.read_file(os.path.join(path, "maps", "Kecamatan", "Kecamatan.shp"))
print(geodf.sample(5)[["KECAMATAN", "KAB_KOTA", "PROVINSI"]])
kab_kot2 = set(geodf["KAB_KOTA"].unique().tolist())
prov3 = set(geodf["PROVINSI"].unique().tolist())
print(kab_kot2 - kab_kot)
print(prov3 - prov)
