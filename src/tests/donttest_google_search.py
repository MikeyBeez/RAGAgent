import os
import sys
import requests

# Add the relative path to the config file
sys.path.append(os.path.join('..', '..'))
from config import GAPI, SEARCH_URL

def google_search(query, api_key, **kwargs):
    url = SEARCH_URL
    params = {"key": api_key, "q": query, "num": 2}  # Retrieve 2 results
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    query = "meta ai"
    results = google_search(query, GAPI)
    print(results)
