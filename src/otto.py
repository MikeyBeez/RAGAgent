import streamlit as st
import sys
import os
import logging
from datetime import datetime

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.initializer import initialize_app
from src.modules import console_utils, llm_interaction, chat_history, model_utils
from src.modules.chat_manager import Chat
from src.modules.process_prompt import ProcessPrompt
from src.modules.pattern_manager import PatternManager

def initialize_streamlit_app():
    if 'app_components' not in st.session_state:
        app_components = initialize_app()
        st.session_state.app_components = app_components
        st.session_state.current_chat = Chat("Untitled Chat")
        st.session_state.pattern_manager = PatternManager(
            os.path.join(os.path.expanduser('~'), '.config', 'fabric', 'patterns'),
            os.path.join(os.path.expanduser('~'), '.config', 'fabric', 'selected_patterns.json')
        )
        st.session_state.system_content = ""
        st.session_state.chat_history = []

def main():
    st.set_page_config(page_title="OTTO - AI Chat Companion", layout="wide")
    initialize_streamlit_app()

    st.title("OTTO - Your AI Chat Companion")

    # Sidebar for settings and commands
    with st.sidebar:
        st.header("Settings")
        if st.button("Select Model"):
            select_model()
        if st.button("Select Fabric Pattern"):
            select_pattern()
        if st.button("Save Chat"):
            save_chat()
        if st.button("Load Chat"):
            load_chat()
        if st.button("Clear Chat"):
            clear_chat()

    # Main chat interface
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.text_area("You:", value=message['content'], height=100, disabled=True)
            else:
                st.text_area("OTTO:", value=message['content'], height=200, disabled=True)

    # User input
    user_input = st.text_input("Your message:", key="user_input")
    if st.button("Send") or (user_input and st.session_state.get('user_input_submitted', False)):
        if user_input:
            process_user_input(user_input)
            st.session_state.user_input_submitted = True
        else:
            st.warning("Please enter a message before sending.")

    # Reset the submitted flag if the input is empty
    if not user_input:
        st.session_state.user_input_submitted = False

def process_user_input(user_input):
    prompt_processor = ProcessPrompt()
    processed_input = prompt_processor.process_input(user_input, st.session_state.chat_history)

    if processed_input["type"] == "prompt":
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get AI response
        llm = st.session_state.app_components['llm']
        response_text = llm_interaction.stream_llm_response(
            llm, 
            st.session_state.system_content, 
            processed_input['content'], 
            st.session_state.chat_history, 
            None,  # console is not used in Streamlit version
            None,  # tts_queue is not used in Streamlit version
            False  # tts_enabled is always False in Streamlit version
        )

        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

        # Save interaction to memory
        prompt_processor.add_to_memory(user_input, response_text)

        # Force a rerun to update the chat display
        st.experimental_rerun()

    elif processed_input["type"] == "command":
        # Handle commands (you may need to implement command handling for Streamlit)
        st.warning(f"Command detected: {user_input}. Command handling not fully implemented in Streamlit version.")

def select_model():
    available_models = model_utils.get_available_models()
    selected_model = st.selectbox("Choose a model:", available_models)
    if selected_model:
        llm = model_utils.initialize_model(selected_model)
        if llm:
            st.session_state.app_components['llm'] = llm
            st.success(f"Switched to model: {selected_model}")
        else:
            st.error(f"Failed to initialize model: {selected_model}")

def select_pattern():
    patterns = st.session_state.pattern_manager.get_all_patterns()
    selected_pattern = st.selectbox("Choose a Fabric pattern:", patterns)
    if selected_pattern:
        st.session_state.pattern_manager.select_pattern(selected_pattern)
        st.session_state.system_content = st.session_state.pattern_manager.load_system_content(selected_pattern)
        st.success(f"Selected pattern: {selected_pattern}")

def save_chat():
    chat_title = st.text_input("Enter a title for this chat:")
    if chat_title:
        st.session_state.current_chat.title = chat_title
        st.session_state.current_chat.messages = st.session_state.chat_history
        st.session_state.app_components['chat_manager'].save_chat(st.session_state.current_chat)
        st.success(f"Chat saved: {chat_title}")

def load_chat():
    chat_list = st.session_state.app_components['chat_manager'].list_chats()
    chat_titles = [chat[1] for chat in chat_list]
    selected_chat = st.selectbox("Select a chat to load:", chat_titles)
    if selected_chat:
        chat_id = chat_list[chat_titles.index(selected_chat)][0]
        loaded_chat = st.session_state.app_components['chat_manager'].load_chat(chat_id)
        if loaded_chat:
            st.session_state.current_chat = loaded_chat
            st.session_state.chat_history = loaded_chat.messages
            st.success(f"Loaded chat: {loaded_chat.title}")

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.current_chat = Chat("Untitled Chat")
    st.success("Chat cleared")

if __name__ == "__main__":
    main()
