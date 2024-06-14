
import os
import requests
import json
from datetime import datetime

def create_memories_directory():
    if not os.path.exists("memories"):
        os.makedirs("memories")

def save_prompt_and_response(prompt, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memories/{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(f"User: {prompt}\n\n")
        file.write(f"Agent: {response}\n\n")

def main():
    model_name = "gemma:2b"  # Replace with the desired model name
    api_url = "http://localhost:11434/api/generate"

    create_memories_directory()

    while True:
        print("\033[1;35mEnter your prompt (or type 'quit' to exit): \033[0m", end="")
        prompt = input()
        print()  # Print a newline after the prompt

        if prompt.lower() == "quit":
            break

        data = {"model": model_name, "prompt": prompt}
        response = requests.post(api_url, json=data)

        print("\033[1;32mAgent: \033[0m", end="")  # Print "Agent: " in bright green

        response_text = ""
        for line in response.iter_lines():
            if line:
                line_decoded = line.decode("utf-8")
                response_json = json.loads(line_decoded)
                print(response_json["response"], end="")  # Print the output
                response_text += response_json["response"]

        print("\n")  # Print a newline after streaming finishes
        save_prompt_and_response(prompt, response_text)

if __name__ == "__main__":
    main() 
