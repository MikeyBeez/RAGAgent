# app.py
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import run_chat_application

if __name__ == "__main__":
    run_chat_application()

