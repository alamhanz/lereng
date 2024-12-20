# pip install chromadb

import chromadb
from chromadb.config import Settings

# Initialize Chroma client
client = chromadb.Client(
    Settings(
        persist_directory="chroma_db",  # Directory to store the database (set None for in-memory)
        chroma_db_impl="duckdb+parquet",
    )
)

# Create or load a collection
collection = client.get_or_create_collection("my_collection")

# Example data
vectors = [
    [0.1, 0.2, 0.3],  # Vector for the first document
    [0.4, 0.5, 0.6],  # Vector for the second document
]
metadatas = [{"text": "Example text 1"}, {"text": "Example text 2"}]
ids = ["id1", "id2"]

# Add to the collection
collection.add(embeddings=vectors, metadatas=metadatas, ids=ids)


# Query vector
query_vector = [0.1, 0.2, 0.25]

# Perform similarity search
results = collection.query(
    query_embeddings=[query_vector], n_results=2  # Number of results to retrieve
)

# Display results
for i in range(len(results["ids"][0])):
    print(f"ID: {results['ids'][0][i]}")
    print(f"Metadata: {results['metadatas'][0][i]}")
    print(f"Distance: {results['distances'][0][i]}")

client.persist()

client = chromadb.Client(
    Settings(
        persist_directory="chroma_db",  # Path to your persisted data
        chroma_db_impl="duckdb+parquet",
    )
)
collection = client.get_collection("my_collection")

collection.update(
    ids=["id1"],
    embeddings=[[0.2, 0.3, 0.4]],  # New vector
    metadatas=[{"text": "Updated text 1"}],
)

collection.delete(ids=["id1"])
