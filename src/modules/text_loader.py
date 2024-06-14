from langchain_community.document_loaders import TextLoader

loader = TextLoader("./index.md")
loader.load()
