# RAGAgent

# AI Chat Agent Project

## Overview

This is a nascent project to create an AI chat agent using LangChain, Ollama, and various tools. The agent is designed to engage in conversations, use external tools, and provide informative responses.

## Current Features

- Basic chat functionality using Ollama with the Llama3 model
- Chat history management
- Rich console interface for enhanced readability
- Logging for debugging and monitoring

## Planned Features

- Context assembly for improved conversation coherence
- Integration of external tools (e.g., web search, calculator)
- Intelligent routing between LLM and tools
- Enhanced context management and coreference resolution
- Expanded model options

## Setup

1. Ensure you have Python 3.8+ installed
2. Set up a Conda environment (recommended)
3. Install required packages:

4. Ensure Ollama is installed and running on your system
5. Pull the Llama3 model:  

```bash
ollama pull llama3
```

## Usage

Run the chat application:

```bash
cd src
python chat_ollama.py
```

Enter your prompts when prompted. Type 'quit' to exit the application.

## Project Status

This project is in its early stages of development. We recently switched from the Gemma:2b model to Llama3 for improved performance, especially with historical and general knowledge questions. Expect frequent updates and potential breaking changes as new features are implemented and the architecture evolves.

## Contributing

As this is a personal project in its early stages, we're not actively seeking contributions at this time. However, feel free to fork the repository and experiment with your own modifications.

## License

MIT license 
