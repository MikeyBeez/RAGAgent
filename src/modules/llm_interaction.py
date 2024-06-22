from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from modules import console_utils
import time
import threading

def setup_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system", "You are an AI named Otto, you answer questions with informative and accurate responses."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

def thinking_animation(console):
    animation = "|/-\\"
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]  # Rich color names
    i = 0
    while getattr(threading.currentThread(), "do_run", True):
        color = colors[i % len(colors)]
        message = f"[bold {color}]Otto is thinking {animation[i % len(animation)]}"
        console.print(message, end="\r")
        i += 1
        time.sleep(0.5)
    console.print(" " * len(message), end="\r") # Clear the line using the message length

def stream_llm_response(llm, prompt_template, user_input, chat_history, console, tts_queue, tts_enabled):
    response_text = ""
    buffer = ""

    # Start the thinking animation in a separate thread
    t = threading.Thread(target=thinking_animation, args=(console,))
    t.start()

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
            buffer = lines[-1]

    # Stop the animation thread
    t.do_run = False
    t.join()

    if buffer:
        console_utils.print_wrapped_text(console, buffer)
        if tts_enabled:
            tts_queue.put(buffer)

    return response_text
