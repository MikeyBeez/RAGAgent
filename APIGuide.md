# 📚 OTTO API Guide: The Spellbook of Functions 🧙‍♂️

This grimoire unveils the mystical incantations that breathe life into OTTO, your AI Chat Companion. Within these pages, you'll find the secrets to understanding and extending OTTO's powers.

## 🧠 app.py (The Invocation)

### `run_chat_application()`
This sacred ritual initiates the entire OTTO experience. It summons the necessary modules, manages the chat loop, and guides your AI adventure.

## 📚 modules/

### 💬 chat_manager.py (Keeper of Conversations)

#### class Chat
- Represents a complete conversation, like a chapter in your AI saga.

  #### `__init__(self, title, messages=None)`
  - `title` (str): The title of the chat, marking its place in your chronicles.
  - `messages` (list, optional): A collection of messages that form the conversation.

  #### `add_message(self, message)`
  - `message` (dict): A single exchange between you and OTTO, added to the ongoing conversation.

  #### `to_dict(self)`
  - Transforms the chat object into a dictionary, suitable for storage or sharing.

#### class ChatManager
- The grand librarian of conversations, managing the storage and retrieval of entire chats.

  #### `__init__(self, db_path='chats.db', chats_dir='chats')`
  - `db_path` (str): The location of the SQLite database where chat metadata is stored.
  - `chats_dir` (str): The directory where the full conversation scrolls are kept.

  #### `save_chat(self, chat)`
  - `chat` (Chat): The conversation to be preserved for posterity.

  #### `list_chats(self)`
  - Unveils a list of all saved chats, allowing you to revisit past adventures.

  #### `load_chat(self, chat_id)`
  - `chat_id` (str): The unique identifier of the chat you wish to summon.

### 📜 chat_history.py (Chronicler of Exchanges)

#### `add_to_history(chat_history, user_input, ai_response)`
- `chat_history` (list): The current unfolding conversation history.
- `user_input` (str): Your words of wisdom or insightful questions.
- `ai_response` (str): OTTO's insightful replies and magical pronouncements.

#### `save_interaction(user_name, user_input, ai_response)`
- `user_name` (str): The name you've chosen for your AI quest.
- `user_input` (str): Your side of the exchange, recorded for posterity.
- `ai_response` (str): OTTO's response, forever etched in the annals of your chat history.

#### `get_memories(memories_dir='memories')`
- `memories_dir` (str): The directory where OTTO's memories are stored.
- Returns: A treasure trove of past interactions, each a shimmering memory.

#### `populate_chat_history(chat_history, memories)`
- `chat_history` (list): The chat history to be populated with the echoes of the past.
- `memories` (list): A collection of memories to be woven into the current conversation.

#### `initialize_chat_history(memories_dir='memories')`
- `memories_dir` (str): The path to the chamber of memories.
- Returns: An initialized chat history, ready to capture new adventures.

### 💾 create_memories.py (The Memory Weaver)

#### `save_prompt_and_response(user_name, prompt, response)`
- `user_name` (str): The name you've chosen for this AI odyssey.
- `prompt` (str): Your question or command, prompting OTTO's wisdom.
- `response` (str): OTTO's insightful answer, carefully crafted to guide you.

### 🗨️ llm_interaction.py (The AI Conjurer)

#### `setup_prompt_template()`
- Prepares the sacred incantation that summons OTTO's intelligence. 

#### `thinking_animation(console)`
- `console` (Console): The enchanted window where the magic unfolds.

#### `stream_llm_response(llm, prompt_template, user_input, chat_history, console, tts_queue, tts_enabled)`
- `llm` (Ollama): The AI entity OTTO embodies, ready to converse.
- `prompt_template` (ChatPromptTemplate): The structure of the incantation used to summon OTTO's knowledge.
- `user_input` (str): Your query or command, setting the course of the conversation.
- `chat_history` (list): The tapestry of past exchanges, providing context to OTTO's responses.
- `console` (Console): The mystical display where the conversation unfolds.
- `tts_queue` (Queue): A queue for messages to be spoken aloud by the text-to-speech enchantment.
- `tts_enabled` (bool): A flag indicating whether OTTO's responses should be spoken aloud. 
- Returns: The AI's complete response, a stream of wisdom from the depths of its knowledge.

### 🔮 model_utils.py (The Model Summoner)

#### `get_available_models()`
- Summons a list of AI entities OTTO can embody, each with its own unique powers.

#### `initialize_model(model_name)`
- `model_name` (str): The chosen AI entity for OTTO to embody.
- Returns: An initialized AI model, ready to engage in conversation.

### 🖥️ console_utils.py (Master of the Visual Arts)

This module governs the visual aspects of your AI journey, painting the console with colors, banners, and user-friendly prompts. It's here that you can customize the aesthetics of your interaction with OTTO.  

### 🧩 assemble.py (Guardian of Context)

#### class SimpleContextAssembler
- A master of weaving together past interactions and external knowledge to provide OTTO with a richer understanding of your requests.

### 🔍 ddg_search.py (Seeker of Web Knowledge)

#### class DDGSearch
- A powerful tool that allows OTTO to venture into the vast expanse of the web, retrieving information to enhance its responses and provide you with the most accurate and up-to-date knowledge.

##  🧪  tests/ (The Proving Grounds)

Within this hallowed hall, the resilience of OTTO's magic is tested. Each module faces rigorous trials to ensure the stability and reliability of its enchantments. Cast `pytest` to witness these trials unfold.

May this grimoire serve you well on your AI adventures! Happy coding, and may OTTO's wisdom always guide you! ✨
