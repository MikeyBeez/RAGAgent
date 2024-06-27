# main.py

import logging
from datetime import datetime
from rich.console import Console
from modules import tts_module, model_utils, console_utils, chat_history, llm_interaction
from modules.chat_manager import Chat, ChatManager
from langchain_core.messages import HumanMessage, AIMessage
from modules.process_prompt import ProcessPrompt

def main():
    # Setup logging
    logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting chat application")

    # Setup console
    console = console_utils.setup_console()
    logging.info("Console setup complete")

    # Display welcome banner
    console_utils.print_welcome_banner(console)

    # Get user name
    user_name = console_utils.get_user_name(console)
    logging.info(f"User {user_name} started a new session")

    # Setup model
    available_models = model_utils.get_available_models()
    model_name = console_utils.get_model_choice(console, available_models)
    logging.info(f"User selected model: {model_name}")
    llm = model_utils.initialize_model(model_name)

    if llm is None:
        console.print("[bold red]Failed to initialize the model. Exiting...[/bold red]")
        logging.error(f"Failed to initialize model {model_name}. Exiting application.")
        return

    logging.info(f"Model {model_name} initialized successfully")

    # Setup chat history and TTS
    chat_hist = chat_history.initialize_chat_history()
    tts_enabled = False
    tts_queue = tts_module.setup_tts_queue()
    tts_thread = tts_module.start_tts_thread(tts_queue)
    logging.info("Chat history and TTS setup complete")

    # Setup prompt template
    prompt_template = llm_interaction.setup_prompt_template()
    logging.info("Prompt template setup complete")

    # Setup chat manager
    chat_manager = ChatManager()
    current_chat = Chat("Untitled Chat")
    logging.info("Chat manager initialized")

    # Setup prompt processor
    prompt_processor = ProcessPrompt()
    logging.info("Prompt processor initialized")

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
                            chat_hist = []
                            for message in loaded_chat.messages:
                                if 'user' in message:
                                    chat_hist.append(HumanMessage(content=message['user']))
                                elif 'agent' in message:
                                    chat_hist.append(AIMessage(content=message['agent']))
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

    console_utils.print_separator(console)
    console.print("[bold cyan]Thank you for using OTTO, your AI Chat Companion. Farewell![/bold cyan]")
    console_utils.print_separator(console)

    tts_module.cleanup_tts(tts_queue, tts_thread)
    logging.info(f"Chat application terminated for user {user_name}")

if __name__ == "__main__":
    main()
