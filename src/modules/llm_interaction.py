# src/modules/llm_interaction.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules import console_utils
import time
import threading
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

def thinking_animation(console):
    logging.debug("Starting thinking animation")
    animation = "|/-\\"
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]  # Rich color names
    i = 0
    while getattr(threading.current_thread(), "do_run", True):
        color = colors[i % len(colors)]
        message = f"[bold {color}]Otto is thinking {animation[i % len(animation)]}"
        padding = "*" * (30 - len(message))  # Adjust the number as needed
        padded_message = f"{message}{padding}"
        console.print(padded_message, end="\r")
        i += 1
        time.sleep(0.5)
    console.print(" " * len(padded_message), end="\r") # Clear the line using the padded message length
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
        # Prepare the formatted prompt
        if isinstance(prompt_template, ChatPromptTemplate):
            formatted_prompt = prompt_template.format_messages(input=user_input, chat_history=chat_history)
        elif isinstance(prompt_template, str):
            formatted_prompt = prompt_template + "\n\nUser Input: " + user_input
        else:
            raise ValueError("prompt_template must be either a ChatPromptTemplate or a string")
        
        for chunk in llm.stream(formatted_prompt):
            response_text += chunk
            buffer += chunk
            if "\n" in buffer or len(buffer) > 50:
                lines = buffer.split("\n")
                for line in lines[:-1]:
                    padded_line = line.ljust(30, '*')  # Adjust the number as needed
                    console_utils.print_wrapped_text(console, padded_line)
                    console.print()
                    if tts_enabled:
                        tts_queue.put(line)
                        logging.debug(f"Added to TTS queue: {line}")
                buffer = lines[-1]
    except ValueError as e:
        logging.error(f"ValueError in prompt handling: {str(e)}")
        console.print(f"[bold red]Error in prompt handling: {str(e)}[/bold red]")
    except Exception as e:
        logging.error(f"Error during LLM streaming: {str(e)}")
        console.print(f"[bold red]Error during LLM streaming: {str(e)}[/bold red]")
    finally:
        # Stop the animation thread
        t.do_run = False
        t.join()
        logging.debug("Thinking animation thread stopped")

        if buffer:
            padded_buffer = buffer.ljust(30, '*')  # Adjust the number as needed
            console_utils.print_wrapped_text(console, padded_buffer)
            if tts_enabled:
                tts_queue.put(buffer)
                logging.debug(f"Added final buffer to TTS queue: {buffer}")

    logging.info(f"LLM response streaming completed. Response length: {len(response_text)}")
    return response_text
