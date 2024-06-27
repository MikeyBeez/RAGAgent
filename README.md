# 🤖 OTTO - Your Intelligent Conversational Companion

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
OTTO is a work in progress.  I just switched from command_handler.py to process_prompt.py but I haven't updated the documentation yet.  Until I get a release version, expect documentation mismatches.  

OTTO is a cutting-edge AI chat agent for macOS, leveraging the power of LangChain, Ollama, and various tools to create an engaging and intelligent conversational experience. Dive into the future of AI interaction with OTTO!

## ✨ Current Features

- 🧠 Advanced chat functionality using Ollama with the Llama3 model
- 📜 Robust chat history management (keep it under 15 for optimal performance!)
- 🎨 Rich, colorful console interface for enhanced readability
- 🗣️ Text-to-speech functionality using macOS's built-in 'say' command
- 📋 Easy interaction copying to clipboard
- 📊 Chat history statistics and management

## 🚀 New & Exciting Updates

- 🖼️ Image recognition capabilities with `visual.py` (Google's multimodal models)
- 🎭 Stylish, terminal-like help display
- 📏 New commands: `/lengthchathistory` and `/copychathistory`
- 🌈 Enhanced visual appeal with colorful OTTO banner

## 🔮 Planned Features

- 🧩 Context assembly for improved conversation coherence
- 🔍 Integration of external tools (e.g., web search, calculator)
- 🧭 Intelligent routing between LLM and tools
- 🧠 Enhanced context management and coreference resolution
- 🔄 Expanded model options

## 🛠️ Setup

1. Ensure you have Python 3.8+ installed on your Mac
2. Set up a Conda environment (recommended)
3. Install required packages:

   ```bash
   pip install -r requirements.txt

Ensure Ollama is installed and running on your macOS system
Pull the Llama3 model:

    ```bash
    ollama pull llama3


🚀 Usage
Run the chat application:

    ``` bash
    cd src
    python main.py

🎛️ Commands

/talk: Enable text-to-speech
/notalk: Disable text-to-speech
/copy: Copy the last interaction to clipboard
/printchathistory: Display chat history
/truncate n: Keep last n entries in history
/clearchathistory: Clear all chat history
/lengthchathistory: Show number of interactions
/copychathistory: Copy full history to clipboard
/help: Display all available commands
/quit: Exit the application

💡 Pro Tip: Keep your chat history under 15 interactions for the best experience!  
   You can do this using slash commands. /lengthchathistory will show you how many
   items are in your chat history.  /truncate 10 will delete older entries.  
   If you want to group chat history, /savechat will save the old entries to a file
   before you truncate.
🎙️ Speech-to-Text
Use macOS's built-in dictation:

Enable in System Preferences > Keyboard > Dictation
Use the keyboard shortcut (default: press Fn twice) to start dictation

🌟 Project Status
OTTO is evolving rapidly! We've recently added new commands, enhanced the visual appeal, and improved history management. Stay tuned for more exciting updates!
🤝 Contributing
While OTTO is primarily a personal project, we welcome ideas and discussions. Feel free to fork the repository and experiment!
📜 License
MIT License

<p align="center">
  Made with ❤️ by AI enthusiasts
</p>


