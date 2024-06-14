import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir, 'modules')
sys.path.append(modules_dir)

from connect_ollama import connect_to_ollama, run_prompt
#from ollama_embeddings import store_embeddings, retrieve_relevant_data

def create_memories_directory():
    if not os.path.exists("memories"):
        os.makedirs("memories")

def save_prompt_and_response(prompt, response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"memories/{timestamp}.txt"

    with open(filename, "w") as file:
        file.write(f"Prompt:\n{prompt}\n\n")
        file.write(f"Response:\n{response}\n")

def main():
    model_name = "gemma:2b"  # Replace with the desired model name

    create_memories_directory()

    llm = connect_to_ollama(model_name)

    while True:
        prompt = input("Enter your prompt (or type 'quit' to exit): ")

        if prompt.lower() == "quit":
            break

        result = run_prompt(llm, prompt)
        print("Generated response:")
        print(result)
        print()

        save_prompt_and_response(prompt, result)

        # Store the prompt and response embeddings
        #store_embeddings(prompt, result)

        # Retrieve relevant data based on the prompt
        #relevant_data = retrieve_relevant_data(prompt)
        #print(f"Relevant data: {relevant_data}")

if __name__ == "__main__":
    main()
