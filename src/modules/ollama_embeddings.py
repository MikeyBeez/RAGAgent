import os
import ollama
import chromadb

# Create the "mydbs" directory if it doesn't exist
db_dir = "mydbs"
os.makedirs(db_dir, exist_ok=True)

documents = [
    "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
    "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
    "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
    "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
    "Llamas are vegetarians and have very efficient digestive systems",
    "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

client = chromadb.PersistentClient(
    path=db_dir,
    settings=chromadb.config.Settings(),
)
collection = client.create_collection(name="docs")

# Store each document in a vector embedding database
for i, d in enumerate(documents):
    response = ollama.embeddings(model="all-minilm", prompt=d)
    embedding = response["embedding"]
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d]
    )

# An example prompt
prompt = "What animals are llamas related to?"

# Generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
    prompt=prompt,
    model="all-minilm"
)
results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=1
)
data = results['documents'][0][0]

# Generate a response combining the prompt and data we retrieved
output = ollama.generate(
    model="gemma:2b",
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])
