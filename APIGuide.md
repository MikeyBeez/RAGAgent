# 📚 OTTO API Guide: The Spellbook of Functions 🧙‍♂️

This grimoire unveils the mystical incantations that breathe life into OTTO, your AI Chat Companion enhanced with the power of Fabric. Within these pages, you'll find the secrets to understanding and extending OTTO's powers.

## 🧠 app.py (The Invocation)

### `run_chat_application()`
This sacred ritual initiates the entire OTTO experience. It summons the necessary modules, manages the chat loop, and guides your AI adventure, now enriched with Fabric patterns.

## 📚 modules/

### 💬 chat_manager.py (Keeper of Conversations)

#### class Chat
- Represents a complete conversation, like a chapter in your AI saga.

  #### `__init__(self, title, messages=None, pattern=None)`
  - `title` (str): The title of the chat, marking its place in your chronicles.
  - `messages` (list, optional): A collection of messages that form the conversation.
  - `pattern` (str, optional): The Fabric pattern used for this chat.

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

#### `add_to_history(chat_history, user_input, ai_response, pattern)`
- `chat_history` (list): The current unfolding conversation history.
- `user_input` (str): Your words of wisdom or insightful questions.
- `ai_response` (str): OTTO's insightful replies and magical pronouncements.
- `pattern` (str): The Fabric pattern used for this exchange.

#### `save_interaction(user_name, user_input, ai_response, pattern)`
- `user_name` (str): The name you've chosen for your AI quest.
- `user_input` (str): Your side of the exchange, recorded for posterity.
- `ai_response` (str): OTTO's response, forever etched in the annals of your chat history.
- `pattern` (str): The Fabric pattern that guided this interaction.

### 💾 create_memories.py (The Memory Weaver)

#### `save_prompt_and_response(user_name, prompt, response, pattern)`
- `user_name` (str): The name you've chosen for this AI odyssey.
- `prompt` (str): Your question or command, prompting OTTO's wisdom.
- `response` (str): OTTO's insightful answer, carefully crafted to guide you.
- `pattern` (str): The Fabric pattern that shaped this memory.

### 🗨️ llm_interaction.py (The AI Conjurer)

#### `setup_prompt_template()`
- Prepares the sacred incantation that summons OTTO's intelligence. 

#### `thinking_animation(console)`
- `console` (Console): The enchanted window where the magic unfolds.

#### `stream_llm_response(llm, system_content, user_input, chat_history, console, tts_queue, tts_enabled)`
- `llm` (Ollama): The AI entity OTTO embodies, ready to converse.
- `system_content` (str): The Fabric pattern's system message, guiding OTTO's behavior.
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

### 🧵 pattern_manager.py (The Pattern Loom)

#### class PatternManager
- The master weaver of Fabric patterns, managing the selection and application of conversational guides.

  #### `__init__(self, patterns_dir, selected_patterns_file)`
  - `patterns_dir` (str): The directory where Fabric patterns are stored.
  - `selected_patterns_file` (str): The file that keeps track of selected patterns.

  #### `load_selected_patterns()`
  - Retrieves the list of currently selected Fabric patterns.

  #### `get_all_patterns()`
  - Returns a list of all available Fabric patterns.

  #### `get_selected_patterns()`
  - Returns the list of currently selected Fabric patterns.

  #### `add_pattern(self, pattern)`
  - `pattern` (str): Adds a new pattern to the selected list.

  #### `remove_pattern(self, pattern)`
  - `pattern` (str): Removes a pattern from the selected list.

  #### `edit_pattern_list()`
  - Allows for interactive editing of the selected pattern list.

  #### `load_system_content(self, pattern_name)`
  - `pattern_name` (str): Loads the system content for a specific Fabric pattern.
  - Returns: The system content (instructions) for the specified pattern.

## 🧪 tests/ (The Proving Grounds)

Within this hallowed hall, the resilience of OTTO's magic is tested. Each module faces rigorous trials to ensure the stability and reliability of its enchantments. Cast `pytest` to witness these trials unfold.

## 🧵 Fabric Patterns

Fabric patterns are the mystic tapestries that guide OTTO's conversational flow. They are stored as Markdown files in the `~/.config/fabric/patterns/` directory.

### Pattern Structure

Each pattern consists of two main components:

1. **System Message**: Contained in `system.md`, this sets the overall behavior and context for OTTO.
2. **User Message Template**: (Optional) Contained in `user.md`, this provides a structure for user inputs.

### Creating Custom Patterns

To weave your own Fabric pattern:

1. Create a new directory in `~/.config/fabric/patterns/` with your pattern name.
2. Within this directory, create `system.md` with your desired system instructions.
3. Optionally, create `user.md` if you want to provide a template for user inputs.
4. Use the PatternManager to add your new pattern to the selected list.

Remember, the power of Fabric lies in its flexibility. Craft your patterns wisely to guide OTTO's responses in the direction of your choosing.

May this grimoire serve you well on your AI adventures! Happy coding, and may OTTO's wisdom, now woven with Fabric, always guide you! ✨
