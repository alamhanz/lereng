import sys

from dotenv import load_dotenv

sys.path.append("../lereng")
import lereng

load_dotenv()

print(lereng.__version__)

choosen_area_col = "KAB_KOTA"
area_fun = lereng.areaname()

# df = lereng.datasample("nation_sample_population.csv")
df = lereng.datasample("jabar_sample_data_kemiskinan.csv")
area_type = area_fun.identify_area(df, choosen_area_col)
map_maker = lereng.chrmap(level=area_type)
df_data = area_fun.normalize(df, choosen_area_col)
print(area_fun.area_db.level)
df_data["old_" + choosen_area_col] = df_data[choosen_area_col]
df_data[choosen_area_col] = df_data["normalized_area"]

# map_maker.insert(df, metric_col="2021", area_col="Prov", store_path="temp_viz")
map_maker.insert(df_data, metric_col="2023", area_col="KAB_KOTA", store_path="temp_viz")
print(map_maker.level)

# print(area_fun.normalize(df, area_col="KAB_KOTA"))
