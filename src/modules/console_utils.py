# src/modules/console_utils.py

import textwrap
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
import logging

def setup_console():
    logging.debug("Setting up console")
    return Console()

def print_welcome_banner(console):
    logging.debug("Printing welcome banner")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    banner = """
    [bold yellow] ██████  ████████ ████████  ██████ [/bold yellow]
    [bold red]██    ██    ██       ██    ██    ██[/bold red]
    [bold green]██    ██    ██       ██    ██    ██[/bold green]
    [bold blue]██    ██    ██       ██    ██    ██[/bold blue]
    [bold magenta]██    ██    ██       ██    ██    ██[/bold magenta]
    [bold cyan] ██████     ██       ██     ██████ [/bold cyan]
    
    [bold white]Your Intelligent Conversational Companion[/bold white]
    """
    console.print(Panel(Align.center(banner), border_style="bold white", expand=False))

def print_separator(console):
    console.print("\n", end="")  # Start a new line
    f1 = "[bold dark_blue]~[/]"
    f2 = "[bold yellow]*[/]"
    separator = (f1 + f2) * 45
    console.print(separator + "\n")  # End with another new line

def print_wrapped_text(console, text):
    wrapped_text = textwrap.fill(text, width=70)
    console.print(wrapped_text)

def get_user_name(console):
    logging.debug("Prompting for user name")
    console.print(Panel(
        Align.center("[bold yellow]Welcome, brave explorer of the AI realm![/bold yellow]\n"
                     "[cyan]What name shall we call you by on this journey?[/cyan]"),
        border_style="bold green"
    ))
    user_name = prompt(HTML('<ansiyellow><b>Your chosen name: </b></ansiyellow>')).strip()
    logging.info(f"User name set to: {user_name}")
    return user_name

def get_model_choice(console, available_models):
    logging.debug("Prompting for model choice")
    model_list = [f"[cyan]• {model}[/cyan]" for model in available_models]
    
    columns = Columns(model_list, equal=True, expand=False)
    
    panel = Panel(
        Align.center(columns),
        title="[bold green]Available Models[/bold green]",
        border_style="bold blue",
        expand=False
    )
    
    console.print("[bold yellow]Behold, the pantheon of AI models at your disposal:[/bold yellow]\n")
    console.print(panel)

    model_choice = prompt(HTML('<ansiyellow><b>Choose your AI companion: </b></ansiyellow>')).strip()
    logging.info(f"User selected model: {model_choice}")
    return model_choice

def get_user_input(console, user_name):
    console.print("[bold cyan]Type '/help' for available commands.[/bold cyan]")
    user_input = prompt(HTML(f'<ansimagenta><b>Enter your prompt, {user_name}: </b></ansimagenta>'))
    logging.debug(f"User input: {user_input}")
    return user_input

def print_command_result(console, result):
    if isinstance(result.get('message'), Panel) and result.get('is_panel', False):
        console.print(result['message'])
    else:
        console.print(f"[bold cyan]{result['message']}[/bold cyan]")
    logging.debug(f"Printed command result: {result['message']}")

def print_copy_instruction(console):
    console.print("[bold cyan]Type '/copy' to copy this interaction, or enter a new prompt.[/bold cyan]")

def print_chat_history(console, chat_history):
    """Prints the chat history to the console."""
    logging.debug("Printing chat history")
    console.print("[bold blue]Chat History:[/bold blue]\n")
    for i, message in enumerate(chat_history):
        if i % 2 == 0:  # User message
            console.print(f"[bold cyan]User:[/bold cyan] {message.content}")
        else:  # AI message
            console.print(f"[bold green]Otto:[/bold green] {message.content}")
    console.print(f"\n[bold blue]Total interactions: {len(chat_history) // 2}[/bold blue]")
    console.print()  # Add a newline after the chat history
    logging.info(f"Printed chat history with {len(chat_history) // 2} interactions")

def print_memory_search_results(console, relevant_memories):
    """Prints the memory search results to the console."""
    logging.debug("Printing memory search results")
    console.print("[bold blue]Memory Search Results:[/bold blue]\n")
    for i, memory in enumerate(relevant_memories, 1):
        console.print(f"[bold cyan]Memory {i}:[/bold cyan]")
        console.print(f"User: {memory['user']}")
        console.print(f"Agent: {memory['agent']}")
        if memory['search_results']:
            console.print(f"Search Results: {memory['search_results']}")
        console.print(f"Similarity: {memory['similarity']:.4f}")
        console.print(f"Access Count: {memory['metadata']['access_count']}")
        console.print(f"Last Accessed: {memory['metadata']['last_accessed']}")
        console.print()
    logging.info(f"Printed {len(relevant_memories)} memory search results")
