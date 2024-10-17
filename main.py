import streamlit as st
import sounddevice as sd
import numpy as np
import whisper
import re
import scipy.io.wavfile as wav
import tempfile
import os
import subprocess

# Check if FFmpeg is installed in Windows
def is_ffmpeg_installed():
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        st.error("FFmpeg is not available. Please ensure FFmpeg is installed and configured in your system's PATH.")
        return False

# Load Whisper model
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

model = load_whisper_model()

def record_audio(duration=10, sample_rate=16000):
    st.write("Recording...")
    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        st.write("Recording complete!")
        return audio.flatten()
    except sd.PortAudioError:
        st.error("Error accessing the microphone. Please check your audio settings.")
        return None

def save_audio(audio, sample_rate=16000):
    _, temp_path = tempfile.mkstemp(suffix=".wav")
    wav.write(temp_path, sample_rate, audio)
    return temp_path

def transcribe_audio(audio_path):
    # Use Windows path directly
    result = model.transcribe(audio_path)
    return result["text"]

def extract_info(text):
    name_pattern = r"(?i)my name is (\w+)"
    phone_pattern = r"(?i)my phone (?:number|no) is (\d{10})"
    email_pattern = r"(?i)my email (?:address|id) is ([\w\.-]+@[\w\.-]+)"
    
    name = re.search(name_pattern, text)
    phone = re.search(phone_pattern, text)
    email = re.search(email_pattern, text)
    
    return {
        "name": name.group(1) if name else "",
        "phone": phone.group(1) if phone else "",
        "email": email.group(1) if email else ""
    }

st.title("Voice-based Form Submission")

# Check if FFmpeg is installed before proceeding
if not is_ffmpeg_installed():
    st.error("FFmpeg is not installed. Please install FFmpeg and ensure it's added to your system's PATH.")
    st.stop()

if st.button("Record Audio"):
    audio = record_audio()
    if audio is not None:
        audio_path = save_audio(audio)
        
        st.audio(audio_path)
        
        transcription = transcribe_audio(audio_path)
        st.write("Transcription:")
        st.write(transcription)
        
        info = extract_info(transcription)
        
        st.write("Extracted Information:")
        name = st.text_input("Name", value=info["name"])
        phone = st.text_input("Phone Number", value=info["phone"])
        email = st.text_input("Email", value=info["email"])
        
        if st.button("Submit"):
            st.success("Form submitted successfully!")
        
        # Clean up temporary file
        os.remove(audio_path)
