# src/modules/llm_interaction.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import logging

def setup_prompt_template():
    logging.info("Setting up prompt template")
    template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI named Otto, you answer questions with informative and accurate responses. You never lie, and you are careful not to hallucinate responses. You try to limit your responses to three paragraphs unless you think you need more to answer properly. If you are correcting code, you always give the full file and not just the edit."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    logging.debug("Prompt template created")
    return template

def stream_llm_response(llm, prompt_template, user_input, chat_history, console, tts_queue, tts_enabled):
    logging.info(f"Streaming LLM response for user input: {user_input}")
    response_text = ""

    try:
        # Prepare the formatted prompt
        if isinstance(prompt_template, ChatPromptTemplate):
            formatted_prompt = prompt_template.format_messages(input=user_input, chat_history=chat_history)
        elif isinstance(prompt_template, str):
            formatted_prompt = prompt_template + "\n\nUser Input: " + user_input
        else:
            raise ValueError("prompt_template must be either a ChatPromptTemplate or a string")
        
        for chunk in llm.stream(formatted_prompt):
            response_text += chunk
            # In Streamlit, we don't need to handle console output or TTS here
            # The full response will be displayed once it's complete

    except Exception as e:
        logging.error(f"Error during LLM streaming: {str(e)}")
        response_text = f"Error during LLM streaming: {str(e)}"

    logging.info(f"LLM response streaming completed. Response length: {len(response_text)}")
    return response_text
