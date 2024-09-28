import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import whisper
import numpy as np
import queue
import pydub
from io import BytesIO
from googletrans import Translator

# Load Whisper model
model = whisper.load_model("base")

# Initialize translator
translator = Translator()

# Class to capture and process audio
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_queue = queue.Queue()

    def recv(self, frame):
        audio_frame = frame.to_ndarray().flatten()
        self.audio_queue.put(audio_frame)
        return frame

# Function to convert raw audio to WAV format (Whisper-compatible)
def convert_raw_to_wav(raw_audio, sample_rate=16000):
    audio = np.array(raw_audio, dtype=np.int16)
    audio_segment = pydub.AudioSegment(
        data=audio.tobytes(),
        sample_width=2,   # 16-bit audio
        frame_rate=sample_rate,
        channels=1        # Mono channel
    )
    wav_io = BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)  # Rewind to the start of the file
    return wav_io

# Function to transcribe audio using Whisper
def transcribe_audio(wav_audio):
    transcription = model.transcribe(wav_audio)
    return transcription['text']

# Streamlit UI - Form Layout
st.title("Voice-Based Form Submission using Whisper")

# WebRTC Audio Recorder for "Name"
st.write("Record your Name:")
webrtc_ctx_name = webrtc_streamer(
    key="audio_name",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True},
)

# Transcribe Name
if webrtc_ctx_name.audio_receiver:
    audio_processor = webrtc_ctx_name.audio_processor
    if audio_processor and not audio_processor.audio_queue.empty():
        raw_audio = []
        while not audio_processor.audio_queue.empty():
            raw_audio.extend(audio_processor.audio_queue.get())

        # Convert raw audio to WAV
        wav_audio = convert_raw_to_wav(raw_audio)
        
        # Transcribe the audio using Whisper
        transcribed_text = transcribe_audio(wav_audio)
        st.session_state['name'] = transcribed_text
        st.write(f"Recognized Name: {transcribed_text}")
else:
    transcribed_text = st.session_state.get('name', "")

# WebRTC Audio Recorder for "Phone Number"
st.write("Record your Phone Number:")
webrtc_ctx_phone = webrtc_streamer(
    key="audio_phone",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True},
)

# Transcribe Phone Number
if webrtc_ctx_phone.audio_receiver:
    audio_processor_phone = webrtc_ctx_phone.audio_processor
    if audio_processor_phone and not audio_processor_phone.audio_queue.empty():
        raw_audio_phone = []
        while not audio_processor_phone.audio_queue.empty():
            raw_audio_phone.extend(audio_processor_phone.audio_queue.get())

        # Convert raw audio to WAV
        wav_audio_phone = convert_raw_to_wav(raw_audio_phone)

        # Transcribe the audio using Whisper
        transcribed_text_phone = transcribe_audio(wav_audio_phone)
        st.session_state['phone_number'] = transcribed_text_phone
        st.write(f"Recognized Phone Number: {transcribed_text_phone}")
else:
    transcribed_text_phone = st.session_state.get('phone_number', "")

# WebRTC Audio Recorder for "Email"
st.write("Record your Email:")
webrtc_ctx_email = webrtc_streamer(
    key="audio_email",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True},
)

# Transcribe Email
if webrtc_ctx_email.audio_receiver:
    audio_processor_email = webrtc_ctx_email.audio_processor
    if audio_processor_email and not audio_processor_email.audio_queue.empty():
        raw_audio_email = []
        while not audio_processor_email.audio_queue.empty():
            raw_audio_email.extend(audio_processor_email.audio_queue.get())

        # Convert raw audio to WAV
        wav_audio_email = convert_raw_to_wav(raw_audio_email)

        # Transcribe the audio using Whisper
        transcribed_text_email = transcribe_audio(wav_audio_email)
        st.session_state['email'] = transcribed_text_email
        st.write(f"Recognized Email: {transcribed_text_email}")
else:
    transcribed_text_email = st.session_state.get('email', "")

# WebRTC Audio Recorder for "Tell Me About Yourself"
st.write("Record 'Tell Me About Yourself':")
webrtc_ctx_about = webrtc_streamer(
    key="audio_about",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True},
)

# Transcribe "Tell Me About Yourself"
if webrtc_ctx_about.audio_receiver:
    audio_processor_about = webrtc_ctx_about.audio_processor
    if audio_processor_about and not audio_processor_about.audio_queue.empty():
        raw_audio_about = []
        while not audio_processor_about.audio_queue.empty():
            raw_audio_about.extend(audio_processor_about.audio_queue.get())

        # Convert raw audio to WAV
        wav_audio_about = convert_raw_to_wav(raw_audio_about)

        # Transcribe the audio using Whisper
        transcribed_text_about = transcribe_audio(wav_audio_about)
        st.session_state['about_yourself'] = transcribed_text_about
        st.write(f"Recognized Text: {transcribed_text_about}")
else:
    transcribed_text_about = st.session_state.get('about_yourself', "")

# Form for final inputs and translations
with st.form(key='form_submission'):
    # Name field
    name = st.text_input("Name", value=transcribed_text)
    
    # Phone number field
    phone_number = st.text_input("Phone Number", value=transcribed_text_phone)
    
    # Email field
    email = st.text_input("Email", value=transcribed_text_email)
    
    # "Tell Me About Yourself" field using the recognized text
    about_yourself = st.text_area("Tell Me About Yourself", value=transcribed_text_about)

    # Language selection for translation of "Tell Me About Yourself"
    languages = {
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Kannada": "kn"
    }

    selected_language = st.selectbox("Translate 'Tell Me About Yourself' to:", list(languages.keys()))
    
    # Submit button inside the form
    submit_button = st.form_submit_button(label="Submit")

# Handling form submission
if submit_button:
    st.success("Form submitted successfully!")
    st.write(f"Name: {name}")
    st.write(f"Phone Number: {phone_number}")
    st.write(f"Email: {email}")
    st.write(f"Tell Me About Yourself: {about_yourself}")

    # Translation after form submission
    target_language_code = languages[selected_language]
    translation = translator.translate(about_yourself, dest=target_language_code)
    st.write(f"Translated Text ({selected_language}): {translation.text}")
