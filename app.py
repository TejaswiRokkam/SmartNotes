import whisper
import streamlit as st
import subprocess
import os
import torch
import torchaudio
import cohere

# Load Whisper + Cohere
model = whisper.load_model("tiny")
torchaudio.set_audio_backend("soundfile")
co = cohere.Client(st.secrets["COHERE_API_KEY"])

# Set wide layout
st.set_page_config(page_title="SmartNotes", layout="wide")

# ----- HEADER -----
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>📝 SmartNotes</h1>
<p style='text-align: center; font-size: 18px;'>AI-Powered Meeting Minutes Generator from Audio/Video</p>
<hr style="border: 1px solid #bbb;">
""", unsafe_allow_html=True)

# ----- FILE UPLOAD -----
with st.container():
    st.markdown("### 📤 Upload your meeting recording")
    uploaded_file = st.file_uploader("Supports .mp3, .wav, .mp4 files", type=["mp3", "wav", "mp4"])
    st.caption("Max size: 200MB")

# ----- Functions -----
def extract_audio_with_ffmpeg(input_video, output_audio="temp_audio.wav"):
    command = [
        "ffmpeg",
        "-i", input_video,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_audio
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_audio

@st.cache_data(show_spinner=False)
def transcribe_large_audio(audio_path, _model, chunk_length_sec=30):
    transcript = ""
    audio, sr = torchaudio.load(audio_path)
    total_samples = audio.shape[1]
    chunk_size = chunk_length_sec * sr
    for i in range(0, total_samples, chunk_size):
        chunk = audio[:, i:i + chunk_size]
        temp_chunk_path = f"chunk_{i}.wav"
        torchaudio.save(temp_chunk_path, chunk, sr)
        result = model.transcribe(temp_chunk_path)
        transcript += result["text"].strip() + " "
        os.remove(temp_chunk_path)
    return transcript.strip()

def summarize_with_cohere(transcript):
    prompt = f"""
You are an AI assistant specialized in generating formal meeting minutes (MoM).

Summarize the following transcript into structured bullet points that include:
- Attendees and their roles
- Motions passed or decisions made
- Discussions held
- Changes to any bylaws or regulations
- Future actions or next steps

Transcript:
\"\"\"{transcript}\"\"\"

MoM Summary:
"""
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=400,
        temperature=0.5,
    )
    return response.generations[0].text.strip()

# ----- MAIN WORKFLOW -----
if uploaded_file:
    ext = uploaded_file.name.split('.')[-1]
    temp_input = f"temp_input.{ext}"

    with open(temp_input, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🎬 Processing file..."):
        if ext == "mp4":
            audio_path = extract_audio_with_ffmpeg(temp_input)
        else:
            audio_path = temp_input

        transcript = transcribe_large_audio(audio_path, model)

    # --- Tabs for Output ---
    tab1, tab2 = st.tabs(["📜 Transcript", "📝 MoM Summary"])

    with tab1:
        st.markdown("### Full Transcript")
        st.text_area("Transcribed Text", transcript, height=400)

    with tab2:
        st.markdown("### Meeting Summary (MoM)")
        with st.spinner("🔍 Summarizing..."):
            summary = summarize_with_cohere(transcript)
        for line in summary.split("\n"):
            if line.strip():
                st.markdown(f"- {line.strip()}")

    # Cleanup
    os.remove(temp_input)
    if os.path.exists("temp_audio.wav"):
        os.remove("temp_audio.wav")

    st.success("✅ Process Complete")
