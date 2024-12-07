import lereng

df = lereng.datasample("nation_sample_population.csv")
map_maker = lereng.chrmap()
map_maker.insert(df, metric="2020")
print("done")

# print(map_maker.shp_indo["provinsi"].head(4))
