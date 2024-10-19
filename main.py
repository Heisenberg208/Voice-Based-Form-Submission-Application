import streamlit as st
import sounddevice as sd
import numpy as np
import re
import tempfile
import os
import speech_recognition as sr
import soundfile as sf

# Initialize recognizer
recognizer = sr.Recognizer()

def record_audio(duration=10, sample_rate=16000):
    st.write("Recording...")
    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        st.write("Recording complete!")
        return audio
    except sd.PortAudioError:
        st.error("Error accessing the microphone. Please check your audio settings.")
        return None

def save_audio(audio, sample_rate=16000):
    # Use NamedTemporaryFile so the file can be automatically cleaned up
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)  # `delete=False` ensures file is not deleted until we manually do it
    sf.write(temp_file.name, audio, sample_rate)  # Use soundfile to save in the proper format
    return temp_file.name

def transcribe_audio(audio_path):
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.RequestError:
        st.error("API unavailable or unresponsive.")
        return ""
    except sr.UnknownValueError:
        st.error("Unable to recognize speech.")
        return ""

def extract_info(text):
    # Patterns to match name, phone number, and email
    name_pattern = r"(?i)my name is (\w+)"
    phone_pattern = r"(?i)my phone (?:number|no) is ([\d\s]+)"
    email_pattern = r"(?i)my email (?:address|id) is (.+)"  # Capture everything after 'my email is'

    # Search for name
    name = re.search(name_pattern, text)

    # Search for phone number
    phone = re.search(phone_pattern, text)
    phone_number = phone.group(1) if phone is not None else ""
    phone_number = re.sub(r"\s+", "", phone_number)  # Remove spaces from phone number

    # Ensure valid phone number (must be exactly 10 digits)
    if not re.fullmatch(r"\d{10}", phone_number):
        phone_number = ""  # Invalidate if not a valid 10-digit number

    # Search for email after phone to avoid overlap
    email = re.search(email_pattern, text)
    email_value = email.group(1).strip() if email is not None else ""  # Trim spaces

    # Return extracted information
    return {
        "name": name.group(1) if name is not None else "",
        "phone": phone_number,
        "email": email_value  # Autofill whatever is captured, valid or not
    }

st.title("Voice-based Form Submission")

if st.button("Record Audio"):
    audio = record_audio()
    if audio is not None:
        audio_path = save_audio(audio)
        
        st.audio(audio_path)  # Play the audio
        
        transcription = transcribe_audio(audio_path)
        st.write("Transcription:")
        st.write(transcription)
        
        info = extract_info(transcription)
        
        st.write("Extracted Information:")
        st.write(info)
        name = st.text_input("Name", value=info["name"])
        phone = st.text_input("Phone Number", value=info["phone"])
        email = st.text_input("Email", value=info["email"])  # Autofill incomplete email
        
        if st.button("Submit"):
            st.success("Form submitted successfully!")
        
        # Cleanup: After form submission, clean up the temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)
