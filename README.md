# streamlit-applications
Any apps made using streamlit for AI and ML projects.

---
# Knowledge Graph
 -- *All credits go to user @thu_vu92*

This application is a simple streamlit based web interface to take in any summarized text data for a show,movie or any other media for which we have a synopsis.

It extracts graph entities(entities & relationships) from text input using Lang graph and OpenAi's gpt4-o, and uses Pyviz to create a visualized representation of knowledge graph, in order to summarize information through a DAG(Directed Acyclic Graph).


## Features
- Creates a knowledge graph from inputed text file (file extension .txt).
- Creates a knowledge graph from input text (in text area).

## Installation
You need to have Python>=3.8 installed, and preferable a code editor like VScode.

Download & Run the *requirements.txt* file using the below command:
`pip install -r requirements.txt`
You can set it up in a new virtual environment if needed.

### Prerequisites
- Python>=3.8
- Open AI API keys (Go to [Open AI API keys](https://platform.openai.com/account/api-keys), and create an API key)

You might need to store the secret credentail key from Open AI inside a .env file with the name `OPENAI_API_KEY`

### Run the app
To run the above app, in your terminal or powershell, just type:
`streamlit run app.run`
and it will open a new window in your browser to run this app. 

Note: If you get some prompts in the command shell for email, etc, just press enter and keep it running.

For closing this app, press `Ctrl+C` in the terminal to close.

---

