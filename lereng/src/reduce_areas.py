import os

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry.polygon import orient

path = os.path.dirname(os.path.abspath(__file__))

from shapely.geometry import MultiPolygon, Polygon, mapping, shape

from .geovalid import geometries_check

pd.options.mode.chained_assignment = None


def validate_geometry(geom):
    """Check and explain geometry validity."""
    return geom.is_valid


def is_closed(geom):
    if geom.geom_type == "Polygon":
        # Check if the Polygon's exterior is closed
        return geom.is_valid and geom.exterior.coords[0] == geom.exterior.coords[-1]
    elif geom.geom_type == "MultiPolygon":
        # Check if all individual Polygons in the MultiPolygon are closed
        return all(
            polygon.exterior.coords[0] == polygon.exterior.coords[-1]
            for polygon in geom.geoms
        )
    return False


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
# all_levels = ["Provinsi"]
all_levels_name = ["provinsi", "kabupaten_kota", "kecamatan"]

param = dict(
    Provinsi=dict(
        tolerance=0.005,
        preserve_topology=False,
    ),
    Kab_Kota=dict(
        tolerance=0.005,
        preserve_topology=True,
    ),
    Kecamatan=dict(
        tolerance=0.005,
        preserve_topology=True,
    ),
)


all_name = dict(zip(all_levels, all_levels_name))
for lvl in all_levels:
    print(lvl)
    geodf = gpd.read_file(os.path.join("maps", "shp", lvl, f"{lvl}.shp"))
    param_level = param[lvl]

    geodf["original_geometry"] = geodf["geometry"].copy()

    geodf["geometry"] = geodf["original_geometry"].simplify(**param_level)

    # geodf["area_difference"] = (
    #     geodf["original_geometry"].geometry.area - geodf["geometry"].area
    # )
    geodf["is_closed"] = geodf["geometry"].apply(is_closed)
    print(geodf["is_closed"].mean())
    geodf = geodf.to_crs(epsg=4326)

    # all_geodf = []
    # for prov in geodf.KODE_PROV.unique():
    #     geodf_temp = geodf[geodf.KODE_PROV == prov]
    #     tol = 0.0001
    #     valid_pct = 1
    #     while (valid_pct <= 0.0075) & (tol <= 0.2):
    #         tol += 0.0001
    #         param_level["tolerance"] = tol
    #         geodf_temp.loc[:, "geometry"] = geodf_temp["geometry"].simplify(
    #             **param_level
    #         )
    #         # geodf_temp.loc[:, "is_valid"] = geodf_temp["geometry"].apply(
    #         #     validate_geometry
    #         # )
    #         # valid_pct = geodf_temp["is_valid"].mean()
    #         geodf_temp.loc[:, "hausdorff_distance"] = geodf_temp.geometry.apply(
    #             lambda x: x.hausdorff_distance(x.simplify(tol))
    #         )

    #     print(prov, ":", tol - 0.0001)
    #     all_geodf.append(geodf_temp)
    # geodf = pd.concat(all_geodf)

    # geodf["geometry"] = geodf["geometry"].apply(
    #     lambda x: reduce_precision(x, precision=7)
    # )

    del geodf["original_geometry"]
    # Save to GeoJSON
    geodf.to_file(
        f"lereng/materials/indonesia_maps/{all_name[lvl]}-light.geojson",
        driver="GeoJSON",
    )

    geodf["is_valid"] = geodf["geometry"].apply(validate_geometry)
    print(geodf.head(5))
