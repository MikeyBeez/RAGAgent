✨ Alas, brave adventurer! You've stumbled upon the grimoire of... ✨

🤖 OTTO - Your Intelligent Conversational Companion 🦜

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
This is OTTO's first release version!  I'm continuing development in the new fabric branch.  You can switch there by pressing what currently says main on RAGAgent's github page.    

OTTO is a cutting-edge AI chat agent for macOS, imbued with the power of LangChain, Ollama, and various mystical artifacts to create an immersive and intelligent conversational experience. Prepare to embark on an extraordinary adventure in artificial intelligence! 🚀


✨ Features: A Treasure Trove of AI Wonders ✨

🧠 Advanced Chat: Engage in thought-provoking conversations with OTTO, powered by the mighty Ollama and its Llama3 model.

📜 Chat History: Relive past exchanges and track the twists and turns of your AI adventure (keep it under 15 for optimal enchantment!).

🎨 Colorful Console: A visually stunning interface enhances your journey with vibrant colors and readability.

🗣️ Text-to-Speech: Listen as OTTO's words come to life through the mystical powers of macOS's built-in 'say' command.

📋 Clipboard Conjuring: Copy interactions with ease and share your AI discoveries with the world.

📊 Chat Insights: Delve into the statistics of your conversations and manage the annals of your AI history.

🔍 Web Quest (/search): Unleash the power of DuckDuckGo search directly within OTTO and enrich your conversations with knowledge from the vast digital realm.

🧠 Memory Recall (/memory): OTTO remembers! Utilize the /memory command to search past conversations using the magic of embeddings and RAG (Retrieval Augmented Generation).

🚀 Embark on Your AI Quest! 🚀

1. Gather Your Artifacts:

🐍 Python 3.8+ (The Serpent of Wisdom)

🧙‍♂️ Ollama (The Enchanted Model Summoner)

🦙 Llama3 model (The Mystical Beast of Knowledge)

Ensure these relics are properly installed on your macOS system.

2. Installation Incantation:

```bash
git clone https://github.com/MikeyBeez/RAGAgent.git
cd RAGAgent
conda create -n otto-env python=3.9
conda activate otto-env
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd src
cd ..
python app.py
```
Use code with caution.
3. Choose Your Path:

Select your adventurer name and your AI companion (from the available models).
4. Command Your Quest:

💬 Type your messages naturally, as if speaking to a wise sage.

🔍 Use magical slash commands to control your destiny:

/help: Reveal the ancient scrolls of available commands.

/savechat: Preserve your current conversation for eternity.

/loadchat: Summon a past conversation from the archives.

/search [query]: Embark on a web search without leaving OTTO's presence.

/memory [query]: Journey through your past conversations to find relevant knowledge.

...and many more! Discover them all with /help.

🏆 A Bard's Advice for a Successful Quest 🏆

💡 Keep your chat history under 15 interactions for optimal performance. (Use /truncate to manage lengthy sagas.)

🔄 Remember to use /truncate to keep your chat history manageable.

📋 Quickly copy interactions to your clipboard with /copy.

🆘 If you encounter any mystical anomalies, consult the scrolls within the chat_ollama.log or seek guidance from the Council of Elders (open an issue on GitHub).

🌟 May Your Conversations Be Ever Insightful! 🌟
