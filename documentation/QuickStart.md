# 🧭 Getting Started with OTTO - Your AI Chat Companion with Fabric 🧭

Welcome, brave explorer, to the realm of OTTO! Prepare yourself for an adventure in artificial intelligence like no other, now enhanced with the power of Fabric. This guide will equip you with all you need to embark on your journey.

## 🧰 Prerequisites: Gathering Your Mystical Artifacts 🧰

Before we begin our quest, ensure you have these magical artifacts:

- 🐍 Python 3.8+ (The Serpent of Wisdom)
- 🧙‍♂️ Ollama (The Enchanted Model Summoner)
- 🦙 Llama3 model (The Mystical Beast of Knowledge)
- 🧵 Fabric (The Loom of Patterns)

All of these should be installed on your trusty macOS steed.

## 🏗️ Installation: Unveiling the Grimoire 🏗️

1. 📥 Clone the sacred repository:
   ```bash
   git clone https://github.com/MikeyBeez/RAGAgent.git
   cd RAGAgent
   ```

2. 🌈 Create a magical Conda environment (recommended):
   ```bash
   conda create -n otto-env python=3.9
   conda activate otto-env
   ```

3. 📚 Install the required scrolls of power:
   ```bash
   pip install -r requirements.txt
   pip install fabric
   ```

4. 🧠 Summon the SpaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. 🧵 Install Fabric:
   - Navigate to where you want the Fabric project to live on your system in a semi-permanent place on your computer.
   ```bash
   # Find a home for Fabric
   cd /where/you/keep/code
   ```
   - Clone the Fabric project to your computer.
   ```bash
   # Clone Fabric to your computer
   git clone https://github.com/danielmiessler/fabric.git
   ```
   - Enter Fabric's main directory.
   ```bash
   # Enter the project folder (where you cloned it)
   cd fabric
   ```
   - Install pipx:
     - macOS:
     ```bash
     brew install pipx
     ```
     - Linux:
     ```bash
     sudo apt install pipx
     ```
     - Windows: Use WSL and follow the Linux instructions.
   - Install Fabric:
   ```bash
   pipx install .
   ```
   - Run setup:
   ```bash
   fabric --setup
   ```
   - Restart your shell to reload everything.
   - Test Fabric by running the help command:
   ```bash
   fabric --help
   ```

6. 🔧 Configure OTTO:
   - Copy the `config_sample.py` file to `config.py`:
   ```bash
   cp config_sample.py config.py
   ```
   - Open `config.py` in your favorite text editor and set your desired model and user name.

Note: To update the Fabric patterns, rerun `fabric --setup`. Patterns are updated almost daily, so if you want the latest, make sure to run this command regularly.

## 🎭 Running OTTO: Awakening the AI Spirit 🎭

1. 🏰 Enter the source chamber:
    cd into the project root.   
 



2. 🔮 Awaken OTTO:
   ```bash
   python app.py
   ```

3. 📝 Choose your adventurer name and select your AI companion

4. 🎨 Select a Fabric pattern to guide your conversation

## 🎮 Basic Usage: Conversing with the AI Sage 🎮

- 💬 Converse with OTTO by typing your messages.
- 🔍 Use magical commands by starting with a /.
  - `/help`: Reveal all available spells.
  - `/savechat`: Preserve your conversation for future generations.
  - `/loadchat`: Recall a conversation from the annals of history.
  - `/pattern`: Choose a new Fabric pattern for your conversation.

## 🗃️ The Archives: Where Memories Linger 🗃️

Your journey will be chronicled in two mystical formats:

- 📜 Memory Scrolls: Individual exchanges stored as JSON in the `memories` directory.
- 📚 Chat Tomes: Full conversations preserved as JSON in the `chats` directory.

## 🎨 Customization: Tailoring OTTO to Your Liking 🎨

OTTO is adaptable to your preferences:

- 🦜 Choose from a variety of AI models at startup.
- 🔊 Toggle text-to-speech with `/talk` and `/notalk`.
- 🎤 Use dictation to speak to Otto -- Fn Fn (macOS).
- 🌐 Adjust context gathering from the vast knowledge of the web.
- 🧵 Create custom Fabric patterns to guide conversations on specific topics.

## 🏆 Pro Tips for Aspiring AI Wizards 🏆

- 💡 Experiment with different Fabric patterns to discover new conversation dynamics.
- 🔄 Use `/truncate` to manage long conversations and maintain optimal performance.
- 📋 Quickly copy interactions with `/copy`.
- 🧠 Use `/memory` to recall relevant information from past conversations.

## 🆘 Troubleshooting: Banishing Mystical Anomalies 🆘

If you encounter any mystical anomalies:

- Ensure Ollama is running and the chosen model is available.
- Check the `chat_ollama.log` for clues.
- Verify that Fabric patterns are properly installed by running `fabric --help`.
- Consult the Council of Elders (aka open an issue on GitHub).

## 🌟 Embark on Your Adventure! 🌟

You're now ready to explore the vast realms of knowledge with OTTO, guided by the wisdom of Fabric patterns. May your conversations be insightful, your learning boundless, and your experience magical!

Remember, brave adventurer, with great AI comes great responsibility. Use OTTO wisely and ethically!

Happy chatting! 🎉🤖🚀
