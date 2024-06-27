# process_prompt.py

import pyperclip
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from modules import ddg_search, chat_history

class ProcessPrompt:
    def __init__(self):
        self.command_shortcuts = {
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

    def process_input(self, user_input, chat_history, tts_enabled):
        if user_input.startswith('/'):
            return self.handle_command(user_input, chat_history, tts_enabled)
        elif user_input.lower().startswith('/search '):
            return self.handle_search(user_input[8:])
        elif user_input.lower().startswith('/memory '):
            return self.handle_memory(user_input[8:], chat_history)
        else:
            return {"type": "prompt", "content": user_input}

    def handle_command(self, command, chat_history, tts_enabled):
        command = self.command_shortcuts.get(command.lower(), command.lower())

        if command == "/quit":
            return {"type": "command", "content": "QUIT"}
        elif command == "/talk":
            return {"type": "command", "content": {"tts_enabled": True, "message": "Text-to-speech enabled"}}
        elif command == "/notalk":
            return {"type": "command", "content": {"tts_enabled": False, "message": "Text-to-speech disabled"}}
        elif command == "/copy" and chat_history:
            to_copy = f"User: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
            pyperclip.copy(to_copy)
            return {"type": "command", "content": {"message": "Copied last interaction to clipboard!"}}
        elif command == "/printch":
            return {"type": "command", "content": {"message": chat_history}}
        elif command == "/clearch":
            chat_history.clear()
            return {"type": "command", "content": {"message": "Chat history has been cleared"}}
        elif command.startswith("/truncate"):
            return self.handle_truncate(command, chat_history)
        elif command.startswith("/tr"):
            return self.handle_truncate(command, chat_history)
        elif command == "/help":
            return {"type": "command", "content": {"message": self.get_help_text(), "is_panel": True}}
        elif command == "/lengthch":
            return {"type": "command", "content": {"message": f"Current chat history length: {len(chat_history) // 2} interactions"}}
        elif command == "/copych":
            full_history = "\n\n".join([f"User: {chat_history[i].content}\nOtto: {chat_history[i+1].content}" for i in range(0, len(chat_history), 2)])
            pyperclip.copy(full_history)
            return {"type": "command", "content": {"message": "Full chat history copied to clipboard!"}}
        elif command in ["/savechat", "/listchats", "/loadchat"]:
            return {"type": "command", "content": {"message": "HANDLE_IN_MAIN", "command": command}}
        else:
            return {"type": "command", "content": {"message": "Unknown command"}}

    def handle_truncate(self, command, chat_history):
        try:
            _, num_entries = command.split()
            num_entries = int(num_entries)
            if num_entries > 0:
                chat_history[:] = chat_history[-num_entries * 2:]
                return {"type": "command", "content": {"message": f"Chat history truncated to {num_entries} entries."}}
            else:
                return {"type": "command", "content": {"message": "Invalid number of entries. Please provide a positive integer."}}
        except (ValueError, IndexError):
            return {"type": "command", "content": {"message": "Invalid command format. Use '/truncate n' where 'n' is the number of entries to keep."}}

    def handle_search(self, query):
        search_results = ddg_search.run_search(query)
        context = f"Search results for '{query}': {search_results}"
        return {"type": "prompt", "content": context + "\n\n" + query}

    def handle_memory(self, query, chat_history):
        relevant_memories = chat_history.search_memories(query)
        context = f"Relevant memories: {relevant_memories}"
        return {"type": "prompt", "content": context + "\n\n" + query}

    def get_help_text(self):
        help_text = Text.assemble(
            ("  Commands:\n\n   ", Style(color="yellow", bold=True)),
            ("   ", Style(color="yellow")), "\n",
            ("  /quit /q           ", Style(color="cyan")), "- Exit the chat.\n",
            ("  /talk /t           ", Style(color="cyan")), "- Enable text-to-speech.\n",
            ("  /notalk /nt        ", Style(color="cyan")), "- Disable text-to-speech.\n",
            ("  /copy              ", Style(color="cyan")), "- Copy to clipboard.\n",
            ("  /printch /pch      ", Style(color="cyan")), "- List chat history.\n",
            ("  /truncate n  /tr n ", Style(color="cyan")), "- Truncate chat history to n.\n",
            ("  /clearch /cch      ", Style(color="cyan")), "- Clear chat history.\n",
            ("  /lengthch /lcc     ", Style(color="cyan")), "- Show chat history length.\n",
            ("  /copych /ccc       ", Style(color="cyan")), "- Copy full chat history.\n",
            ("  /savechat /sc      ", Style(color="cyan")), "- Save current chat.\n",
            ("  /listchats /lc     ", Style(color="cyan")), "- List saved chats.\n",
            ("  /loadchat /ldc     ", Style(color="cyan")), "- Load a saved chat.\n",
            ("  /search query      ", Style(color="cyan")), "- Perform a web search.\n",
            ("  /memory query      ", Style(color="cyan")), "- Search chat memories.\n"
        )
        
        return Panel(
            help_text,
            title="OTTO Help",
            border_style="bold green",
            expand=False,
            style="on black"
        )
