from connect_ollama import connect_to_ollama, run_prompt

def main():
    model_name = "gemma:2b"  # Replace with the desired model name

    llm = connect_to_ollama(model_name)

    while True:
        prompt = input("Enter your prompt (or type 'quit' to exit): ")

        if prompt.lower() == "quit":
            break

        result = run_prompt(llm, prompt)
        print("Generated response:")
        print(result)
        print()

if __name__ == "__main__":
    main()
