# main.py
import sys
import os
import logging
from datetime import datetime

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.initializer import initialize_app
from src.modules import console_utils, llm_interaction, tts_module, chat_history, model_utils
from src.modules.chat_manager import Chat
from src.modules.process_prompt import ProcessPrompt
from src.modules.pattern_manager import PatternManager
import config

def run_chat_application():
    logging.info("Starting chat application")
    console = console_utils.setup_console()  # Initialize console at the beginning
    try:
        app_components = initialize_app()
        
        user_name = app_components['user_name']
        llm = app_components['llm']
        chat_hist = app_components['chat_hist']
        tts_enabled = app_components['tts_enabled']
        tts_queue = app_components['tts_queue']
        tts_thread = app_components['tts_thread']
        chat_manager = app_components['chat_manager']
        current_chat = Chat("Untitled Chat")  # Create a new Chat object
        prompt_processor = ProcessPrompt()

        # Initialize PatternManager
        patterns_dir = os.path.join(os.path.expanduser('~'), '.config', 'fabric', 'patterns')
        selected_patterns_file = os.path.join(os.path.expanduser('~'), '.config', 'fabric', 'selected_patterns.json')
        pattern_manager = PatternManager(patterns_dir, selected_patterns_file)

        logging.info("All components initialized successfully")

        console_utils.print_welcome_banner(console)
        console_utils.print_separator(console)
        console.print("[bold cyan]Chat session started. Type your messages or commands below.[/bold cyan]")
        console_utils.print_separator(console)

        while True:
            user_input = console_utils.get_user_input(console, user_name)
            logging.debug(f"Received user input: {user_input}")
            console_utils.print_separator(console)

            processed_input = prompt_processor.process_input(user_input, chat_hist, tts_enabled)
            logging.debug(f"Processed input type: {processed_input['type']}")

            if processed_input["type"] == "command":
                logging.info(f"User {user_name} entered command: {user_input}")
                if processed_input["content"] == "QUIT":
                    logging.info(f"User {user_name} initiated quit command")
                    break
                if isinstance(processed_input["content"], dict):
                    if processed_input["content"].get("message") == "HANDLE_IN_MAIN":
                        if processed_input["content"]["command"] in ['/savechat', '/sc']:
                            chat_title = console.input("Enter a title for this chat: ")
                            current_chat.title = chat_title
                            chat_id = chat_manager.save_chat(current_chat)
                            console.print(f"Chat saved with title: {chat_title} (ID: {chat_id})")
                            logging.info(f"User {user_name} saved chat: {chat_title} (ID: {chat_id})")
                        elif processed_input["content"]["command"] in ['/listchats', '/lc']:
                            chats = chat_manager.list_chats()
                            for chat in chats:
                                console.print(f"ID: {chat[0]}, Title: {chat[1]}, Created: {chat[2]}")
                            logging.info(f"User {user_name} listed chats")
                        elif processed_input["content"]["command"] in ['/loadchat', '/ldc']:
                            chat_id = console.input("Enter the ID of the chat to load: ")
                            loaded_chat = chat_manager.load_chat(chat_id)
                            if loaded_chat:
                                current_chat = loaded_chat
                                chat_hist = chat_history.convert_chat_to_history(loaded_chat)
                                console.print(f"Loaded chat: {current_chat.title}")
                                logging.info(f"User {user_name} loaded chat: {current_chat.title} (ID: {chat_id})")
                            else:
                                console.print("Chat not found.")
                                logging.warning(f"User {user_name} attempted to load non-existent chat with ID: {chat_id}")
                    else:
                        tts_enabled = processed_input["content"].get("tts_enabled", tts_enabled)
                        if processed_input["content"].get("is_panel"):
                            console.print(processed_input["content"]["message"])
                        elif "message" in processed_input["content"] and isinstance(processed_input["content"]["message"], list):
                            console_utils.print_chat_history(console, processed_input["content"]["message"])
                        else:
                            console_utils.print_command_result(console, processed_input["content"])
                console_utils.print_separator(console)
                continue

            logging.info(f"Processed user input: {processed_input['content']}")

            # Pattern selection
            while True:
                patterns = pattern_manager.get_selected_patterns()
                console.print("\nAvailable patterns:")
                for i, pattern in enumerate(patterns, 1):
                    console.print(f"{i}. {pattern}")
                console.print("0. Edit pattern list")

                try:
                    choice = int(console.input("\nSelect a pattern number: "))
                    if choice == 0:
                        pattern_manager.edit_pattern_list()
                    elif 1 <= choice <= len(patterns):
                        selected_pattern = patterns[choice - 1]
                        system_content = pattern_manager.load_system_content(selected_pattern)
                        console.print(f"\nUsing pattern: {selected_pattern}")
                        break
                    else:
                        console.print("Invalid choice. Please try again.")
                except ValueError:
                    console.print("Invalid input. Please enter a number.")

            try:
                console.print("[bold green]Otto:[/bold green]")
                logging.info("Sending prompt to LLM for response")
                
                # Combine system content with user input
                combined_input = f"{system_content}\n\nUser Input: {processed_input['content']}"
                
                response_text = llm_interaction.stream_llm_response(
                    llm, combined_input, "", chat_hist, console, tts_queue, tts_enabled
                )

                logging.info(f"Received LLM response of length: {len(response_text)}")
                chat_history.add_to_history(chat_hist, user_input, response_text)
                chat_history.save_interaction(user_name, user_input, response_text)

                current_chat.add_message({
                    "user_name": user_name,
                    "user": user_input,
                    "metadata": {
                        "accessCount": 0,
                        "lastAccess": None,
                        "creation": datetime.now().strftime("%Y%m%d_%H%M%S")
                    }
                })
                current_chat.add_message({
                    "user_name": "AI",
                    "agent": response_text,
                    "metadata": {
                        "accessCount": 0,
                        "lastAccess": None,
                        "creation": datetime.now().strftime("%Y%m%d_%H%M%S")
                    }
                })

                # Add the interaction to memory
                search_results = ""
                if "Search results for" in processed_input['content']:
                    search_results = processed_input['content'].split("Question:")[0]
                prompt_processor.add_to_memory(user_input, response_text, search_results)
                logging.info("Added interaction to memory")

                logging.info(f"Chat history updated for user {user_name}")

                console.print()  # Add a blank line
                console_utils.print_copy_instruction(console)

            except Exception as e:
                console.print(f"[bold red]Error during interaction: {str(e)}[/bold red]")
                logging.error(f"Error during interaction: {str(e)}", exc_info=True)

            console_utils.print_separator(console)

    except Exception as e:
        console.print(f"[bold red]Error during application startup: {str(e)}[/bold red]")
        logging.error(f"Error during application startup: {str(e)}", exc_info=True)

    finally:
        console_utils.print_separator(console)
        console.print("[bold cyan]Thank you for using OTTO, your AI Chat Companion. Farewell![/bold cyan]")
        console_utils.print_separator(console)
        if 'tts_queue' in locals() and 'tts_thread' in locals():
            tts_module.cleanup_tts(tts_queue, tts_thread)
        if 'user_name' in locals():
            logging.info(f"Chat application terminated for user {user_name}")
        else:
            logging.info("Chat application terminated")

if __name__ == "__main__":
    run_chat_application()
