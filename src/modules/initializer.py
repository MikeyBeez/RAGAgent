# src/modules/initializer.py

import logging
from rich.console import Console
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.modules import model_utils, chat_history, chat_manager, console_utils, tts_module, llm_interaction, process_prompt
import config

def initialize_logging():
    logging.basicConfig(filename='chat_ollama.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting chat application")

def initialize_console():
    console = console_utils.setup_console()
    logging.info("Console setup complete")
    return console

def initialize_user(console):
    user_name = config.USERNAME
    if user_name == "User":
        user_name = console_utils.get_user_name(console)
        # Update config file with the new username
        update_config('USERNAME', user_name)
    logging.info(f"User {user_name} started a new session")
    return user_name

def initialize_model(console):
    available_models = model_utils.get_available_models()
    model_name = config.MODEL_NAME
    if model_name not in available_models:
        model_name = console_utils.get_model_choice(console, available_models)
        # Update config file with the new model name
        update_config('MODEL_NAME', model_name)
    logging.info(f"User selected model: {model_name}")
    llm = model_utils.initialize_model(model_name)
    if llm is None:
        raise Exception("Failed to initialize the model")
    logging.info(f"Model {model_name} initialized successfully")
    return llm

def initialize_chat_components():
    chat_hist = chat_history.initialize_chat_history(user_name)
    tts_enabled = config.TTS_ENABLED
    tts_queue = tts_module.setup_tts_queue()
    tts_thread = tts_module.start_tts_thread(tts_queue)
    logging.info("Chat history and TTS setup complete")
    return chat_hist, tts_enabled, tts_queue, tts_thread

def initialize_chat_manager():
    chat_mgr = chat_manager.ChatManager()
    logging.info("Chat manager initialized")
    return chat_mgr

def initialize_prompt_components():
    prompt_template = llm_interaction.setup_prompt_template()
    prompt_processor = process_prompt.ProcessPrompt()
    logging.info("Prompt components initialized")
    return prompt_template, prompt_processor

def update_config(key, value):
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.py')
    with open(config_path, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if line.startswith(f"{key} = "):
            lines[i] = f"{key} = \"{value}\"\n"
            break
    
    with open(config_path, 'w') as f:
        f.writelines(lines)

def initialize_app():
    initialize_logging()
    console = initialize_console()
    user_name = initialize_user(console)
    llm = initialize_model(console)
    chat_hist, tts_enabled, tts_queue, tts_thread = initialize_chat_components()
    chat_mgr = initialize_chat_manager()
    prompt_template, prompt_processor = initialize_prompt_components()
    
    return {
        'console': console,
        'user_name': user_name,
        'llm': llm,
        'chat_hist': chat_hist,
        'tts_enabled': tts_enabled,
        'tts_queue': tts_queue,
        'tts_thread': tts_thread,
        'chat_manager': chat_mgr,
        'prompt_template': prompt_template,
        'prompt_processor': prompt_processor
    }
