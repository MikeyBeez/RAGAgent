from langchain_community.tools import DuckDuckGoSearchRun

query = "Who is Beethoven"
search = DuckDuckGoSearchRun()
results = search.run(query)
print(results)
