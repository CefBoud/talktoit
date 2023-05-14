# 📞 Talktoit
Talktoit is a way to launch an Web interface and talk to your data using a LLM. As of now, you can supply a URL and you API key, build your index and start cooking in less than 5 min.


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