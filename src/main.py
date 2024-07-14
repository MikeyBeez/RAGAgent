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

        # Initialize system_content with a default value
        system_content = ""

        logging.info("All components initialized successfully")

        console_utils.print_welcome_banner(console)
        console_utils.print_separator(console)
        console.print("[bold cyan]Chat session started. Type your messages or commands below.[/bold cyan]")
        console_utils.print_separator(console)

        while True:
            user_input = console_utils.get_user_input(console, user_name)
            logging.debug(f"Received user input: {user_input}")
            console_utils.print_separator(console)

            processed_input = prompt_processor.process_input(user_input, chat_hist)
            logging.debug(f"Processed input type: {processed_input['type']}")

            if processed_input["type"] == "command":
                logging.info(f"User {user_name} entered command: {user_input}")
                if processed_input["content"] == "QUIT":
                    logging.info(f"User {user_name} initiated quit command")
                    break
                if isinstance(processed_input["content"], dict):
                    if processed_input["content"].get("message") == "CREATE_NEW_CHAT":
                        chat_title = processed_input["content"]["title"]
                        current_chat = Chat(chat_title)
                        chat_hist.clear()
                        console.print(f"[bold green]Created new chat: {chat_title}[/bold green]")
                    elif processed_input["content"].get("message") == "SAVE_CHAT":
                        chat_manager.save_chat(current_chat)
                        console.print(f"[bold green]Saved chat: {current_chat.title}[/bold green]")
                    elif processed_input["content"].get("message") == "LOAD_CHAT":
                        chat_list = chat_manager.list_chats()
                        for i, chat_info in enumerate(chat_list, 1):
                            console.print(f"{i}. {chat_info[1]} (Created: {chat_info[2]})")
                        selection = int(console.input("Enter the number of the chat to load: "))
                        if 1 <= selection <= len(chat_list):
                            chat_id = chat_list[selection - 1][0]
                            loaded_chat = chat_manager.load_chat(chat_id)
                            if loaded_chat:
                                current_chat = loaded_chat
                                chat_hist = current_chat.messages
                                console.print(f"[bold green]Loaded chat: {current_chat.title}[/bold green]")
                        else:
                            console.print("[bold red]Invalid selection.[/bold red]")
                    elif processed_input["content"].get("message") == "SELECT_PATTERN":
                        patterns = pattern_manager.get_all_patterns()
                        console.print("\nAvailable patterns:")
                        for i, pattern in enumerate(patterns, 1):
                            console.print(f"{i}. {pattern}")
                        
                        while True:
                            try:
                                choice = int(console.input("\nSelect a pattern number: "))
                                if 1 <= choice <= len(patterns):
                                    selected_pattern = patterns[choice - 1]
                                    pattern_manager.select_pattern(selected_pattern)
                                    system_content = pattern_manager.load_system_content(selected_pattern)
                                    console.print(f"\nUsing pattern: {selected_pattern}")
                                    break
                                else:
                                    console.print("Invalid choice. Please try again.")
                            except ValueError:
                                console.print("Invalid input. Please enter a number.")
                    
                    elif processed_input["content"].get("message") == "SHOW_PATTERN":
                        current_pattern = pattern_manager.get_selected_pattern()
                        console.print(f"\nCurrent pattern: {current_pattern}")
                        system_content = pattern_manager.load_system_content(current_pattern)
                        console.print(f"\nSystem content:\n{system_content}")

                    elif processed_input["content"].get("message") == "SHOW_MODEL_SETTINGS":
                        available_models = model_utils.get_available_models()
                        model_settings_text = prompt_processor.get_model_settings_text(available_models)
                        console.print(model_settings_text)
                        
                        while True:
                            user_input = console.input("Enter a setting or model number (or 'q' to quit): ")
                            if user_input.lower() == 'q':
                                break
                            
                            if user_input.startswith('/'):
                                setting, value = user_input.split(maxsplit=1)
                                if setting == "/temperature":
                                    temperature = float(value)
                                    # Update temperature in llm_interaction.stream_llm_response call
                                elif setting == "/topk":
                                    top_k = int(value)
                                    # Update top_k in llm_interaction.stream_llm_response call
                                # Handle other settings similarly
                            else:
                                try:
                                    model_index = int(user_input) - 1
                                    if 0 <= model_index < len(available_models):
                                        selected_model = available_models[model_index]
                                        # Switch to the selected model
                                        llm = model_utils.initialize_model(selected_model)
                                        console.print(f"Switched to model: {selected_model}")
                                    else:
                                        console.print("Invalid model number.")
                                except ValueError:
                                    console.print("Invalid input. Please enter a setting or model number.")

                    else:
                        tts_enabled = processed_input["content"].get("tts_enabled", tts_enabled)
                        if processed_input["content"].get("is_panel"):
                            console.print(processed_input["content"]["message"])
                        else:
                            console_utils.print_command_result(console, processed_input["content"])
                console_utils.print_separator(console)
                continue

            logging.info(f"Processed user input: {processed_input['content']}")

            try:
                console.print("[bold green]Otto:[/bold green]")
                logging.info("Sending prompt to LLM for response")
                
                response_text = llm_interaction.stream_llm_response(
                    llm, system_content, processed_input['content'], chat_hist, console, tts_queue, tts_enabled
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
