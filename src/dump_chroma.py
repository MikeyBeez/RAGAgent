import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from chromadb import PersistentClient

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "mydbs")

def dump_documents():
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    persistent_client = PersistentClient(path=DB_DIR)
    collection = persistent_client.get_or_create_collection("chat_history")

    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name="chat_history",
        embedding_function=embedding_function,
    )

    # Retrieve all documents from the collection
    results = langchain_chroma.collection.get()

    # Print the documents
    for doc in results["documents"]:
        print(doc)

    print("Total documents:", len(results["documents"]))

# Run the program
dump_documents()

