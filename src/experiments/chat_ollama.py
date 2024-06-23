import logging
import subprocess
import textwrap
from rich.console import Console
from rich.text import Text
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules.create_memories import save_prompt_and_response
import pyperclip
import threading
import queue
import time

# Set up logging
logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_available_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
        return models
    except Exception as e:
        logging.error(f"Error fetching models: {str(e)}")
        return []

def print_wrapped_text(console, text):
    wrapped_text = textwrap.fill(text, width=70)
    console.print(wrapped_text, end="")


def speak_text(text):
    try:
        time.sleep(0.5)  # Add a 0.5-second delay before speaking
        subprocess.run(['say', text], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in text-to-speech: {e}")


def tts_worker(tts_queue):
    while True:
        text = tts_queue.get()
        if text is None:
            break
        speak_text(text)
        tts_queue.task_done()

def main():
    logging.info("Starting chat application")
    
    console = Console()

    user_name = console.input("[bold yellow]Enter your name (or press Enter for 'User'): [/bold yellow]").strip() or "User"

    available_models = get_available_models()
    
    if not available_models:
        console.print("[bold yellow]No models found. You may need to pull a model first.[/bold yellow]")
        console.print("[bold yellow]Suggestion: Run 'ollama pull llama3' to get started.[/bold yellow]")
        return

    console.print("[bold cyan]Available models:[/bold cyan]")
    for model in available_models:
        console.print(f"- {model}")

    default_model = "llama3:latest" if "llama3:latest" in available_models else available_models[0]
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
    text_to_speech_enabled = False
    tts_queue = queue.Queue()
    tts_thread = threading.Thread(target=tts_worker, args=(tts_queue,))
    tts_thread.start()

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI named Otto, you answer questions with informative and accurate responses."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm

    while True:
        console.print(f"[bold magenta]{user_name}, enter your prompt (type '/copy' to copy last interaction, '/talk' to enable TTS, '/notalk' to disable TTS, '/quit' to exit):[/bold magenta]")
        prompt = console.input()
        console.print()

        if prompt.lower() == "/quit":
            break

        if prompt.lower() == "/talk":
            text_to_speech_enabled = True
            console.print("[bold cyan]Text-to-speech enabled[/bold cyan]")
            continue

        if prompt.lower() == "/notalk":
            text_to_speech_enabled = False
            console.print("[bold cyan]Text-to-speech disabled[/bold cyan]")
            continue

        if prompt.lower() == "/copy" and chat_history:
            to_copy = f"{user_name}: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
            pyperclip.copy(to_copy)
            console.print("[bold cyan]Copied last interaction to clipboard![/bold cyan]")
            continue

        logging.info(f"User input: {prompt}")

        try:
            console.print(f"[bold magenta]{user_name}:[/bold magenta] {prompt}")
            
            console.print("[bold green]Otto:[/bold green] ", end="")
            response_text = ""
            buffer = ""
            for chunk in llm.stream(prompt_template.format(input=prompt, chat_history=chat_history)):
                response_text += chunk
                buffer += chunk
                if "\n" in buffer or len(buffer) > 50:
                    lines = buffer.split("\n")
                    for line in lines[:-1]:
                        print_wrapped_text(console, line)
                        console.print()
                        if text_to_speech_enabled:
                            tts_queue.put(line)
                    buffer = lines[-1]
            if buffer:
                print_wrapped_text(console, buffer)
                console.print()
                if text_to_speech_enabled:
                    tts_queue.put(buffer)

            logging.info(f"AI response: {response_text}")

            chat_history.append(HumanMessage(content=prompt))
            chat_history.append(AIMessage(content=response_text))

            save_prompt_and_response(prompt, response_text)

            console.print("[bold cyan]Type 'copy' to copy this interaction, or enter a new prompt.[/bold cyan]")

        except Exception as e:
            console.print(f"[bold red]Error during interaction: {str(e)}[/bold red]")
            logging.error(f"Error during interaction: {str(e)}")

    # Clean up TTS thread
    tts_queue.put(None)
    tts_thread.join()
    logging.info("Chat application terminated")

if __name__ == "__main__":
    main()
