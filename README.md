# 📞 Talktoit
Talktoit is a way to launch an Web interface and talk to your data using a LLM. As of now, you can supply a URL and you API key, build your index and start cooking in less than 5 min.

# 🤔 Why build this ?
The most obvious and honest answer is for the heck of it. To have fun and tinker with these fascinating technological bricks.

A more dreamy and ambtious anwser is to have something that lowers the entry barrier and makes it easier to play in the LLM ecosystem through a nice and simple UI.

# What next ?
Some ideas that come to mind regarding the evolution of this extermely modest project are
- More elaborate scraping. Scrapy is wonderfully rich and can be leveraged more.
- Use other sources of data in step 1 instead of a website: 
    - Youtube/audio with a transcripe API or Model (Whisper ?)
    - PDFs
    - Other text sources?
- use different LLMs in step 2, maybe llama.cpp to enable offline mode without GPU?
- Conversation history using LangChain

# 🧐 Demo


![](demo.gif)


# 💻  Install

```
git clone https://github.com/CefBoud/talktoit.git
cd talktoit

# optional virtualenv step
python -m venv .venv
source .venv/bin/activate
# end virtualenv

pip install -r requirements.txt
```

# 🚀 Launch

```
# https://platform.openai.com/account/api-keys
export OPENAI_API_KEY=<openai key>

source .venv/bin/activate # if installed in virtualenv

python main.py --server_port 8888
```

Go to localhost:8888 and enjoy 😃!

# 🔧 Dependencies
The main third-party package requirements are:
- `llama_index`
-  `openai`
- `langchain`
- `gradio`
- `scrapy`