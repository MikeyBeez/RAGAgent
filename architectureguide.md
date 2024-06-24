# 🧙‍♂️ OTTO's Magical Grimoire: Functions & System Architecture 🏰

Welcome, fellow sorcerers of code! Prepare to unravel the mystical workings of OTTO, your AI Chat Companion. This tome will guide you through the arcane structures and offer insights for weaving your own enchantments.

## 🌟 The Grand Overview

OTTO is a modular spellbook, with each scroll (module) handling specific magical tasks:
OTTO
### 🧠 main.py (The Grand Ritual)
### 📚 modules/
### 💬 chat_manager.py (Conversation Keeper)
### 📜 chat_history.py (Memory Scribe)
### 🎭 command_handler.py (Spell Interpreter)
### 💾 create_memories.py (Memory Crystallizer)
### 🗨️ llm_interaction.py (AI Whisperer)
### 🔮 model_utils.py (Model Summoner)
### 🖥️ console_utils.py (Visual Enchanter)
### 🧩 assemble.py (Context Weaver)
### 🔍 ddg_search.py (Knowledge Seeker)
### 🧪 tests/ (Spell Verification Chamber)

## 🔮 Core Magical Components

### 1. 🧠 The Grand Ritual (main.py)
- Orchestrates the entire magical performance
- Summons other modules and manages the chat loop

### 2. 💬 Conversation Keeper (chat_manager.py)
- Guardians of the Chat Realm
- Saves and loads entire conversations

### 3. 📜 Memory Scribe (chat_history.py)
- Chronicles individual exchanges
- Manages the ebb and flow of chat history

### 4. 🎭 Spell Interpreter (command_handler.py)
- Deciphers and executes magical commands
- Handles special instructions like `/savechat`, `/loadchat`

### 5. 🗨️ AI Whisperer (llm_interaction.py)
- Communes with the AI spirit
- Streams responses with a mesmerizing thinking animation

### 6. 🔮 Model Summoner (model_utils.py)
- Calls forth AI models from the Ollama realm
- Lists available models and initializes the chosen one

### 7. 🖥️ Visual Enchanter (console_utils.py)
- Crafts the visual spectacle of the console
- Manages user input and output with colorful flair

### 8. 🧩 Context Weaver (assemble.py)
- Gathers context to enhance AI understanding
- Performs name recognition and pronoun resolution

### 9. 🔍 Knowledge Seeker (ddg_search.py)
- Ventures into the web to gather relevant information
- Enhances AI responses with current knowledge

## 🎨 Customization Canvases

Harness your creativity and enhance OTTO with these customization opportunities:

1. 🌈 Aesthetic Alchemy (console_utils.py)
   - Modify colors, banners, and text styles
   - Add new visual effects or animations

2. 🧠 Intellect Amplification (llm_interaction.py)
   - Adjust the system message to change OTTO's personality
   - Implement different prompt templates for various use cases

3. 🔍 Knowledge Expansion (assemble.py, ddg_search.py)
   - Integrate additional search engines or knowledge bases
   - Implement more sophisticated context assembly techniques

4. 🎭 Command Crafting (command_handler.py)
   - Add new slash commands for custom functionality
   - Modify existing commands or their behaviors

5. 💾 Memory Manipulation (chat_manager.py, chat_history.py)
   - Implement different storage methods (e.g., database integration)
   - Add features like chat merging or selective memory deletion

6. 🔮 Model Mastery (model_utils.py)
   - Add support for different AI model providers
   - Implement model switching during a chat session

7. 🌐 Web Wizardry
   - Create a web interface for OTTO using a framework like Flask or FastAPI
   - Implement real-time chat updates using WebSockets

## 🧪 Spell Testing

Ensure your enchantments are stable:
- Each scroll has its own test spell in the `tests/` chamber
- Cast `pytest` to verify all magical components

## 🚀 Leveling Up OTTO

As you embark on your customization quest, remember these wise words:

1. 📚 Document your arcane knowledge for future sorcerers
2. 🧹 Keep your code clean and modular for easy enchantment
3. 🛡️ Test your spells thoroughly to prevent magical mishaps
4. 🌟 Share your innovations with the OTTO community!

view the log in the src directory:  

python log_viewer.py --file chat_ollama.log --start-date 2024-06-23 --end-date 2024-06-24 --type INFO --search "AI response"

May your code be bug-free and your AI responses ever insightful! Happy enchanting, code sorcerers! 🧙‍♂️✨
