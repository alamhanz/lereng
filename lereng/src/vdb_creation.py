import os

import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("hf_token")
# model_id = "GoToCompany/gemma2-9b-cpt-sahabatai-v1-base"

# model_id = "sentence-transformers/all-MiniLM-L6-v2"
# model_id = "HIT-TMG/KaLM-embedding-multilingual-mini-instruct-v1"
# model_id = "BAAI/bge-multilingual-gemma2" ## too long
model_id = "akahana/roberta-base-indonesia"

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}


def query(texts):
    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
    )
    return response.json()


texts = [
    "Daerah Istimewa Yogyakarta",
    "DI Yogyakarta",
]

output = query(texts)
# import pandas as pd

# embeddings = pd.DataFrame(output)
# print(embeddings)
print(len(output))
a, b = output
a = np.array(a).reshape(-1)
b = np.array(a).reshape(-1)
# print(np.array(a).shape)
# print(np.array(a).reshape(-1).shape)
dist = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(dist)
print(a[:10])
print(b[:10])
