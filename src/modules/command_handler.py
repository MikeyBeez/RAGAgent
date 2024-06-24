# modules/command_handler.py
import pyperclip
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

COMMAND_SHORTCUTS = {
    "/pch": "/printch",
    "/cch": "/clearch",
    "/lcc": "/lengthch",
    "/ccc": "/copych",
    "/q": "/quit",
    "/nt": "/notalk",
    "/t": "/talk",
    "/tr n": "/truncate n",
    "/sc": "/savechat",
    "/lc": "/listchats",
    "/ldc": "/loadchat",
}

def is_command(user_input):
    return user_input.startswith('/')

def handle_command(command, chat_history, tts_enabled):
    command = COMMAND_SHORTCUTS.get(command.lower(), command.lower())  # Apply shortcut if available

    if command == "/quit":
        return "QUIT"
    elif command == "/talk":
        return {"tts_enabled": True, "message": "Text-to-speech enabled"}
    elif command == "/notalk":
        return {"tts_enabled": False, "message": "Text-to-speech disabled"}
    elif command == "/copy" and chat_history:
        to_copy = f"User: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
        pyperclip.copy(to_copy)
        return {"message": "Copied last interaction to clipboard!"}
    elif command == "/printch":
        return {"message": chat_history}
    elif command == "/clearch":
        chat_history.clear()
        return {"message": "chat history has been cleared"}
    elif command.startswith("/truncate"):
        try:
            _, num_entries = command.split()
            num_entries = int(num_entries)
            if num_entries > 0:
                chat_history[:] = chat_history[-num_entries * 2:]
                return {"message": f"Chat history truncated to {num_entries} entries."}
            else:
                return {"message": "Invalid number of entries. Please provide a positive integer."}
        except (ValueError, IndexError):
            return {"message": "Invalid command format. Use '/truncate n' where 'n' is the number of entries to keep."}
    elif command == "/help":
        return {"message": get_help_text(), "is_panel": True}
    elif command == "/lengthch":
        return {"message": f"Current chat history length: {len(chat_history) // 2} interactions"}
    elif command == "/copych":
        full_history = "\n\n".join([f"User: {chat_history[i].content}\nOtto: {chat_history[i+1].content}" for i in range(0, len(chat_history), 2)])
        pyperclip.copy(full_history)
        return {"message": "Full chat history copied to clipboard!"}
    elif command in ["/savechat", "/listchats", "/loadchat"]:
        return {"message": "HANDLE_IN_MAIN", "command": command}
    else:
        return {"message": "Unknown command"}

def get_help_text():
    """Returns the help message text."""
    help_text = Text.assemble(
        ("  Commands:\n\n   ", Style(color="yellow", bold=True)),
        ("   ", Style(color="yellow")), "\n",
        ("  /quit /q           ", Style(color="cyan")), "- Exit the chat.\n",
        ("  /talk /t           ", Style(color="cyan")), "- text-to-speech.\n",
        ("  /notalk /nt        ", Style(color="cyan")), "- No tts.\n",
        ("  /copy              ", Style(color="cyan")), "- Copy to clipboard.\n",
        ("  /printch /pch      ", Style(color="cyan")), "- list chat history.\n",
        ("  /truncate n  /tr n ", Style(color="cyan")), "- Truncate ch to n. \n",
        ("  /clearch /cch      ", Style(color="cyan")), "- Empty chat history.\n",
        ("  /lengthch /lcc     ", Style(color="cyan")), "- Lenghth chat history.\n",
        ("  /copych /ccc       ", Style(color="cyan")), "- Copy chat history.\n",
        ("  /savechat /sc      ", Style(color="cyan")), "- Save current chat.\n",
        ("  /listchats /lc     ", Style(color="cyan")), "- List saved chats.\n",
        ("  /loadchat /ldc     ", Style(color="cyan")), "- Load a saved chat.\n"
    )
    
    panel = Panel(
        help_text,
        title="OTTO Help",
        border_style="bold green",
        expand=False,
        style="on black"
    )
    
    return panel
