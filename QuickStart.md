🧭 gettingstarted.md: Charting Your Course 🧭

# 🚀 Getting Started with OTTO - Your AI Chat Companion 🤖

Welcome, brave explorer, to the realm of OTTO! Prepare yourself for an adventure in artificial intelligence like no other. This guide will equip you with all you need to embark on your journey.

## 🧰 Prerequisites: Gathering Your Mystical Artifacts 🧰

Before we begin our quest, ensure you have these magical artifacts:

- 🐍 Python 3.8+ (The Serpent of Wisdom)
- 🧙‍♂️ Ollama (The Enchanted Model Summoner)
- 🦙 Llama3 model (The Mystical Beast of Knowledge)

All of these should be installed on your trusty macOS steed.

## 🏗️ Installation:  Unveiling the Grimoire 🏗️

1. 📥 Clone the sacred repository:
   
```bash
   git clone https://github.com/MikeyBeez/RAGAgent.git
   cd RAGAgent
```

🌈 Create a magical Conda environment (recommended):

```bash
conda create -n otto-env python=3.9
conda activate otto-env
content_copy
```

📚 Install the required scrolls of power:
```bash
pip install -r requirements.txt
```

🧠 Summon the SpaCy language model:
```bash
python -m spacy download en_core_web_sm
```

🎭 Running OTTO: Awakening the AI Spirit 🎭
🏰 Enter the source chamber:
```bash
cd src
cd ..
```

🔮 Awaken OTTO:
```bash
python app.py
```

📝 Choose your adventurer name and select your AI companion

🎮 Basic Usage: Conversing with the AI Sage 🎮

💬 Converse with OTTO by typing your messages.

🔍 Use magical commands by starting with a /.

/help: Reveal all available spells.

/savechat: Preserve your conversation for future generations.

/loadchat: Recall a conversation from the annals of history.

🗃️ The Archives: Where Memories Linger 🗃️

Your journey will be chronicled in two mystical formats:

📜 Memory Scrolls: Individual exchanges stored as JSON in the memories directory.

📚 Chat Tomes: Full conversations preserved as JSON in the chats directory.

🎨 Customization: Tailoring OTTO to Your Liking 🎨

OTTO is adaptable to your preferences:

🦜 Choose from a variety of AI models at startup.

🔊 Toggle text-to-speech with /talk and /notalk.

🎤 Use dictation to speak to Otto -- Fn Fn (macOS).

🌐 Adjust context gathering from the vast knowledge of the web.

🏆 Pro Tips for Aspiring AI Wizards 🏆

💡 Keep your chat history under 15 interactions for optimal performance.

🔄 Use /truncate to manage long conversations.

📋 Quickly copy interactions with /copy.

🆘 Troubleshooting: Banishing Mystical Anomalies 🆘

If you encounter any mystical anomalies:

Ensure Ollama is running and the chosen model is available.
Check the chat_ollama.log for clues.
Consult the Council of Elders (aka open an issue on GitHub).
🌟 Embark on Your Adventure! 🌟
You're now ready to explore the vast realms of knowledge with OTTO. May your conversations be insightful, your learning boundless, and your experience magical!

Remember, brave adventurer, with great AI comes great responsibility. Use OTTO wisely and ethically!

Happy chatting! 🎉🤖🚀
