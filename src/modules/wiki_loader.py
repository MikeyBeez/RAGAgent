from langchain.document_loaders import WikipediaLoader

# Load content from Wikipedia using WikipediaLoader
loader = WikipediaLoader("Machine_learning")
document = loader.load()
