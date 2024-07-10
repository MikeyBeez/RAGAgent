# process_prompt.py

import logging
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
            "/q": "/quit",
            "/nt": "/notalk",
            "/t": "/talk",
            "/tr n": "/truncate n",
            "/sc": "/savechat",
            "/lc": "/listchats",
            "/ldc": "/loadchat",
            "/m": "/memory",
            "/f": "/fabric",
            "/sp": "/showpattern",
        }
        self.ddg_search = DDGSearch()

    def process_input(self, user_input, chat_history):
        logging.debug(f"Processing user input: {user_input}")
        if user_input.startswith('/'):
            if user_input.lower().startswith('/search '):
                logging.debug("Detected search command")
                return self.handle_search(user_input[8:])
            elif user_input.lower().startswith('/memory ') or user_input.lower().startswith('/m '):
                logging.debug("Detected memory command")
                return self.handle_memory(user_input[8:] if user_input.lower().startswith('/memory ') else user_input[3:], chat_history)
            else:
                logging.debug("Detected other command")
                return self.handle_command(user_input, chat_history)
        else:
            logging.debug("Input is a prompt, returning content")
            return {"type": "prompt", "content": user_input}

    def handle_command(self, command, chat_history):
        command = self.command_shortcuts.get(command.lower(), command.lower())
        logging.debug(f"Handling command: {command}")

        if command == "/quit":
            return {"type": "command", "content": "QUIT"}
        elif command == "/talk":
            return {"type": "command", "content": {"tts_enabled": True, "message": "Text-to-speech enabled"}}
        elif command == "/notalk":
            return {"type": "command", "content": {"tts_enabled": False, "message": "Text-to-speech disabled"}}
        elif command == "/copy":
            logging.debug("Copying last interaction")
            to_copy = f"User: {chat_history[-2].content}\nOtto: {chat_history[-1].content}"
            pyperclip.copy(to_copy)
            return {"type": "command", "content": {"message": "Copied last interaction to clipboard!"}}
        elif command.startswith("/truncate") or command.startswith("/tr"): 
            logging.debug("Truncating chat history")
            return self.handle_truncate(command, chat_history)
        elif command == "/help":
            logging.debug("Displaying help text")
            return {"type": "command", "content": {"message": self.get_help_text(), "is_panel": True}}
        elif command.startswith("/chat "):
            chat_title = command[6:].strip()
            if chat_title:
                return {"type": "command", "content": {"message": "CREATE_NEW_CHAT", "title": chat_title}}
        elif command == "/savechat":
            return {"type": "command", "content": {"message": "SAVE_CHAT"}}
        elif command == "/loadchat":
            return {"type": "command", "content": {"message": "LOAD_CHAT"}}
        elif command.startswith("/fabric") or command.startswith("/f"):
            return {"type": "command", "content": {"message": "SELECT_PATTERN"}}
        elif command.startswith("/showpattern") or command.startswith("/sp"):
            return {"type": "command", "content": {"message": "SHOW_PATTERN"}}
        else:
            logging.warning(f"Unknown command encountered: {command}")
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
        logging.debug(f"Performing search for: {query}")
        search_results = self.ddg_search.run_search(query)
        context = f"Search results for '{query}':\n" + "\n".join(search_results)
        # Pass search_results to add_to_memory
        self.add_to_memory("", "", "\n".join(search_results))  # Adding search results to memory
        logging.debug("Search complete, returning results") 
        return {"type": "prompt", "content": context + "\n\nQuestion: " + query}

    def handle_memory(self, query, chat_history):
        logging.debug(f"Searching memories for: {query}")
        relevant_memories = search_memories(query)
        context = "Relevant memories:\n"
        for mem in relevant_memories:
            context += f"User: {mem['user']}\n"
            context += f"Agent: {mem['agent']}\n"
            if mem['search_results']:
                context += f"Search Results: {mem['search_results']}\n"
            context += "\n"
        logging.debug("Memory search complete, returning results")
        return {"type": "prompt", "content": context + "\n" + query}

    def add_to_memory(self, user_input, agent_response, search_results=""):
        logging.debug("Adding interaction to memory")
        add_memory(user_input, agent_response, search_results)

    def get_help_text(self):
        commands = [
            ("/quit, /q", "Exit the chat"),
            ("/talk, /t", "Enable text-to-speech"),
            ("/notalk, /nt", "Disable text-to-speech"),
            ("/copy", "Copy to clipboard"),
            ("/truncate n, /tr n", "Truncate chat history to n"),
            ("/search query", "Perform a web search"),
            ("/memory query, /m query", "Search memories"),
            ("/chat <title>", "Create a new chat"),
            ("/savechat", "Save the current chat"),
            ("/loadchat", "Load a saved chat"),
            ("/fabric, /f", "Select a Fabric pattern"),
            ("/showpattern, /sp", "Show the current pattern"),
        ]

        def create_command_text(command, description):
            return Text.assemble(
                (f"  {command:<18}", Style(color="green")),
                (f"{description}\n", Style(color="yellow"))
            )

        left_column = [create_command_text(cmd, desc) for cmd, desc in commands[:6]]
        right_column = [create_command_text(cmd, desc) for cmd, desc in commands[6:]]

        columns = Columns([Text().join(left_column), Text().join(right_column)])

        return Panel(
            columns,
            title="OTTO Help",
            border_style="bold green",
            expand=False,
            box=box.ROUNDED,
            padding=(1, 1)
        )
