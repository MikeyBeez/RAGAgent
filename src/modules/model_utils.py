# src/modules/model_utils.py
import subprocess
import logging
from typing import List, Optional
from langchain_community.llms import Ollama

def get_available_models() -> List[str]:
    """
    Retrieves a list of available Ollama models.

    Returns:
        List[str]: A list of model names.
    """
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
        logging.info(f"Retrieved {len(models)} available models")
        return models
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing 'ollama list' command: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error fetching models: {str(e)}")
        return []

def initialize_model(model_name: str) -> Optional[Ollama]:
    """
    Initializes an Ollama model with the given name.

    Args:
        model_name (str): The name of the model to initialize.

    Returns:
        Optional[Ollama]: An initialized Ollama model object, or None if initialization fails.
    """
    try:
        llm = Ollama(model=model_name)
        logging.info(f"Successfully initialized model: {model_name}")
        print(f"Successfully initialized model: {model_name}")
        return llm
    except Exception as e:
        logging.error(f"Error initializing model {model_name}: {str(e)}")
        return None

def switch_model(model_name: str) -> Optional[Ollama]:
    """
    Switches to a different Ollama model.

    Args:
        model_name (str): The name of the model to switch to.

    Returns:
        Optional[Ollama]: An initialized Ollama model object for the new model, or None if switching fails.
    """
    return initialize_model(model_name)

def validate_model(model_name: str) -> bool:
    """
    Validates if a given model name is available.

    Args:
        model_name (str): The name of the model to validate.

    Returns:
        bool: True if the model is available, False otherwise.
    """
    available_models = get_available_models()
    if model_name in available_models:
        logging.info(f"Model {model_name} is available")
        return True
    else:
        logging.warning(f"Model {model_name} is not available")
        return False

def get_model_info(model_name: str) -> Optional[dict]:
    """
    Retrieves information about a specific model.

    Args:
        model_name (str): The name of the model to get information about.

    Returns:
        Optional[dict]: A dictionary containing model information, or None if the information cannot be retrieved.
    """
    try:
        result = subprocess.run(['ollama', 'show', model_name], capture_output=True, text=True, check=True)
        info_lines = result.stdout.strip().split('\n')
        info_dict = {}
        for line in info_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                info_dict[key.strip()] = value.strip()
        logging.info(f"Retrieved information for model: {model_name}")
        return info_dict
    except subprocess.CalledProcessError as e:
        logging.error(f"Error retrieving information for model {model_name}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error retrieving model information: {str(e)}")
        return None
