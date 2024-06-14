from langchain_community.llms import Ollama

llm = Ollama(
        model="gemma:2b"
)  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `

response = llm.invoke("Tell me a joke")
print(response)
