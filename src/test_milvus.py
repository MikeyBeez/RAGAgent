import os
from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType
import ollama

# Connect to Milvus
client = MilvusClient("milvus_demo.db")

# Create a collection named 'prompts' if it doesn't exist
collection_name = "prompts"
if not client.has_collection(collection_name):
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="prompt", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
    ]
    schema = CollectionSchema(fields)
    client.create_collection(collection_name, schema=schema)

# Test prompt and embedding
test_prompt = "The clock is broken."
test_embedding = ollama.embeddings(model="all-minilm", prompt=test_prompt)["embedding"]

# Store the test prompt and its embedding in the 'prompts' collection
client.insert(collection_name=collection_name, data=[
    {"prompt": test_prompt, "embedding": test_embedding}
])

# Create index for the 'embedding' field
index = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 128}
}
client.create_index(collection_name=collection_name, field_name="embedding", index_params=index)

# Load the collection to memory before performing a search
client.load_collection(collection_name=collection_name)

# Query prompt and embedding
query_prompt = "Why am I always late?"
query_embedding = ollama.embeddings(model="all-minilm", prompt=query_prompt)["embedding"]

# Perform a similarity search and retrieve the relevant document
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = client.search(
    collection_name=collection_name,
    data=[query_embedding],
    anns_field="embedding",
    param=search_params,
    limit=1,
    output_fields=["prompt"]
)

# Print the retrieved document
print("Results are:")
print(results[0]["prompt"])
