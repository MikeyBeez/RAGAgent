✨ Alas, brave adventurer! You've stumbled upon the grimoire of... ✨

🤖 OTTO - Your Intelligent Conversational Companion 🦜

🚀 Embark on Your AI Quest! 🚀

See the video!  https://www.youtube.com/watch?v=YJAc-D-WXC4&t=191s  

<p align="center">
<pre>
         🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
       🔵        ████████          ████████       🔵 
       🟠        ██    ██          ██    ██       🟠  
       🟢        ██  * ██    TT    ██ *  ██       🟢  
       🟣        ██    ██          ██    ██       🟣  
       🔴        ████████          ████████       🔴  
         🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦
         ❤️               ❤️    ❤️              ❤️                
          ❤️    ❤️                       ❤️    ❤️  
           ❤️           ❤️        ❤️          ❤️
            ❤️               ❤️             ❤️  
              ❤️                          ❤️    
                ❤️                      ❤️      
                  ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️      
                  *~ *~ *~ *~ *~ *~ *~ *~


                          🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
                          🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
</pre>
</p>

OTTO is a cutting-edge AI chat agent for macOS, now enhanced with the power of Fabric! Combining LangChain, Ollama, and Fabric's pattern-based approach, OTTO offers an immersive and intelligent conversational experience. Prepare to embark on an extraordinary adventure in artificial intelligence! 🚀

Young apprentice wizards can find additional scrolls of maps, spells, and rituals in the chamber of documentation.  After chanting the README, wise apprentices will find the chamber of documentation and chant the quickstart spells.  

## ✨ Features: A Treasure Trove of AI Wonders ✨

🧠 **Advanced Chat**: Engage in thought-provoking conversations with OTTO, powered by Ollama and its Llama3 model.

🎭 **Fabric Patterns**: Utilize a variety of pre-defined conversation patterns to guide and enhance your interactions.

📜 **Chat History**: Relive past exchanges and track the twists and turns of your AI adventure.

🎨 **Colorful Console**: A visually stunning interface enhances your journey with vibrant colors and readability.

🗣️ **Text-to-Speech**: Listen as OTTO's words come to life through the mystical powers of macOS's built-in 'say' command.

📋 **Clipboard Conjuring**: Copy interactions with ease and share your AI discoveries with the world.

📊 **Chat Insights**: Delve into the statistics of your conversations and manage the annals of your AI history.

🔍 **Web Quest (/search)**: Unleash the power of DuckDuckGo search directly within OTTO.

🧠 **Memory Recall (/memory)**: OTTO remembers! Search past conversations using embeddings and RAG.

## 🚀 Embark on Your AI Quest! 🚀

1. **Gather Your Artifacts**:
   - 🐍 Python 3.8+ (The Serpent of Wisdom)
   - 🧙‍♂️ Ollama (The Enchanted Model Summoner)
   - 🦙 gemma2 model (The Mystical Beast of Knowledge)
   - 🧵 Fabric (The Loom of Patterns)

2. **Installation Incantation**:
   ```bash
   git clone https://github.com/MikeyBeez/RAGAgent.git
   cd RAGAgent
   conda create -n otto-env python=3.9
   conda activate otto-env
   pip install -r requirements.txt
   cp config_sample.py config.py
   python -m spacy download en_core_web_sm
   cd src
   cd ..
   python app.py
   ```

3. **Choose Your Path**:
   - Select your adventurer name and your AI companion (from the available models).
   - Choose a Fabric pattern to guide your conversation.

4. **Command Your Quest**:
   - 💬 Type your messages naturally, as if speaking to a wise sage.
   - 🔍 Use magical slash commands to control your destiny:
     - `/help`: Reveal the ancient scrolls of available commands.
     - `/chat <title>`: Create a new chat with the given title.
     - `/savechat`: Preserve your current conversation for eternity.
     - `/loadchat`: Summon a past conversation from the archives.
     - `/search <query>`: Embark on a web search without leaving OTTO's presence.
     - `/memory <query>`, `/m <query>`: Journey through your past conversations to find relevant knowledge.
     - `/fabric`, `/f`: Choose a new Fabric pattern for your conversation.
     - `/showpattern`, `/sp`: Display the current Fabric pattern and its mystical content.

## 🧙‍♂️ Sharing Code with the AI Sage 🧙‍♂️

To share your arcane code with OTTO, use this potent incantation in your terminal:

```bash
find . -type f -not \( -path "*/__pycache__/*" -o -path "./src/archive/*" -o -path "./src/experiments/*" -o -path "./src/tests/*" -o -name "*.db" -o -name "*.pyc" -o -name "*.json" -o -name "config*" -o -path "*/chats/*" -o -path "./memories/*" -o -name "*.log" -o -name "*pytest*" -o -path "*/.git/*" \) -exec sh -c 'if file -b --mime-type "$1" | grep -qE "^text/"; then echo "--- $1 ---"; cat "$1"; fi' _ {} \; | pbcopy
```

This mystical command will gather all relevant code files, ignoring those in the forbidden realms, and copy them to your clipboard. Paste the result into your chat with OTTO, and the AI sage shall parse your code with ease.

## 🏆 A Bard's Advice for a Successful Quest 🏆

💡 Experiment with different Fabric patterns to discover new depths in your conversations.

🔄 Use `/truncate` to keep your chat history manageable and ensure optimal performance.

📋 Quickly copy interactions to your clipboard with `/copy`.

🆘 If you encounter any mystical anomalies, consult the scrolls within the `chat_ollama.log` or seek guidance from the Council of Elders (open an issue on GitHub).

📜 Chat Persistence and Management
OTTO provides a flexible chat management system that allows you to create, save, and load chats. However, it's important to understand how chat persistence works to ensure you don't lose your valuable conversations.

When you start a new chat using the /chat <title> command, the chat is created in memory but not automatically saved.

To persist a chat and ensure it's available for future sessions, you must explicitly save it using the /savechat command.

If you exit the app without saving the current chat, the chat will be lost and cannot be recovered.

To continue a previous conversation, use the /loadchat command to select and load a saved chat.

The /listchats command displays a list of all saved chats, allowing you to choose which one to load.

Remember to save your chats frequently to avoid losing your progress!

🌟 May Your Conversations Be Ever Insightful! 🌟
