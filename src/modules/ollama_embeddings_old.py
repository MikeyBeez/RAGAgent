import os
import ollama
import chromadb

# Create the "mydbs" directory if it doesn't exist
db_dir = "mydbs"
os.makedirs(db_dir, exist_ok=True)

client = chromadb.PersistentClient(
    path=db_dir,
    settings=chromadb.config.Settings(),
)

def store_embeddings(prompt, response):
    collection = client.get_or_create_collection(name="docs")

    # Generate embeddings for the prompt and response
    prompt_embedding = ollama.embeddings(model="all-minilm", prompt=prompt)["embedding"]
    response_embedding = ollama.embeddings(model="all-minilm", prompt=response)["embedding"]

    # Store the prompt and response embeddings in the Chroma collection
    collection.add(
        ids=["prompt", "response"],
        embeddings=[prompt_embedding, response_embedding],
        documents=[prompt, response]
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
