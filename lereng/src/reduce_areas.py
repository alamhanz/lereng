import os

import geopandas as gpd
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

from shapely.geometry import mapping, shape


def reduce_precision(geometry, precision=7):
    """
    Reduce the precision of coordinates in a geometry.

    Args:
        geometry (shapely.geometry): The input geometry (e.g., Polygon, MultiPolygon).
        precision (int): Number of decimal places to keep.

    Returns:
        shapely.geometry: Geometry with reduced precision.
    """

    def round_coords(coords):
        """
        Round the coordinates to the specified precision.
        Handles both 2D and 3D coordinates.
        """
        return [[round(coord, precision) for coord in point] for point in coords]

    if geometry.geom_type == "Polygon":
        # Handle Polygon
        geo_json = mapping(geometry)
        geo_json["coordinates"] = [
            round_coords(ring) for ring in geo_json["coordinates"]
        ]
        return shape(geo_json)

    elif geometry.geom_type == "MultiPolygon":
        # Handle MultiPolygon
        geo_json = mapping(geometry)
        geo_json["coordinates"] = [
            [round_coords(ring) for ring in multi_polygon]
            for multi_polygon in geo_json["coordinates"]
        ]
        return shape(geo_json)

    else:
        raise TypeError(f"Unsupported geometry type: {geometry.geom_type}")


def shapefile_sample():
    # geodf = gpd.read_file(os.path.join(path, "maps", "shp", "Provinsi", "Provinsi.shp"))
    geodf = gpd.read_file(os.path.join("maps", "shp", "Provinsi", "Provinsi.shp"))
    geodf["rand"] = np.random.randint(1, 100, len(geodf))
    return geodf


all_levels = ["Provinsi", "Kab_Kota", "Kecamatan"]
all_levels_name = ["provinsi", "kabupaten_kota", "kecamatan"]

param = dict(
    Provinsi=dict(
        tolerance=0.008,
        preserve_topology=False,
    ),
    Kab_Kota=dict(
        tolerance=0.001,
        preserve_topology=True,
    ),
    Kecamatan=dict(
        tolerance=0.0006,
        preserve_topology=True,
    ),
)


all_name = dict(zip(all_levels, all_levels_name))
for lvl in all_levels:
    print(lvl)
    geodf = gpd.read_file(os.path.join("maps", "shp", lvl, f"{lvl}.shp"))
    param_level = param[lvl]
    geodf["geometry"] = geodf["geometry"].simplify(**param_level)
    geodf["geometry"] = geodf["geometry"].apply(reduce_precision)

    print(geodf.sample(5))

    # Save to GeoJSON
    geodf.to_file(
        f"lereng/materials/indonesia_maps/{all_name[lvl]}-light.geojson",
        driver="GeoJSON",
    )
