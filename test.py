import lereng

map_maker = lereng.chrmap()
df = lereng.datasample("nation_sample_population.csv")
map_maker.insert(df, metric="2020", level="provinsi", path="temp_viz")

# df = lereng.datasample("jabar_sample_data_kemiskinan.csv")
# map_maker.insert(df, metric="2023", level="kabupaten_kota")
# print(map_maker.shp_indo["provinsi"].head(4))
