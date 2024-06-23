# modules/command_handler.py
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
        to_copy = f"User: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
        pyperclip.copy(to_copy)
        return {"message": "Copied last interaction to clipboard!"}
    elif command.lower() == "/printchathistory":
        return {"message": chat_history}
    elif command.lower() == "/clearchathistory":
        chat_history.clear()
        return {"message": "chat history has been cleared"}
    elif command.lower().startswith("/truncate"):
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
    elif command.lower() == "/help":
        return {"message": get_help_text()}
    elif command.lower() == "/lengthchathistory":
        return {"message": f"Current chat history length: {len(chat_history) // 2} interactions"}
    elif command.lower() == "/copychathistory":
        full_history = "\n\n".join([f"User: {chat_history[i].content}\nOtto: {chat_history[i+1].content}" for i in range(0, len(chat_history), 2)])
        pyperclip.copy(full_history)
        return {"message": "Full chat history copied to clipboard!"}
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
    help_text += "  /lengthchathistory   - Display the number of interactions in the chat history.\n"
    help_text += "  /copychathistory     - Copy the full chat history to the clipboard.\n"
    return help_text
