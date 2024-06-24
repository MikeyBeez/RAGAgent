# modules/chat_history.py
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

def get_memories(memories_dir='memories'):
    #print(f"Getting memories from {memories_dir}")
    memory_files = [f for f in os.listdir(memories_dir) if f.endswith('.json')]
    memory_files.sort(reverse=True)  # Sort in descending order
    
    print(f"Found  and loaded {len(memory_files)} memory files")
    
    memories = []
    for file in memory_files:
        file_path = os.path.join(memories_dir, file)
        #print(f"Reading file: {file_path}")
        try:
            with open(file_path, 'r') as f:
                memory = json.load(f)
            memories.append(memory)
            #print(f"Added memory from {file}")
        except json.JSONDecodeError:
            print(f"Skipped invalid JSON file: {file}")
    
    print(f"Returning {len(memories)} memories")
    return memories

def populate_chat_history(chat_history, memories):
    for memory in memories:
        chat_history.append(HumanMessage(content=memory['user']))
        chat_history.append(AIMessage(content=memory['agent']))

def initialize_chat_history(memories_dir='memories'):
    chat_history = []
    memories = get_memories(memories_dir)
    populate_chat_history(chat_history, memories)
    return chat_history
