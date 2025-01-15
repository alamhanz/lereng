import json
import os
import shutil

import chromadb
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from jinja2 import Environment, FileSystemLoader

PATH_ABS = os.path.dirname(os.path.abspath(__file__))
PATH_MATERIALS = os.path.join(PATH_ABS, "materials")
PATH_MAPS = os.path.join(PATH_ABS, "materials", "indonesia_maps")
PATH_SAMPLE = os.path.join(PATH_ABS, "sample")


def datasample(name):
    return pd.read_csv(os.path.join(PATH_SAMPLE, name))


def get_embedding(texts):
    # MODEL_ID = "akahana/roberta-base-indonesia"
    MODEL_ID = "facebook/fasttext-id-vectors"
    hf_token = os.getenv("hf_token")
    api_url = (
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{MODEL_ID}"
    )
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
    )
    hf_response = response.json()
    if "error" in hf_response:
        hf_response = []

    return hf_response


class chrmap:

    def __init__(self, level="provinsi"):
        # Load SHP file
        self.level = level
        self.shp_indo = {}
        for m in os.listdir(PATH_MAPS):
            lvl = m.split("-")[0].lower()
            if level == lvl:
                dtemp = gpd.read_file(os.path.join(PATH_MAPS, m))
                dtemp.columns = [c.lower() for c in dtemp.columns]
                self.shp_indo[lvl] = dtemp

        if len(self.shp_indo) == 0:
            raise ValueError("level options: `provinsi, kecamatan, kab_kota`")

    def insert(self, data, metric_col, area_col, path="temp_viz"):
        ## put the data into js
        env = Environment(loader=FileSystemLoader(PATH_MATERIALS))
        template_js = env.get_template("lereng_viz.js")
        template_html = env.get_template("lereng_viz.html")

        data["numbers"] = data[metric_col]
        data[self.level] = data[area_col]
        df_metric = data[[self.level, "numbers"]]
        df_metric = df_metric.groupby(self.level)[["numbers"]].sum().reset_index()

        # Merge SHP and DataFrame on shp_file_name
        geojson = self.shp_indo[self.level].merge(df_metric, on=self.level, how="left")

        # Show only province that matter
        geojson["area_name"] = geojson[self.level]
        if self.level != "provinsi":
            geojson["null_numbers"] = geojson["numbers"].isnull()
            df_null = geojson.groupby("kode_prov").agg(
                count_n=("null_numbers", "sum"),
                count_all=("null_numbers", "count"),
            )
            df_null["pct_n"] = df_null["count_n"] / df_null["count_all"]
            used_kode_prov = df_null[df_null["pct_n"] <= 0.005].index.tolist()

            geojson = geojson[geojson.kode_prov.isin(used_kode_prov)]

        geojson_file = os.path.join(path, "map_with_data.geojson")
        geojson.to_file(geojson_file, driver="GeoJSON")

        # Copy template as well
        for i in ["html", "js"]:
            shutil.copy(
                os.path.join(PATH_MATERIALS, f"lereng_viz.{i}"),
                os.path.join(path, f"lereng_viz.{i}"),
            )

        with open(geojson_file, "r") as f:
            geojson_data = json.load(f)

        rendered_js = template_js.render(geojson_data=json.dumps(geojson_data))
        rendered_html = template_html.render(js_content=rendered_js)
        output_html = os.path.join(path, "lereng_viz.html")
        with open(output_html, "w") as f:
            f.write(rendered_html)


class areaname:
    def __init__(self):
        self.standard = pd.read_csv(os.path.join(PATH_MATERIALS, "standard_name.csv"))
        self.area_types = ["PROVINSI", "KECAMATAN", "KAB_KOTA"]
        self.all_name = {}
        for i in self.area_types:
            self.all_name[i] = set(self.standard[i].unique())
        self.current_areas = set()

    def identify_area(self, df, area_col):
        self.current_areas = set(df[area_col].unique())
        identity = None
        n_intersect = 1
        for i in self.area_types:
            intersect = self.current_areas & self.all_name[i]
            if n_intersect < len(intersect):
                n_intersect = len(intersect)
                identity = i

        return identity.lower()

    def normalize(self, df, area_col):
        ## Identify Area
        area_type = self.identify_area(df, area_col).upper()

        ## Start AreaDB
        db_level = dict(zip(self.area_types, ["PROV", "KOTA", "KEC"]))
        area_db = areadb(level=db_level[area_type])

        ## Split Area
        known_area = self.current_areas & self.all_name[area_type]
        unknown_area = self.current_areas - self.all_name[area_type]

        all_area_dict = dict(zip(known_area, known_area))
        unknown_area_dict = {}
        for i in unknown_area:
            candidate_norm = area_db.get_normalize(i, n_results=3)
            if len(candidate_norm) == 0:
                unknown_area_dict[i] = i
            else:
                unknown_area_dict[i] = candidate_norm[0]

        all_area_dict.update(unknown_area_dict)
        df["normalized_area"] = df[area_col].apply(lambda x: all_area_dict[x])
        df["is_already_normalized"] = df[area_col].isin(known_area)
        return df


class areadb:
    def __init__(self, level):
        # Level = PROV, KOTA, KEC
        # Initialize HF API
        CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(CURRENT_PATH, "materials")
        CHROMA_PATH = os.path.join(DATA_PATH, "vdb")
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            "indo_areas", metadata={"hnsw:space": "cosine"}
        )
        self.level = level

    def get_normalize(self, area, n_results=5):
        query_vector = get_embedding(area)
        if len(query_vector) == 0:
            print("No Response")
            return []

        results = self.collection.query(
            query_embeddings=query_vector,
            n_results=n_results,
            where={"level": self.level},
        )
        # results = self.collection.get(ids=["PR34"], include=["embeddings", "documents"])
        results = results["documents"][0]
        return results
