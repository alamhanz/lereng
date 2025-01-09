# pip install chromadb

import math
import os

import chromadb
import joblib
import numpy as np
import pandas as pd
import requests
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, "..", "materials")
CHROMA_PATH = os.path.join(DATA_PATH, "vdb")


def create_nested_dicts(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    df["KODE_PROV"] = "PR" + df["KODE_PROV"].astype(str)
    df["KODE_KK"] = "KK" + df["KODE_KK"].astype(str)
    df["KODE_KEC"] = "KC" + df["KODE_KEC"].astype(str)

    # Create dictionaries
    prov_dict = {row["KODE_PROV"]: row["PROVINSI"] for _, row in df.iterrows()}
    kk_dict = {row["KODE_KK"]: row["KAB_KOTA"] for _, row in df.iterrows()}
    kec_dict = {row["KODE_KEC"]: row["KECAMATAN"] for _, row in df.iterrows()}

    # Combine into a single dictionary
    result = {"PROV": prov_dict, "KOTA": kk_dict, "KEC": kec_dict}
    return result


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
    return hf_response


# Get The Standard Name
# -- cleaned up "--"
# areas_name = create_nested_dicts(os.path.join(DATA_PATH, "standard_name.csv"))
# joblib.dump(areas_name, os.path.join(DATA_PATH, "standard_name.pkl"))
areas_name = joblib.load(os.path.join(DATA_PATH, "standard_name.pkl"))

# Initialize Chroma client
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    "indo_areas", metadata={"hnsw:space": "cosine"}
)

# Creation
level = "KEC"  # PROV, KOTA, KEC
n_areas = len(areas_name[level])
JSON_LIMIT = 30

if n_areas >= JSON_LIMIT:
    k = math.ceil(n_areas / JSON_LIMIT)
    for i in range(15, k):
        print(i)
        area_text = list(areas_name[level].values())[
            i * JSON_LIMIT : (i + 1) * JSON_LIMIT
        ]
        area_ids = list(areas_name[level].keys())[i * JSON_LIMIT : (i + 1) * JSON_LIMIT]

        vv = [get_embedding(i) for i in area_text]
        metadatas = [{"level": level} for i in area_text]
        try:
            print(np.array(vv).shape)

            # Add to collections
            collection.upsert(
                documents=area_text, embeddings=vv, metadatas=metadatas, ids=area_ids
            )
        except:
            print("fail")
            print([len(i) for i in vv])
