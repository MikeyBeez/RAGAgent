# chroma_retrieve.py

import os
import ollama
import chromadb

# Define the directory for the database
db_dir = './mydbs'  # Update this path as necessary

client = chromadb.PersistentClient(
    path=db_dir,
    settings=chromadb.config.Settings(),
)

def retrieve_relevant_data(query):
    collection = client.get_or_create_collection(name="docs")

    # Generate an embedding for the query
    query_embedding = ollama.embeddings(model="all-minilm", prompt=query)["embedding"]

    # Retrieve the most relevant document based on the query embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results['documents'][0][0]

