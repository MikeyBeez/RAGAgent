import os
import json
from datetime import datetime, timedelta

memories_dir = os.path.join("..", "memories")
current_timestamp = datetime.now()

for filename in os.listdir(memories_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(memories_dir, filename)
        
        with open(file_path, "r") as file:
            data = json.load(file)
            metadata = data.get("metadata", {})
            
            creation_timestamp_str = metadata.get("creation")
            if creation_timestamp_str:
                try:
                    creation_timestamp = datetime.strptime(creation_timestamp_str, "%Y%m%d_%H%M%S")
                    if (current_timestamp - creation_timestamp) > timedelta(days=5) and metadata.get("accessCount", 0) == 0:
                        user_input = input(f"Do you want to delete the file {filename}? (y/n): ")
                        if user_input.lower() == "y":
                            os.remove(file_path)
                            print(f"Deleted file: {filename}")
                        else:
                            print(f"Skipped deleting file: {filename}")
                except ValueError:
                    print(f"Skipping file {filename} due to invalid creation timestamp.")
            else:
                print(f"Skipping file {filename} due to missing creation timestamp.")

print("File deletion process completed.")
