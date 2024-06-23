# src/modules/model_utils.py
# This shows available models and initializes the user's model of choice.

import subprocess
from langchain_community.llms import Ollama

def get_available_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
        return models
    except Exception as e:
        print(f"Error fetching models: {str(e)}")
        return []

def initialize_model(model_name):
    try:
        return Ollama(model=model_name)
    except Exception as e:
        print(f"Error initializing the model: {str(e)}")
        return None
