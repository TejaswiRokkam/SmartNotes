# 📝 SmartNotes: AI Meeting Minutes Generator

SmartNotes is an AI-powered web app that lets you **upload meeting audio or video files** and automatically generates **bullet-point meeting summaries (Minutes of Meeting)**. It saves time, improves documentation, and ensures no important discussion is missed.

---

## 🔍 What It Does

✔️ Upload `.mp3`, `.wav`, or `.mp4` files  
🎧 Transcribes audio using OpenAI Whisper  
🧠 Summarizes content using Cohere’s LLM into clean bullet points  
📋 Displays both the transcript and MoM summary in a simple UI  
🚀 Supports long meetings, chunked audio processing  
💯 Runs locally or can be deployed to the web

---

## 🛠️ Tech Stack

| Purpose              | Technology               |
|----------------------|--------------------------|
| Frontend UI          | Streamlit                |
| Transcription        | Whisper (via OpenAI or local) |
| Summarization        | Cohere LLM               |
| Audio/Video Handling | FFmpeg, Torchaudio       |
| Language             | Python                   |

---

## 🛠️ Installation

> ⚠️ Python 3.8 or higher required

1. Clone the repo
git clone https://github.com/TejaswiRokkkam/SmartNotes.git

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```
4. Install dependencies
```bash
pip install -r requirements.txt
```
---

## 🔐 Setup API Keys
1. Inside the project folder, create a hidden folder called .streamlit
2. Inside .streamlit, create a file called secrets.toml
3. Paste the following inside secrets.toml:
```bash
COHERE_API_KEY = "your-cohere-api-key"
```
---

## ▶️ Run the App
```bash
streamlit run app.py
```
Go to your browser and open: http://localhost:8501
