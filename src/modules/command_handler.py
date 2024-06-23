# modules/command_handler.py
# This module runs all the special commands that start with a slash /
import pyperclip

def is_command(user_input):
    return user_input.startswith('/')

def handle_command(command, chat_history, tts_enabled):
    if command.lower() == "/quit":
        return "QUIT"
    elif command.lower() == "/talk":
        return {"tts_enabled": True, "message": "Text-to-speech enabled"}
    elif command.lower() == "/notalk":
        return {"tts_enabled": False, "message": "Text-to-speech disabled"}
    elif command.lower() == "/copy" and chat_history:
        to_copy = f"User: {chat_history[-2].content}\n" \
                  f"Otto: {chat_history[-1].content}"
        pyperclip.copy(to_copy)
        return {"message": "Copied last interaction to clipboard!"}
    elif command.lower() == "/printchathistory":
        return {"message": chat_history}
    elif command.lower() == "/clearchathistory":
        chat_history.clear()
        return {"message": "chat history has been cleared"}
    elif command.lower().startswith("/truncate"):
        try:
            _, num_entries = command.split()  # Split command into "/truncate" and "n"
            num_entries = int(num_entries)
            if num_entries > 0:
                chat_history[:] = chat_history[-num_entries * 2:]  # Truncate the list in place
                return {"message": f"Chat history truncated to {num_entries} entries."}
            else:
                return {"message": "Invalid number of entries. " \
                        "Please provide a positive integer."}
        except (ValueError, IndexError):
            return {"message": "Invalid command format. " \
                    "Use '/truncate n' where 'n' is the number of entries to keep."}
    elif command.lower() == "/help":
        return {"message": get_help_text()}  # Return the help text
    else:
        return {"message": "Unknown command"}

def get_help_text():
    """Returns the help message text."""
    help_text = "\n[bold cyan]Available Commands:[/bold cyan]\n"
    help_text += "  /quit                - Exit the chat.\n"
    help_text += "  /talk                - Enable text-to-speech.\n"
    help_text += "  /notalk              - Disable text-to-speech.\n"
    help_text += "  /copy                - Copy the last interaction to the clipboard.\n"
    help_text += "  /printchathistory    - Display the chat history.\n" 
    help_text += "  /truncate n          - Truncate chat history to the last 'n' entries.\n"
    help_text += "  /clearchathistory    - Empty the chat history.\n" 
    return help_text
