import os

import geopandas as gpd
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))


def shapefile_sample():
    geodf = gpd.read_file(os.path.join(path, "maps", "Provinsi", "Provinsi.shp"))
    geodf["rand"] = np.random.randint(1, 100, len(geodf))
    return geodf


def keep_first(geo):
    if geo.geom_type == "Polygon":
        return geo
    elif geo.geom_type == "MultiPolygon":
        return geo.geoms[0]


geodf = gpd.read_file(os.path.join(path, "maps", "Provinsi", "Provinsi.shp"))
print(geodf.sample(5)["PROVINSI"])
prov = set(geodf["PROVINSI"].unique().tolist())

geodf = gpd.read_file(os.path.join(path, "maps", "Kab_Kota", "Kab_kota.shp"))
# print(geodf.sample(5)[["KAB_KOTA", "PROVINSI"]])
kab_kot = set(geodf["KAB_KOTA"].unique().tolist())
prov2 = set(geodf["PROVINSI"].unique().tolist())
# print(prov2 - prov)


geodf = gpd.read_file(os.path.join(path, "maps", "Kecamatan", "Kecamatan.shp"))
# print(geodf.sample(5)[["KECAMATAN", "KAB_KOTA", "PROVINSI"]])
geodf["geometry2"] = geodf.geometry.apply(lambda _geo: keep_first(_geo))
geodf["geometry2"] = geodf.geometry2.centroid
geodf["longitude"] = geodf.geometry2.x
geodf["latitude"] = geodf.geometry2.y

print(geodf[["KECAMATAN", "KAB_KOTA", "PROVINSI", "longitude", "latitude"]].sample(15))

kab_kot2 = set(geodf["KAB_KOTA"].unique().tolist())
prov3 = set(geodf["PROVINSI"].unique().tolist())
# print(kab_kot2 - kab_kot)
# print(prov3 - prov)

# print(geodf.query("KAB_KOTA == 'Pahuwato'"))
# del geodf["geometry"]
# geodf.to_csv("maps/name/standard_name.csv")
geodf[["KECAMATAN", "KAB_KOTA", "PROVINSI", "longitude", "latitude"]].to_csv(
    "for_bubu.csv"
)
