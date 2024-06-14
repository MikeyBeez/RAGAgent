import os
import time
import random
import warnings
import ollama
from langchain_chroma import Chroma
from chromadb import PersistentClient

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="The installed version of bitsandbytes was compiled without GPU support.")

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "mydbs")

def create_db_directory():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

def generate_unique_id():
    timestamp = int(time.time())
    random_num = random.randint(0, 1000000)
    return f"{timestamp}_{random_num}"

def store_embeddings(prompt, response):
    # Skip storing embeddings if the prompt or response is empty or whitespace
    if not prompt.strip() or not response.strip():
        print("Skipping storage: Prompt or response is empty or whitespace.")
        return

    create_db_directory()

    # Generate embeddings using ollama
    prompt_embedding = ollama.embeddings(model="all-minilm", prompt=prompt)["embedding"]
    response_embedding = ollama.embeddings(model="all-minilm", prompt=response)["embedding"]

    persistent_client = PersistentClient(path=DB_DIR)
    collection = persistent_client.get_or_create_collection("chat_history")

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="chat_history",
    )

    # Generate unique IDs for the prompt and response embeddings
    prompt_id = generate_unique_id()
    response_id = generate_unique_id()

    # Store the prompt and response embeddings in the Chroma database
    langchain_chroma.add_embeddings([prompt_embedding], metadatas=[{"text": prompt, "response": response}], ids=[prompt_id])
    langchain_chroma.add_embeddings([response_embedding], metadatas=[{"text": response, "response": response}], ids=[response_id])

    print(f"Stored prompt with ID: {p

