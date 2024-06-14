from langchain.document_loaders import CSVLoader

# Load data from a CSV file using CSVLoader
loader = CSVLoader("./data/data.csv")
documents = loader.load()

# Access the content and metadata of each document
for document in documents:    
		content = document.page_content    
		metadata = document.metadata     
