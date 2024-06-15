import ollama
import os
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
    create_memories_directory()

    while True:
        print("\033[1;35mEnter your prompt (or type 'quit' to exit): \033[0m", end="")
        prompt = input()
        print()  # Print a newline after the prompt

        if prompt.lower() == "quit":
            break

        stream = ollama.chat(
                model='gemma:2b',
                keep_alive=1,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        response_text = ""
        for chunk in stream:
            response_text += chunk['message']['content']
            print(chunk['message']['content'], end='', flush=True)

        print("\n")  # Print a newline after streaming finishes
        save_prompt_and_response(prompt, response_text)

if __name__ == "__main__":
    main()
