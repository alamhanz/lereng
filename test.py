from dotenv import load_dotenv

import lereng

load_dotenv()

map_maker = lereng.chrmap(level="provinsi")
df = lereng.datasample("nation_sample_population.csv")
map_maker.insert(df, metric_col="2021", area_col="Prov", path="temp_viz")

area_fun = lereng.areaname()
print(area_fun.normalize(df, area_col="Prov"))

# df = lereng.datasample("jabar_sample_data_kemiskinan.csv")
# map_maker.insert(df, metric="2023", level="kabupaten_kota", path="temp_viz")
area_llm = lereng.areadb("PROV")
print(area_llm.get_normalize("Yogyakarta"))
