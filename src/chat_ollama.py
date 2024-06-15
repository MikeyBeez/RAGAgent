import os
import requests
import json
from datetime import datetime
from modules.create_memories import save_prompt_and_response

def main():
    model_name = "gemma:2b"  # Replace with the desired model name
    api_url = "http://localhost:11434/api/generate"

    while True:
        print("\033[1;35mEnter your prompt (or type 'quit' to exit): \033[0m", end="")
        prompt = input()
        print()  # Print a newline after the prompt

        if prompt.lower() == "quit":
            break

        data = {
            "model": model_name,
            "prompt": prompt,
            "keep_alive": "1h",  # Set keep_alive to 1 hour
            "stream": True  # Enable streaming
        }
        response = requests.post(api_url, json=data, stream=True)  # Set stream=True

        print("\033[1;32mAgent: \033[0m", end="")  # Print "Agent: " in bright green

        response_text = ""
        for line in response.iter_lines():
            if line:
                line_decoded = line.decode("utf-8")
                response_json = json.loads(line_decoded)
                print(response_json["response"], end="", flush=True)  # Print each line as it is received
                response_text += response_json["response"]

        print("\n")  # Print a newline after streaming finishes
        save_prompt_and_response(prompt, response_text)

if __name__ == "__main__":
    main()
