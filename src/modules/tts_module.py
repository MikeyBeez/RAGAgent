# modules/tts_module.py
import subprocess
import threading
import queue
import time

def speak_text(text):
    try:
        time.sleep(0.5)  # Add a 0.5-second delay before speaking
        subprocess.run(['say', text], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in text-to-speech: {e}")

def tts_worker(tts_queue):
    while True:
        text = tts_queue.get()
        if text is None:
            break
        speak_text(text)
        tts_queue.task_done()

def setup_tts_queue():
    return queue.Queue()

def start_tts_thread(tts_queue):
    tts_thread = threading.Thread(target=tts_worker, args=(tts_queue,))
    tts_thread.start()
    return tts_thread

def cleanup_tts(tts_queue, tts_thread):
    tts_queue.put(None)
    tts_thread.join()
