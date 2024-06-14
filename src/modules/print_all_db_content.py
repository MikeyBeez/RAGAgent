# print_db_content.py

import chromadb
from chromadb.config import Settings

def print_db_content():
    db_dir = 'path/to/your/database'  # Ensure this path is correct
    client = chromadb.Client(Settings(is_persistent=True, persist_directory=db_dir))

    collection = client.get_collection("docs")  # Replace "docs" with your actual collection name

    try:
        # Fetch all documents in the collection
        all_documents = collection.get()
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if not all_documents['documents']:
        print("No documents found in the database.")
    else:
        for idx, doc in enumerate(all_documents['documents']):
            print(f"Document {idx + 1}: {doc}")

if __name__ == "__main__":
    print_db_content()

