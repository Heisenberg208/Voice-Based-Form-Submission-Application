import streamlit as st
import sounddevice as sd
import numpy as np
import re
import tempfile
import os
import speech_recognition as sr
import soundfile as sf

recognizer = sr.Recognizer()

def record_audio(duration=10, sample_rate=16000):
    st.info("Recording audio for 10 seconds...")
    try:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        st.success("Recording complete!")
        return audio
    except sd.PortAudioError:
        st.error("Error accessing the microphone. Please check your audio settings.")
        return None

def save_audio(audio, sample_rate=16000):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, audio, sample_rate)
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
    name_pattern = r"(?i)my name is (\w+)"
    phone_pattern = r"(?i)my phone (?:number|no) is ([\d\s]+)"
    email_pattern = r"(?i)my email (?:address|id) is (.+)"

    name = re.search(name_pattern, text)
    phone = re.search(phone_pattern, text)
    phone_number = phone.group(1) if phone is not None else ""
    phone_number = re.sub(r"\s+", "", phone_number)

    if not re.fullmatch(r"\d{10}", phone_number):
        phone_number = ""

    email = re.search(email_pattern, text)
    email_value = email.group(1).strip() if email is not None else ""

    return {
        "name": name.group(1) if name is not None else "",
        "phone": phone_number,
        "email": email_value
    }

# Set the title and intro
st.title("Voice-based Form Submission")
st.write("Record your voice to automatically fill in the form below.")

# Initialize the info variable with default empty values
info = {"name": "", "phone": "", "email": ""}

# Organize layout using columns for recording and displaying the result
col1, col2 = st.columns(2)

# Column 1: Audio recording and transcription
with col1:
    st.subheader("Record Your Audio")
    if st.button("Start Recording"):
        audio = record_audio()
        if audio is not None:
            audio_path = save_audio(audio)
            
            st.audio(audio_path)
            
            transcription = transcribe_audio(audio_path)
            st.subheader("Transcription:")
            st.write(transcription)

            info = extract_info(transcription)

            # Delete temporary audio file after use
            if os.path.exists(audio_path):
                os.remove(audio_path)

# Column 2: Form for user input
with col2:
    st.subheader("Fill the Form")
    with st.form(key="user_form"):
        name = st.text_input("Name", value=info.get("name", ""))
        phone = st.text_input("Phone Number", value=info.get("phone", ""))
        email = st.text_input("Email", value=info.get("email", ""))
        
        submit_button = st.form_submit_button(label="Submit")
        
        if submit_button:
            if name and phone and email:
                st.success(f"Form submitted successfully!\n\nName: {name}\nPhone: {phone}\nEmail: {email}")
            else:
                st.error("Please fill out all the fields before submitting.")

# Footer for help or support information
st.write("---")
st.write("If you need help with the form submission, please contact support.")
