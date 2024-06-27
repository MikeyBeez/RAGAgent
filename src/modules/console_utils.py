# src/modules/console_utils.py

import textwrap
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

def setup_console():
    return Console()

def print_welcome_banner(console):
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
    console.print(Panel(
        Align.center("[bold yellow]Welcome, brave explorer of the AI realm![/bold yellow]\n"
                     "[cyan]What name shall we call you by on this journey?[/cyan]"),
        border_style="bold green"
    ))
    return prompt(HTML('<ansiyellow><b>Your chosen name: </b></ansiyellow>')).strip()

def get_model_choice(console, available_models):
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

    return prompt(HTML('<ansiyellow><b>Choose your AI companion: </b></ansiyellow>')).strip()

def get_user_input(console, user_name):
    console.print("[bold cyan]Type '/help' for available commands.[/bold cyan]")
    return prompt(HTML(f'<ansimagenta><b>Enter your prompt, {user_name}: </b></ansimagenta>'))

def print_command_result(console, result):
    if isinstance(result.get('message'), Panel) and result.get('is_panel', False):
        console.print(result['message'])
    else:
        console.print(f"[bold cyan]{result['message']}[/bold cyan]")

def print_copy_instruction(console):
    console.print("[bold cyan]Type '/copy' to copy this interaction, or enter a new prompt.[/bold cyan]")

def print_chat_history(console, chat_history):
    """Prints the chat history to the console."""
    console.print("[bold blue]Chat History:[/bold blue]\n")
    for i, message in enumerate(chat_history):
        if i % 2 == 0:  # User message
            console.print(f"[bold cyan]User:[/bold cyan] {message.content}")
        else:  # AI message
            console.print(f"[bold green]Otto:[/bold green] {message.content}")
    console.print(f"\n[bold blue]Total interactions: {len(chat_history) // 2}[/bold blue]")
    console.print()  # Add a newline after the chat history
