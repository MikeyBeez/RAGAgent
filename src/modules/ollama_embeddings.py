# ollama_embeddings.py

import os
import json
import numpy as np
from numpy.linalg import norm
import ollama
from datetime import datetime
from typing import List, Tuple, Dict, Any
import logging

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Get the project root directory (assuming it's two levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# Set the memories directory relative to the project root
memories_dir = os.path.join(project_root, "memories")

def read_file(filename: str) -> Dict[str, Any]:
    """Read a JSON file and return its contents."""
    with open(os.path.join(memories_dir, filename), encoding="utf-8") as f:
        data = json.load(f)
        logging.debug(f"Read file: {filename}")
        return data

def save_embeddings(filename: str, embeddings: List[float]) -> None:
    """Save embeddings to a JSON file."""
    embeddings_dir = os.path.join(memories_dir, "embeddings")
    os.makedirs(embeddings_dir, exist_ok=True)
    with open(os.path.join(embeddings_dir, f"{filename}.json"), "w") as f:
        json.dump(embeddings, f)
    logging.info(f"Saved embeddings for file: {filename}")

def load_embeddings(filename: str) -> List[float]:
    """Load embeddings from a JSON file."""
    embeddings_file = os.path.join(memories_dir, "embeddings", f"{filename}.json")
    if not os.path.exists(embeddings_file):
        logging.debug(f"No existing embeddings found for file: {filename}")
        return []
    with open(embeddings_file, "r") as f:
        embeddings = json.load(f)
        logging.debug(f"Loaded existing embeddings for file: {filename}")
        return embeddings

def get_embeddings(filename: str, modelname: str) -> List[float]:
    """Get embeddings for a file, either from cache or by generating new ones."""
    if embeddings := load_embeddings(filename):
        return embeddings
    memory_data = read_file(filename)
    combined_text = memory_data.get("user", "") + "\n" + memory_data.get("agent", "") + "\n" + memory_data.get("search_results", "")
    embeddings = ollama.embeddings(model=modelname, prompt=combined_text)["embedding"]
    save_embeddings(filename, embeddings)
    logging.info(f"Generated new embeddings for file: {filename}")
    return embeddings

def find_most_similar(needle: List[float], haystack: List[List[float]]) -> List[Tuple[float, int]]:
    """Find cosine similarity of every file to a given embedding."""
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def search_memories(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search memories and return the top_k most relevant ones with metadata."""
    logging.info(f"Searching memories for query: {query}")
    memory_files = [f for f in os.listdir(memories_dir) if f.endswith(".json") and not f.startswith("embeddings_")]
    embeddings = [get_embeddings(f, "nomic-embed-text") for f in memory_files]
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    most_similar_files = find_most_similar(query_embedding, embeddings)[:top_k]
    
    relevant_memories = []
    for similarity, index in most_similar_files:
        filename = memory_files[index]
        memory_data = read_file(filename)
        
        # Update access count and last accessed time
        memory_data['metadata']['access_count'] = memory_data['metadata'].get('access_count', 0) + 1
        memory_data['metadata']['last_accessed'] = datetime.now().isoformat()
        
        # Save updated metadata
        with open(os.path.join(memories_dir, filename), 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        relevant_memories.append({
            "user": memory_data.get("user", ""),
            "agent": memory_data.get("agent", ""),
            "search_results": memory_data.get("search_results", ""),
            "similarity": similarity,
            "metadata": memory_data['metadata']
        })
        logging.debug(f"Found relevant memory: {filename} (similarity: {similarity:.4f})")
    
    logging.info(f"Found {len(relevant_memories)} relevant memories")
    return relevant_memories

def add_memory(user_input: str, agent_response: str, search_results: str = "") -> None:
    """Add a new memory to the system."""
    timestamp = datetime.now().isoformat()
    filename = f"{timestamp.replace(':', '_')}.json"
    memory_data = {
        "user": user_input,
        "agent": agent_response,
        "search_results": search_results,
        "metadata": {
            "creation_time": timestamp,
            "access_count": 0,
            "last_accessed": timestamp
        }
    }
    with open(os.path.join(memories_dir, filename), 'w') as f:
        json.dump(memory_data, f, indent=2)
    
    # Generate and save embedding
    get_embeddings(filename, "nomic-embed-text")
    logging.info(f"Added new memory: {filename}")
