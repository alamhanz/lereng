import lereng

map_maker = lereng.chrmap()
# df = lereng.datasample("nation_sample_population.csv")
# map_maker.insert(df, metric="2021", level="provinsi", path="temp_viz")

df = lereng.datasample("jabar_sample_data_kemiskinan.csv")
map_maker.insert(df, metric="2023", level="kabupaten_kota", path="temp_viz")
