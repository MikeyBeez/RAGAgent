# modules/create_memories.py
import json
import os
from datetime import datetime

def save_prompt_and_response(user_name, prompt, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"
    
    memory_data = {
        "user_name": user_name,
        "user": prompt,
        "agent": response,
        "metadata": {
            "accessCount": 0,
            "lastAccess": None,
            "creation": timestamp
        }
    }
    
    memories_dir = 'memories'
    os.makedirs(memories_dir, exist_ok=True)
    
    file_path = os.path.join(memories_dir, filename)
    with open(file_path, 'w') as f:
        json.dump(memory_data, f, indent=2)

    print(f"Memory saved: {file_path}")
