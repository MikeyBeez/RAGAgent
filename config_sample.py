# config.py
import os

DEFAULT_USERNAME = "User"
USERNAME = os.environ.get("OTTO_USERNAME", DEFAULT_USERNAME)

# Add other configuration variables here
MODEL_NAME = os.environ.get("OTTO_MODEL", "default_model_name")
TTS_ENABLED = os.environ.get("OTTO_TTS_ENABLED", "False").lower() == "true"
GAPI = "Add your Google Search API Key Here."
