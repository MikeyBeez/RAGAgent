import argparse
from langchain_community.llms import Ollama

def connect_to_ollama(model_name):
    llm = Ollama(model=model_name)
    return llm

def run_prompt(llm, prompt):
    response = llm.invoke(prompt)
    return response

def main():
    parser = argparse.ArgumentParser(description="Ollama CLI")
    parser.add_argument("--model", type=str, default="gemma:2b", help="Name of the Ollama model to use")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    args = parser.parse_args()

    llm = connect_to_ollama(args.model)
    result = run_prompt(llm, args.prompt)
    print(result)

if __name__ == "__main__":
    main()
