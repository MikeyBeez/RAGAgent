# process_prompt.py

import pyperclip
from rich import box
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from modules.ddg_search import DDGSearch
from modules.ollama_embeddings import search_memories, add_memory

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
            "/m": "/memory",
        }
        self.ddg_search = DDGSearch()

    def process_input(self, user_input, chat_history, tts_enabled):
        if user_input.startswith('/'):
            if user_input.lower().startswith('/search '):
                return self.handle_search(user_input[8:])
            elif user_input.lower().startswith('/memory ') or user_input.lower().startswith('/m '):
                return self.handle_memory(user_input[8:] if user_input.lower().startswith('/memory ') else user_input[3:], chat_history)
            else:
                return self.handle_command(user_input, chat_history, tts_enabled)
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
        search_results = self.ddg_search.run_search(query)
        context = f"Search results for '{query}':\n" + "\n".join(search_results)
        return {"type": "prompt", "content": context + "\n\nQuestion: " + query}

    def handle_memory(self, query, chat_history):
        relevant_memories = search_memories(query)
        context = "Relevant memories:\n"
        for mem in relevant_memories:
            context += f"User: {mem['user']}\n"
            context += f"Agent: {mem['agent']}\n"
            if mem['search_results']:
                context += f"Search Results: {mem['search_results']}\n"
            context += "\n"
        return {"type": "prompt", "content": context + "\n" + query}

    def add_to_memory(self, user_input, agent_response, search_results=""):
        add_memory(user_input, agent_response, search_results)

    def get_help_text(self):
        commands = [
            ("/quit, /q", "Exit the chat"),
            ("/talk, /t", "Enable text-to-speech"),
            ("/notalk, /nt", "Disable text-to-speech"),
            ("/copy", "Copy to clipboard"),
            ("/printch, /pch", "List chat history"),
            ("/tr n", "Truncate chat history to n"),
            ("/clearch, /cch", "Clear chat history"),
            ("/lengthch, /lcc", "Show chat history length"),
            ("/copych, /ccc", "Copy full chat history"),
            ("/savechat, /sc", "Save current chat"),
            ("/listchats, /lc", "List saved chats"),
            ("/loadchat, /ldc", "Load a saved chat"),
            ("/search query", "Perform a web search"),
            ("/memory query, /m query", "Search chat memories"),
        ]

        def create_command_text(command, description):
            return Text.assemble(
                (f"  {command:<18}", Style(color="green")),
                (f"{description}\n", Style(color="yellow"))
            )

        left_column = [create_command_text(cmd, desc) for cmd, desc in commands[:7]]
        right_column = [create_command_text(cmd, desc) for cmd, desc in commands[7:]]

        columns = Columns([Text().join(left_column), Text().join(right_column)])

        return Panel(
            columns,
            title="OTTO Help",
            border_style="bold green",
            expand=False,
            box=box.ROUNDED,
            padding=(1, 1)
        )
