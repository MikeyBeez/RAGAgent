# modules/chat_history.py
import logging
import json
import os
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

def add_to_history(chat_history, user_input, ai_response):
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=ai_response))

def save_interaction(user_name, user_input, ai_response):
    from modules.create_memories import save_prompt_and_response
    save_prompt_and_response(user_name, user_input, ai_response)

def get_memories(username, num_memories=10, memories_dir='memories'):
    logging.info(f"Attempting to load memories for user: {username}")
    logging.info(f"Looking in directory: {memories_dir}")
    
    if not os.path.exists(memories_dir):
        os.makedirs(memories_dir)
        logging.info(f"Created memories directory: {memories_dir}")
        return []

    memory_files = [f for f in os.listdir(memories_dir) if f.endswith('.json')]
    memory_files.sort(reverse=True)  # Sort in descending order to get newest first
    
    logging.info(f"Found {len(memory_files)} total memory files")
    
    memories = []
    for file in memory_files:
        file_path = os.path.join(memories_dir, file)
        try:
            with open(file_path, 'r') as f:
                memory = json.load(f)
            if memory.get('user_name') == username:
                memories.append(memory)
                logging.info(f"Added memory from file: {file} for user {username}")
                if len(memories) >= num_memories:
                    break
        except json.JSONDecodeError:
            logging.warning(f"Skipped invalid JSON file: {file}")
    
    logging.info(f"Loaded {len(memories)} memories for user {username}")
    
    # Sort memories by timestamp if available, otherwise by filename
    memories.sort(key=lambda x: x.get('metadata', {}).get('creation', x.get('filename', '')), reverse=True)
    
    return memories[:num_memories]

def populate_chat_history(chat_history, memories):
    for memory in memories:
        chat_history.append(HumanMessage(content=memory['user']))
        chat_history.append(AIMessage(content=memory['agent']))

def initialize_chat_history(username, num_memories=10, memories_dir='memories'):
    chat_history = []
    memories = get_memories(username, num_memories, memories_dir)
    populate_chat_history(chat_history, memories)
    return chat_history

def convert_chat_to_history(chat):
    history = []
    for message in chat.messages:
        if 'user' in message:
            history.append(HumanMessage(content=message['user']))
        elif 'agent' in message:
            history.append(AIMessage(content=message['agent']))
    return history
