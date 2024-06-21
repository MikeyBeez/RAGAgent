import logging
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules.create_memories import save_prompt_and_response

# Set up logging
logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting chat application")
    
    # Initialize Rich Console
    console = Console()

    # Initialize the Ollama LLM
    llm = Ollama(model="llama3")
    logging.info("Initialized Ollama LLM with llama3 model")

    # Initialize chat history
    chat_history = []

    # Define the prompt template for chat interactions
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI named Otto, you answer questions with simple answers and no funny stuff."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    # Create a chain that combines the prompt template with the Ollama LLM
    chain = prompt_template | llm

    while True:
        prompt = console.input("[bold magenta]Enter your prompt (or type 'quit' to exit): [/bold magenta]")
        console.print()

        if prompt.lower() == "quit":
            break

        logging.info(f"User input: {prompt}")

        # TODO: Implement router to decide between tools and LLM
        # if should_use_tool(prompt):
        #     response = use_tool(prompt)
        # else:
        #     # Use LLM as before

        # Invoke the chain to generate a response
        response = chain.invoke({"input": prompt, "chat_history": chat_history})

        logging.info(f"AI response: {response}")

        # Update chat history with user input and AI response
        chat_history.append(HumanMessage(content=prompt))
        chat_history.append(AIMessage(content=response))

        # Print the AI's response using Rich
        ai_response = Text(response)
        ai_panel = Panel(ai_response, title="Agent Otto", border_style="green")
        console.print(ai_panel)

        # Save prompt and response to memory
        save_prompt_and_response(prompt, response)

    logging.info("Chat application terminated")

if __name__ == "__main__":
    main()
