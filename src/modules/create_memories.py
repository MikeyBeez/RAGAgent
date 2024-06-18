import os
import json
from datetime import datetime

def save_prompt_and_response(prompt, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memories/{timestamp}.json"

    # Create the directory if it doesn't exist
    os.makedirs("memories", exist_ok=True)

    # Create the JSON object
    data = {
        "user": prompt,
        "agent": response,
        "metadata": {
            "accessCount": 0,
            "lastAccess": None,
            "creation": timestamp
        }
    }

    # Write the JSON object to the file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return filename  # Return the filename for potential future use
