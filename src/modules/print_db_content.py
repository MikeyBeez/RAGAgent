# print_db_content.py

import chromadb
from chromadb.config import Settings

def print_db_content():
    db_dir = 'path/to/your/database'  # Ensure this path is correct
    client = chromadb.Client(Settings(is_persistent=True, persist_directory=db_dir))

    collection = client.get_collection("docs")  # Replace "docs" with your actual collection name

    try:
        # Query to fetch all documents in the collection
        query_result = collection.query(
            query_embeddings=[],  # An empty query to match all documents
            n_results=1  # Adjust this number as needed to cover all documents
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if not query_result['documents']:
        print("No documents found in the database.")
    else:
        for idx, doc in enumerate(query_result['documents']):
            print(f"Document {idx + 1}: {doc}")

if __name__ == "__main__":
    print_db_content()

