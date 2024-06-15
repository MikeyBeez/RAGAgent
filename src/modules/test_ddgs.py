from langchain_community.tools import DuckDuckGoSearchRun

query = "Who is Beethoven"
search = DuckDuckGoSearchRun()
try:
    results = search.run(query)
    if isinstance(results, str):  # check if results is a string
        results_list = results.split("\n")  # split into a list
    else:  # assume it's already a list
        results_list = results
    for result in results_list:
        print(result)
except Exception as e:  # catch any exceptions
    print(f"Error: {e}")
    # you can try again here if you want
    # search.run(query)  # try again
