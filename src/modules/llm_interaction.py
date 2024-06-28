# src/modules/llm_interaction.py
# This module has the system message and does animation.
# More importantly it talks to the LLM and returns a stream of text.  

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules import console_utils
import time
import threading
import logging

def setup_prompt_template():
    logging.info("Setting up prompt template")
    template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI named Otto, you answer questions with informative and accurate responses. You never lie, and you are careful not to halucinate responses.  You try to limit your responses to three paragraphs unless you think you need more to answer properly.  If you are correcting code, you always give the full file and not just the edit."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    logging.debug("Prompt template created")
    return template

def thinking_animation(console):
    logging.debug("Starting thinking animation")
    animation = "|/-\\"
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]  # Rich color names
    i = 0
    while getattr(threading.current_thread(), "do_run", True):
        color = colors[i % len(colors)]
        message = f"[bold {color}]Otto is thinking {animation[i % len(animation)]}"
        console.print(message, end="\r")
        i += 1
        time.sleep(0.5)
    console.print(" " * len(message), end="\r") # Clear the line using the message length
    logging.debug("Thinking animation stopped")

def stream_llm_response(llm, prompt_template, user_input, chat_history, console, tts_queue, tts_enabled):
    logging.info(f"Streaming LLM response for user input: {user_input}")
    response_text = ""
    buffer = ""

    # Log the assembled prompt
    logging.info("Assembled prompt:")
    logging.info(prompt_template)

    # Start the thinking animation in a separate thread
    t = threading.Thread(target=thinking_animation, args=(console,))
    t.start()
    logging.debug("Thinking animation thread started")

    try:
        for chunk in llm.stream(prompt_template.format(input=user_input, chat_history=chat_history)):
            response_text += chunk
            buffer += chunk
            if "\n" in buffer or len(buffer) > 50:
                lines = buffer.split("\n")
                for line in lines[:-1]:
                    console_utils.print_wrapped_text(console, line)
                    console.print()
                    if tts_enabled:
                        tts_queue.put(line)
                        logging.debug(f"Added to TTS queue: {line}")
                buffer = lines[-1]
    except Exception as e:
        logging.error(f"Error during LLM streaming: {str(e)}")
        raise

    # Stop the animation thread
    t.do_run = False
    t.join()
    logging.debug("Thinking animation thread stopped")

    if buffer:
        console_utils.print_wrapped_text(console, buffer)
        if tts_enabled:
            tts_queue.put(buffer)
            logging.debug(f"Added final buffer to TTS queue: {buffer}")

    logging.info(f"LLM response streaming completed. Response length: {len(response_text)}")
    return response_text
