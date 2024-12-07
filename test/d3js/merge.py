import json

import geopandas as gpd
import pandas as pd

# Load SHP file
shp = gpd.read_file("your_map.shp")

# Example DataFrame with numbers
df = pd.DataFrame(
    {"shp_file_name": ["Region1", "Region2", "Region3"], "numbers": [10, 50, 100]}
)

# Merge SHP and DataFrame on shp_file_name
geojson = shp.merge(df, left_on="shp_file_name", right_on="shp_file_name")

# Export to GeoJSON
geojson.to_file("map_with_data.geojson", driver="GeoJSON")
