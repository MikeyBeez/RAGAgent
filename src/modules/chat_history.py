# modules/chat_history.py
from langchain_core.messages import HumanMessage, AIMessage
from modules.create_memories import save_prompt_and_response

def add_to_history(chat_history, user_input, ai_response):
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=ai_response))

def save_interaction(user_input, ai_response):
    save_prompt_and_response(user_input, ai_response)
