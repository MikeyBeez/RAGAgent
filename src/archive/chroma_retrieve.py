import os
import ollama
import chromadb

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
        n_results=1
    )

    return results['documents'][0][0]
