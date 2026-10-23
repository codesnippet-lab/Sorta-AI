
# Sorta — AI Downloads Butler 🪄

Sorta is a file-organization assistant that uses a locally running Gemma model
to suggest folders for your files. You can review the suggestions before
taking any action.

## Features

- Upload multiple files in a Streamlit interface
- Use local Gemma AI through Ollama to suggest folders
- Preview the proposed organization
- Keep the user in control: this prototype does not move, rename, or delete files

## Built with

- Python
- Streamlit
- Ollama
- Gemma 3 1B

## Run locally

### 1. Install Ollama

Install Ollama for your operating system:
https://ollama.com/download

### 2. Download Gemma

Open a terminal and run:

```bash
ollama pull gemma3:1b
```

Ensure Ollama is running.

### 3. Set up Sorta

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Launch the app

```bash
streamlit run app.py
```

Open the local URL printed in your terminal.

## Privacy and safety

Sorta sends filenames to the locally running Gemma model to generate folder
suggestions. This prototype does not send file contents to an external AI
service and does not modify files on your computer.

## Current limitations

- Suggestions are based on filenames, not file contents.
- Moving files and undo are not implemented yet.
- Ollama and Gemma must be installed locally.
