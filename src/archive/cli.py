# cli.py
import argparse
from connect_openai import create_openai_llm, generate_response

def main():
    parser = argparse.ArgumentParser(description="OpenAI CLI")
    parser.add_argument("--model", default="text-davinci-002", help="OpenAI model to use")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--max_tokens", type=int, default=100, help="Maximum number of tokens to generate")
    args = parser.parse_args()

    llm = create_openai_llm()

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        response = generate_response(llm, user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
