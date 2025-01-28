import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely.validation import explain_validity


def geometries_check(gdf, simplify_tolerance=0.01, area_threshold=1e-6):
    """
    Cleans and validates geometries in a GeoDataFrame for rendering.

    Parameters:
        gdf (GeoDataFrame): Input GeoDataFrame with geometries to clean.
        simplify_tolerance (float): Tolerance for geometry simplification.
        area_threshold (float): Minimum area to apply simplification.

    Returns:
        GeoDataFrame: Cleaned and validated GeoDataFrame.
    """

    def ensure_closed(geom):
        """Ensure polygon paths are closed."""
        if geom.is_empty:
            return geom
        if isinstance(geom, Polygon):
            if not geom.exterior.is_closed:
                return Polygon(list(geom.exterior.coords) + [geom.exterior.coords[0]])
        return geom

    # def conditional_simplify(geom):
    #     """Simplify geometry only if it exceeds the area threshold."""
    #     if geom.area > area_threshold:
    #         return geom.simplify(simplify_tolerance)
    #     return geom

    def validate_geometry(geom):
        """Check and explain geometry validity."""
        if not geom.is_valid:
            return explain_validity(geom)
        return "Valid"

    # Ensure closed paths
    gdf["geometry"] = gdf["geometry"].apply(ensure_closed)

    # # Simplify geometries conditionally
    # gdf["geometry"] = gdf["geometry"].apply(conditional_simplify)

    # Ensure consistent ring orientation (clockwise)
    gdf["geometry"] = gdf["geometry"].apply(lambda geom: orient(geom, sign=1.0))

    # Check validity and keep only valid geometries
    gdf["validity_reason"] = gdf["geometry"].apply(validate_geometry)
    # gdf = gdf[gdf["validity_reason"] == "Valid"]

    # # Drop the validity reason column if not needed
    # gdf = gdf.drop(columns=["validity_reason"])

    return gdf
