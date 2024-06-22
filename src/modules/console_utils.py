# modules/console_utils.py
import textwrap
from rich.console import Console

def setup_console():
    return Console()

# In modules/console_utils.py

def print_separator(console):
    console.print("\n", end="") # Start a new line
    f1 = "[bold dark_blue]~[/]"
    f2 = "[bold yellow]*[/]"
    separator = (f1 + f2) * 45
    console.print(separator + "\n") # End with another new line

#def print_separator(console):
#    emoji1 = "🔵"  # Dark blue circle emoji
#    emoji2 = "🙂"
#    separator = (emoji1 + emoji2) * 11  # Repeat the pattern 11 times
#    console.print("\n" + separator + "\n")

def print_wrapped_text(console, text):
    wrapped_text = textwrap.fill(text, width=70)
    console.print(wrapped_text, end="")

def get_user_name(console):
    return console.input("[bold yellow]Enter your name (or press Enter for 'User'): [/bold yellow]").strip() or "User"

def get_model_choice(console, available_models):
    console.print("[bold cyan]Available models:[/bold cyan]")
    for model in available_models:
        console.print(f"- {model}")

    default_model = "llama3:latest" if "llama3:latest" in available_models else available_models[0]
    return console.input(f"[bold yellow]Enter the Ollama model name (default is {default_model}): [/bold yellow]").strip() or default_model

def get_user_input(console, user_name):
    return console.input(f"[bold magenta]{user_name}, enter your prompt (type '/copy' to copy last interaction, '/talk' to enable TTS, '/notalk' to disable TTS, '/quit' to exit):[/bold magenta]")

def print_command_result(console, result):
    console.print(f"[bold cyan]{result['message']}[/bold cyan]")

def print_copy_instruction(console):
    console.print("[bold cyan]Type '/copy' to copy this interaction, or enter a new prompt.[/bold cyan]")
