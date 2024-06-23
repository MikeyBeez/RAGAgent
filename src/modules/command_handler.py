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
        to_copy = f"User: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
        pyperclip.copy(to_copy)
        return {"message": "Copied last interaction to clipboard!"}
    else:
        return {"message": "Unknown command"}
