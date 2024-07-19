import base64
import sys
import time
import pyautogui
from PIL import Image
import io
import os
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import subprocess

load_dotenv()

# Configure the Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables")
    sys.exit(1)
genai.configure(api_key=api_key)

print("Gemini API configured successfully")

class ScreenCapture:
    def __init__(self):
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def capture(self, size=(640, 480)):
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.resize(size)
        screenshot = screenshot.convert('RGB')  # Convert to RGB mode

        # Save the screenshot to a file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.jpg"
        filepath = os.path.join(self.screenshot_dir, filename)
        screenshot.save(filepath)
        print(f"Screenshot saved: {filepath}")

        # Return the image as bytes
        buffered = io.BytesIO()
        screenshot.save(buffered, format="JPEG")
        return buffered.getvalue()

class Assistant:
    def __init__(self):
        print("Initializing Gemini model...")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini model initialized")

    def answer(self, prompt, image):
        if not prompt:
            return

        print("Prompt:", prompt)

        try:
            image_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(image).decode()
                }
            ]
            
            response = self.model.generate_content([prompt, image_parts[0]])
            
            print("Response:", response.text)

            if response.text:
                self._tts(response.text)
        except Exception as e:
            print(f"Error generating response: {e}")

    def _tts(self, response):
        try:
            subprocess.run(["say", response])
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

screen_capture = ScreenCapture()
assistant = Assistant()
recognizer = sr.Recognizer()

def listen_and_process():
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Audio captured. Recognizing...")
            prompt = recognizer.recognize_google(audio)
            print("You said:", prompt)
            image = screen_capture.capture()
            assistant.answer(prompt, image)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    print("Starting the assistant. Press 'l' to listen, 'q' to quit.")
    while True:
        key = input("Press 'l' to listen or 'q' to quit: ").lower()
        if key == 'q':
            print("Quitting...")
            break
        elif key == 'l':
            print("Initiating listening...")
            listen_and_process()
        else:
            print("Invalid input. Please press 'l' to listen or 'q' to quit.")

    print("Assistant stopped.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

