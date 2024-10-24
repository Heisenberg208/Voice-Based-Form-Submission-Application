import streamlit as st
import sounddevice as sd
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
st.title("🎙️ Voice-based Form Submission")
st.write("Record your voice to automatically fill in the form below. 🎤")

# Step 0: How to Use
with st.expander("ℹ️ How to Use", expanded=True):
    st.markdown("""
    ### Step-by-Step Guide:
    1. **Click** on "Start Recording" to record your voice.
    2. **Speak clearly** and mention the following details in the correct format:
       - "My name is [Your Name]."
       - "My phone number is [Your 10-digit phone number]."
       - "My email address is [Your email address]."
    3. After recording, your audio will be transcribed and the details will be filled in automatically.
    4. Review the form, edit if needed, and click on "Submit Form" to complete the submission.

    ### Important Notes:
    - Ensure you are in a **quiet environment** for better accuracy.
    - Speak **slowly and clearly**.
    - Your phone number should have **10 digits** without any special characters or spaces.
    - The email address must be in a valid format (e.g., name@example.com).
    """)

# Initialize the info variable with default empty values
info = st.session_state.get('info', {"name": "", "phone": "", "email": ""})

# Step 1: Record Audio Section
st.markdown("### Step 1: Record Your Audio")
st.write("---")
if st.button("🎧 Start Recording"):
    audio = record_audio()
    if audio is not None:
        audio_path = save_audio(audio)
        
        # Display the audio file player after recording
        st.audio(audio_path, format="audio/wav")
        
        # Transcribe the audio
        transcription = transcribe_audio(audio_path)
        st.subheader("Transcription:")
        st.write(transcription)

        # Extract name, phone, and email from the transcription
        info = extract_info(transcription)

        # Save info in session state for persistence across reruns
        st.session_state['info'] = info
        
        # Delete the audio file to save space
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Step 2: Form Submission Section
st.write("---")
st.markdown("### Step 2: Review and Submit the Form")

# Create a form with fields pre-filled from the transcribed info
with st.form(key="user_form"):
    name = st.text_input("🧑 Name", value=info.get("name", ""), placeholder="Enter your name")
    phone = st.text_input("📞 Phone Number", value=info.get("phone", ""), placeholder="Enter your phone number")
    email = st.text_input("✉️ Email", value=info.get("email", ""), placeholder="Enter your email")

    submit_button = st.form_submit_button(label="✅ Submit Form")

    if submit_button:
        if name and phone and email:
            st.success(f"Form submitted successfully!\n\n**Name**: {name}\n**Phone**: {phone}\n**Email**: {email}")
        else:
            st.error("Please fill out all fields before submitting the form.")

# Footer for help or support information
st.write("---")
st.markdown("💡 If you need help with the form submission, please contact our support team.")