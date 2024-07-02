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
   ```

4. 🧠 Summon the SpaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. 🧵 Weave the Fabric patterns:
   ```bash
   mkdir -p ~/.config/fabric/patterns
   cp -R patterns/* ~/.config/fabric/patterns/
   ```
6. cp config_sample.py config.py
   set your model and user name

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
- Verify that Fabric patterns are properly installed in `~/.config/fabric/patterns/`.
- Consult the Council of Elders (aka open an issue on GitHub).

## 🌟 Embark on Your Adventure! 🌟

You're now ready to explore the vast realms of knowledge with OTTO, guided by the wisdom of Fabric patterns. May your conversations be insightful, your learning boundless, and your experience magical!

Remember, brave adventurer, with great AI comes great responsibility. Use OTTO wisely and ethically!

Happy chatting! 🎉🤖🚀
