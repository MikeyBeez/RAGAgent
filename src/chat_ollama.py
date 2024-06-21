import logging
import subprocess
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules.create_memories import save_prompt_and_response
import pyperclip

# Set up logging
logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_chat_panel(prompt, response, index):
    content = f"[bold magenta]You:[/bold magenta] {prompt}\n\n[bold green]Otto:[/bold green] {response}"
    return Panel(content, title=f"Interaction {index + 1}", border_style="bold")

def get_available_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
        return models
    except Exception as e:
        logging.error(f"Error fetching models: {str(e)}")
        return []

def main():
    logging.info("Starting chat application")
    
    console = Console()

    available_models = get_available_models()
    
    if not available_models:
        console.print("[bold yellow]No models found. You may need to pull a model first.[/bold yellow]")
        console.print("[bold yellow]Suggestion: Run 'ollama pull llama3' to get started.[/bold yellow]")
        return

    console.print("[bold cyan]Available models:[/bold cyan]")
    for model in available_models:
        console.print(f"- {model}")

    default_model = "llama3" if "llama3" in available_models else available_models[0]
    model_name = console.input(f"[bold yellow]Enter the Ollama model name (default is {default_model}): [/bold yellow]")
    model_name = model_name.strip() if model_name.strip() else default_model
    
    if model_name not in available_models:
        console.print(f"[bold red]Model '{model_name}' not found. Please pull it first with 'ollama pull {model_name}'[/bold red]")
        return

    try:
        llm = Ollama(model=model_name)
        logging.info(f"Initialized Ollama LLM with {model_name} model")
        console.print(f"[bold green]Successfully initialized {model_name} model[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error initializing the model: {str(e)}[/bold red]")
        return

    chat_history = []

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI named Otto, you answer questions with informative and accurate responses."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm

    interaction_count = 0

    while True:
        prompt = console.input("[bold magenta]Enter your prompt (type 'copy' to copy last interaction, '/quit' to exit): [/bold magenta]")
        console.print()

        if prompt.lower() == "/quit":
            break

        if prompt.lower() == "copy" and interaction_count > 0:
            to_copy = f"You: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
            pyperclip.copy(to_copy)
            console.print("[bold cyan]Copied last interaction to clipboard![/bold cyan]")
            continue

        logging.info(f"User input: {prompt}")

        try:
            response_text = ""
            with Live(Panel(response_text, title="Otto is thinking...", border_style="yellow"), refresh_per_second=4) as live:
                for chunk in llm.stream(prompt_template.format(input=prompt, chat_history=chat_history)):
                    response_text += chunk
                    live.update(Panel(response_text, title="Otto", border_style="green"))

            logging.info(f"AI response: {response_text}")

            chat_history.append(HumanMessage(content=prompt))
            chat_history.append(AIMessage(content=response_text))

            panel = create_chat_panel(prompt, response_text, interaction_count)
            console.print(panel)

            save_prompt_and_response(prompt, response_text)

            interaction_count += 1

        except Exception as e:
            console.print(f"[bold red]Error during interaction: {str(e)}[/bold red]")
            logging.error(f"Error during interaction: {str(e)}")

    logging.info("Chat application terminated")

if __name__ == "__main__":
    main()
