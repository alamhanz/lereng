import sys

from dotenv import load_dotenv

sys.path.append("../lereng")
import lereng

load_dotenv()

print(lereng.__version__)

map_maker = lereng.chrmap(level="provinsi")
# df = lereng.datasample("nation_sample_population.csv")
# map_maker.insert(df, metric_col="2021", area_col="Prov", store_path="temp_viz")
df = lereng.datasample("jabar_sample_data_kemiskinan.csv")
map_maker.insert(df, metric_col="2023", area_col="KAB_KOTA", store_path="temp_viz")

area_fun = lereng.areaname()
print(area_fun.normalize(df, area_col="KAB_KOTA"))
