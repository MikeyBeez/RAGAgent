# print_db_content_paginated.py

import chromadb
from chromadb.config import Settings

def print_db_content():
    db_dir = './mydbs'  # Ensure this path is correct
    client = chromadb.Client(Settings(is_persistent=True, persist_directory=db_dir))

    collection = client.get_collection("docs")  # Replace "docs" with your actual collection name

    page_size = 100  # Number of documents to fetch per page
    offset = 0
    documents_fetched = 0

    try:
        while True:
            # Query to fetch documents in batches
            query_result = collection.query(
                query_embeddings=[],  # An empty query to match all documents
                n_results=page_size,
                offset=offset
            )
            
            if not query_result['documents']:
                break

            for idx, doc in enumerate(query_result['documents']):
                print(f"Document {documents_fetched + idx + 1}: {doc}")

            documents_fetched += len(query_result['documents'])
            offset += page_size

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_db_content()

