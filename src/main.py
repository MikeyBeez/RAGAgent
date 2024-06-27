# src/main.py
import sys
import os
import logging
from datetime import datetime

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.initializer import initialize_app
from src.modules import console_utils, llm_interaction, tts_module, chat_history, model_utils
from src.modules.chat_manager import Chat
import config

def run_chat_application():
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
        prompt_template = app_components['prompt_template']
        prompt_processor = app_components['prompt_processor']

        console_utils.print_welcome_banner(console)
        console_utils.print_separator(console)
        console.print("[bold cyan]Chat session started. Type your messages or commands below.[/bold cyan]")
        console_utils.print_separator(console)

        while True:
            user_input = console_utils.get_user_input(console, user_name)
            console_utils.print_separator(console)

            processed_input = prompt_processor.process_input(user_input, chat_hist, tts_enabled)

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
                        elif processed_input["content"]["command"] == "model":
                            available_models = model_utils.get_available_models()
                            console.print("[bold cyan]Available models:[/bold cyan]")
                            for i, model in enumerate(available_models, 1):
                                console.print(f"{i}. {model}")
                            model_choice = console.input("[bold yellow]Enter the number of the model you want to use (or press Enter to keep the current model): [/bold yellow]")
                            if model_choice.isdigit() and 1 <= int(model_choice) <= len(available_models):
                                new_model = available_models[int(model_choice) - 1]
                                llm = model_utils.switch_model(new_model)
                                console.print(f"[bold green]Switched to model: {new_model}[/bold green]")
                            elif model_choice == "":
                                console.print("[bold yellow]Keeping the current model.[/bold yellow]")
                            else:
                                console.print("[bold red]Invalid choice. Keeping the current model.[/bold red]")
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

            try:
                console.print("[bold green]Otto:[/bold green]")
                response_text = llm_interaction.stream_llm_response(
                    llm, prompt_template, processed_input['content'], chat_hist, console, tts_queue, tts_enabled
                )

                logging.info(f"AI response: {response_text}")
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
