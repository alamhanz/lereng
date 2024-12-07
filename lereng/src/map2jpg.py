import os

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))

all_levels = ["Provinsi", "Kab_Kota", "Kecamatan"]
for lvl in all_levels:
    # Load the shapefile
    geodf_shp = gpd.read_file(os.path.join(path, "maps", "shp", lvl, f"{lvl}.shp"))
    geodf_json = gpd.read_file(os.path.join(path, "materials", f"{lvl}-light.geojson"))

    # Select specific columns (including 'geometry')
    selected_columns = [lvl.upper(), "geometry"]
    selected_gdf_shp = geodf_shp[selected_columns]
    selected_gdf_json = geodf_json[selected_columns]

    area_choose = selected_gdf_shp.sample()[lvl.upper()].values[0]

    filtered_gdf_shp = selected_gdf_shp.query(f"{lvl.upper()} == '{area_choose}'")
    filtered_gdf_json = selected_gdf_json.query(f"{lvl.upper()} == '{area_choose}'")

    # Plot the GeoDataFrame
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    filtered_gdf_shp.plot(ax=ax1, edgecolor="k")

    fig2, ax2 = plt.subplots(figsize=(10, 10))
    filtered_gdf_json.plot(ax=ax2, edgecolor="k")

    # Customize the plot (optional)
    ax1.set_title(f"{area_choose}-shp")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")

    ax2.set_title(f"{area_choose}-json")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")

    # Save the plot as a JPG
    output_path1 = f"img/{area_choose}-shp.jpg"
    fig1.savefig(output_path1, format="jpg", dpi=300)

    output_path2 = f"img/{area_choose}-json.jpg"
    fig2.savefig(output_path2, format="jpg", dpi=300)
