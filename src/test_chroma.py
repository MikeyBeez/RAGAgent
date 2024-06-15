import os
import chromadb
import ollama

# Create the embed_db directory if it doesn't exist
os.makedirs("embed_db", exist_ok=True)

# Create a ChromaDB client
chroma_client = chromadb.Client()

# Create a collection named 'prompts' if it doesn't exist
prompt_collection = chroma_client.get_or_create_collection("prompts")

# Test prompt and embedding
test_prompt = "The clock is broken."
test_embedding = ollama.embeddings(model="all-minilm", prompt=test_prompt)["embedding"]

# Store the test prompt and its embedding in the 'prompts' collection
prompt_collection.add(
    documents=[test_prompt],
    embeddings=[test_embedding],
    ids=["test_prompt"]
)

# Query prompt and embedding
query_prompt = "Why am I always late?"
print(query_prompt)
print("\n")
query_embedding = ollama.embeddings(model="all-minilm", prompt=query_prompt)["embedding"]

# Perform a similarity search and retrieve the relevant document
results = prompt_collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

# Print the retrieved document
print("Results are:")
print(results["documents"][0][0])
