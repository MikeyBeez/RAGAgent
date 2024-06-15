import os
import json
from datetime import datetime

def save_prompt_and_response(prompt, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memories/{timestamp}.txt"

    # Create the directory if it doesn't exist
    os.makedirs("memories", exist_ok=True)

    # Add metadata (example)
    metadata = {
        "accessCount": 0,
        "lastAccess": None,
        "creation": timestamp
    }

    with open(filename, "w") as file:
        file.write(f"User: {prompt}\n\n")
        file.write(f"Agent: {response}\n\n")
        json.dump(metadata, file)  # Serialize metadata to JSON

    return filename  # Return the filename for potential future use
