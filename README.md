# lereng
Chrolopleth for Indonesia map.

## Introduction
Simple Package to create indonesian map given table contains Area Dimension and One Value.

## How to use it

Prepare the data which contain one area dimension and one value. Then follow the script below:
```
df = lereng.datasample("nation_sample_population.csv")
map_maker = lereng.chrmap(level="provinsi")
map_maker.insert(df, metric_col="2021", area_col="Prov", store_path="temp_viz") # The result save on "temp_viz" folder in html
map_maker.render() # render the map for notebook visualization
```

The data may have not normalized data like "sumut" or "DI Yogya". This package provide normalize function using fast-text model from Hugging Face platform. Please provide `.env` file with the following content `hf_token=xxx`. Then follow the script below:
```
area_fun = lereng.areaname()
df = lereng.datasample("nation_sample_population.csv")
df_normalized = area_fun.normalize(df, area_col="Prov")

map_maker = lereng.chrmap(level="provinsi")
map_maker.insert(df_normalized, metric_col="2021", area_col="Prov", store_path="temp_viz") # The result save on "temp_viz" folder in html
map_maker.render() # render the map for notebook visualization
```

## Sources

* https://www.indonesia-geospasial.com/2023/05/download-shapefile-batas-administrasi.html
* https://tanahair.indonesia.go.id/portal-web/unduh
* https://github.com/Alf-Anas/batas-administrasi-indonesia
* [jabar_sample source](https://jabar.bps.go.id/id/statistics-table/2/OTE5IzI=/persentase-penduduk-miskin-jawa-barat--maret-2024.html)
* [nation_sample source](https://sultra.bps.go.id/en/statistics-table/1/NDc3OCMx/population-by-province-in-indonesia--thousand---2019--2023.html)
* [embedding hf](https://huggingface.co/blog/getting-started-with-embeddings)
