# RAGAgent

# AI Chat Agent Project for macOS

## Overview

This is a nascent project to create an AI chat agent for macOS using LangChain, Ollama, and various tools. The agent is designed to engage in conversations, use external tools, and provide informative responses.

You should also look at the file visual.py as it uses googl'e multimodel models to do image recognition tasks.  This is a working standalone program that I want to integrate into this project.

## Current Features

- Basic chat functionality using Ollama with the Llama3 model
- Chat history management
- Rich console interface for enhanced readability
- Logging for debugging and monitoring
- Text-to-speech functionality for spoken responses using macOS's built-in 'say' command
- Option to copy interactions to clipboard

## Planned Features

- Context assembly for improved conversation coherence
- Integration of external tools (e.g., web search, calculator)
- Intelligent routing between LLM and tools
- Enhanced context management and coreference resolution
- Expanded model options

## Setup

1. Ensure you have Python 3.8+ installed on your Mac
2. Set up a Conda environment (recommended)
3. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

Ensure Ollama is installed and running on your macOS system
Pull the Llama3 model:

    ```bash
    ollama pull llama3
    ```

Usage
Run the chat application:

    ```bash
    cd src
    python main.py
    ```


Enter your prompts when prompted.
Type '/talk' to enable text-to-speech.
Type '/notalk' to disable text-to-speech.
Type 'copy' to copy the last interaction to clipboard.
Type '/quit' to exit the application.

For speech-to-text input, you can use macOS's built-in dictation feature:

Enable dictation in System Preferences > Keyboard > Dictation
Use the keyboard shortcut (default is pressing Fn twice) to start dictation when prompted for input

Project Status
This project is in active development. We recently added text-to-speech functionality using macOS's 'say' command and the ability to copy interactions. The Llama3 model is currently used for improved performance, especially with historical and general knowledge questions. Expect frequent updates and potential breaking changes as new features are implemented and the architecture evolves.
Contributing
As this is a personal project in its early stages, we're not actively seeking contributions at this time. However, feel free to fork the repository and experiment with your own modifications.
License
MIT license
Copy
This updated README.md now includes:

1. A specification in the title that this is for macOS.
2. Mention of the 'say' command for text-to-speech in the Current Features section.
3. Instructions on how to use macOS's built-in dictation feature for speech-to-text input in the Usage section.
4. Updated Setup instructions to clarify that this is for macOS systems.

These changes make it clear that the project is designed for macOS and takes advantage of some of its built-in features for both text-to-speech and speech-to-text functionality. CopyRetryClaude does not have the ability to run the code it generates yet.Claude can make mistakes. Please double-check responses.
