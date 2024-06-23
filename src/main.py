# main.py

import logging
from rich.console import Console
from modules import tts_module, model_utils, console_utils, chat_history, command_handler, llm_interaction

def main():
    # Setup logging
    logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting chat application")

    # Setup console
    console = console_utils.setup_console()

    # Display welcome banner
    console_utils.print_welcome_banner(console)

    # Get user name
    user_name = console_utils.get_user_name(console)

    # Setup model
    available_models = model_utils.get_available_models()
    model_name = console_utils.get_model_choice(console, available_models)
    llm = model_utils.initialize_model(model_name)

    if llm is None:
        console.print("[bold red]Failed to initialize the model. Exiting...[/bold red]")
        return

    # Setup chat history and TTS
    chat_hist = []
    tts_enabled = False
    tts_queue = tts_module.setup_tts_queue()
    tts_thread = tts_module.start_tts_thread(tts_queue)

    # Setup prompt template
    prompt_template = llm_interaction.setup_prompt_template()

    console_utils.print_separator(console)
    console.print("[bold cyan]Chat session started. Type your messages or commands below.[/bold cyan]")
    console_utils.print_separator(console)

    while True:
        user_input = console_utils.get_user_input(console, user_name)
        console_utils.print_separator(console)

        if command_handler.is_command(user_input):
            command_result = command_handler.handle_command(user_input, chat_hist, tts_enabled)
            if command_result == "QUIT":
                break
            if isinstance(command_result, dict):
                tts_enabled = command_result.get("tts_enabled", tts_enabled)

                # Correctly handle printing chat history:
                if "message" in command_result and isinstance(command_result["message"], list):
                    console_utils.print_chat_history(console, command_result["message"])
                else:
                    console_utils.print_command_result(console, command_result)

            console_utils.print_separator(console)
            continue

        logging.info(f"User input: {user_input}")

        try:
            console.print("[bold green]Otto:[/bold green]")
            response_text = llm_interaction.stream_llm_response(
                llm, prompt_template, user_input, chat_hist, console, tts_queue, tts_enabled
            )

            logging.info(f"AI response: {response_text}")
            chat_history.add_to_history(chat_hist, user_input, response_text)
            chat_history.save_interaction(user_input, response_text)

            console.print()  # Add a blank line
            console_utils.print_copy_instruction(console)

        except Exception as e:
            console.print(f"[bold red]Error during interaction: {str(e)}[/bold red]")
            logging.error(f"Error during interaction: {str(e)}")

        console_utils.print_separator(console)

    console_utils.print_separator(console)
    console.print("[bold cyan]Thank you for using OTTO, your AI Chat Companion. Farewell![/bold cyan]")
    console_utils.print_separator(console)

    tts_module.cleanup_tts(tts_queue, tts_thread)
    logging.info("Chat application terminated")

if __name__ == "__main__":
    main()
