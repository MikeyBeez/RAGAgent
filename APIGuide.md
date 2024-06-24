# 📚 OTTO API Guide: The Spellbook of Functions 🧙‍♂️

## 🧠 main.py

### `main()`
The central function that orchestrates the entire OTTO experience.

## 💬 chat_manager.py

### class Chat
Represents a chat session.

#### `__init__(self, title, messages=None)`
- `title` (str): The title of the chat
- `messages` (list, optional): Initial messages for the chat

#### `add_message(self, message)`
- `message` (dict): A message to add to the chat

#### `to_dict(self)`
Returns a dictionary representation of the chat.

### class ChatManager
Manages chat sessions.

#### `__init__(self, db_path='chats.db', chats_dir='chats')`
- `db_path` (str): Path to the SQLite database
- `chats_dir` (str): Directory to store chat files

#### `save_chat(self, chat)`
- `chat` (Chat): The chat to save
Returns: The ID of the saved chat

#### `list_chats(self)`
Returns: A list of tuples containing chat IDs, titles, and creation times

#### `load_chat(self, chat_id)`
- `chat_id` (str): The ID of the chat to load
Returns: A Chat object if found, None otherwise

## 📜 chat_history.py

### `add_to_history(chat_history, user_input, ai_response)`
- `chat_history` (list): The current chat history
- `user_input` (str): The user's input
- `ai_response` (str): The AI's response

### `save_interaction(user_name, user_input, ai_response)`
- `user_name` (str): The name of the user
- `user_input` (str): The user's input
- `ai_response` (str): The AI's response

### `get_memories(memories_dir='memories')`
- `memories_dir` (str): Directory containing memory files
Returns: A list of memory dictionaries

### `populate_chat_history(chat_history, memories)`
- `chat_history` (list): The chat history to populate
- `memories` (list): List of memory dictionaries

### `initialize_chat_history(memories_dir='memories')`
- `memories_dir` (str): Directory containing memory files
Returns: An initialized chat history list

## 🎭 command_handler.py

### `is_command(user_input)`
- `user_input` (str): The user's input
Returns: True if the input is a command, False otherwise

### `handle_command(command, chat_history, tts_enabled)`
- `command` (str): The command to handle
- `chat_history` (list): The current chat history
- `tts_enabled` (bool): Whether text-to-speech is enabled
Returns: A dictionary with the result of the command execution

## 💾 create_memories.py

### `save_prompt_and_response(user_name, prompt, response)`
- `user_name` (str): The name of the user
- `prompt` (str): The user's prompt
- `response` (str): The AI's response

## 🗨️ llm_interaction.py

### `setup_prompt_template()`
Returns: A ChatPromptTemplate object

### `thinking_animation(console)`
- `console` (Console): The Rich console object

### `stream_llm_response(llm, prompt_template, user_input, chat_history, console, tts_queue, tts_enabled)`
- `llm` (Ollama): The language model object
- `prompt_template` (ChatPromptTemplate): The prompt template
- `user_input` (str): The user's input
- `chat_history` (list): The current chat history
- `console` (Console): The Rich console object
- `tts_queue` (Queue): Queue for text-to-speech
- `tts_enabled` (bool): Whether text-to-speech is enabled
Returns: The complete response text

## 🔮 model_utils.py

### `get_available_models()`
Returns: A list of available Ollama models

### `initialize_model(model_name)`
- `model_name` (str): The name of the model to initialize
Returns: An initialized Ollama model object

## 🖥️ console_utils.py

### `setup_console()`
Returns: A Rich Console object

### `print_welcome_banner(console)`
- `console` (Console): The Rich console object

### `print_separator(console)`
- `console` (Console): The Rich console object

### `print_wrapped_text(console, text)`
- `console` (Console): The Rich console object
- `text` (str): The text to print

### `get_user_name(console)`
- `console` (Console): The Rich console object
Returns: The user's chosen name

### `get_model_choice(console, available_models)`
- `console` (Console): The Rich console object
- `available_models` (list): List of available models
Returns: The chosen model name

### `get_user_input(console, user_name)`
- `console` (Console): The Rich console object
- `user_name` (str): The user's name
Returns: The user's input

### `print_command_result(console, result)`
- `console` (Console): The Rich console object
- `result` (dict): The command execution result

### `print_copy_instruction(console)`
- `console` (Console): The Rich console object

### `print_chat_history(console, chat_history)`
- `console` (Console): The Rich console object
- `chat_history` (list): The chat history to print

## 🧩 assemble.py

### class SimpleContextAssembler

#### `__init__(self)`

#### `extract_name(self, text)`
- `text` (str): The text to extract a name from
Returns: The extracted name or None

#### `resolve_pronoun(self, prompt)`
- `prompt` (str): The prompt to resolve pronouns in
Returns: The prompt with resolved pronouns

#### `assemble_context(self, prompt)`
- `prompt` (str): The prompt to assemble context for
Returns: A list of context elements

#### `expand_prompt(self, prompt, context)`
- `prompt` (str): The original prompt
- `context` (list): The assembled context
Returns: The expanded prompt with context

## 🔍 ddg_search.py

### class DDGSearch

#### `__init__(self)`

#### `run_search(self, query)`
- `query` (str): The search query
Returns: A list of search results
