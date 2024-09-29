import streamlit as st
import speech_recognition as sr
from googletrans import Translator
import time

translator = Translator()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='en-IN')
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")
        return None

st.set_page_config(page_title="Voice-Based Form Submission", page_icon="🎤", layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css('style.css')

st.markdown('<h1 class="header">🎙️ Voice-Based Form Submission</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Speak your responses and watch them appear like magic!</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    for field in ["Name", "Phone Number", "Email"]:
        if st.button(f"🎤 Record {field}"):
            recognized_text = recognize_speech()
            if recognized_text:
                st.session_state[field.lower().replace(" ", "_")] = recognized_text
                st.success(f"Recognized {field}: {recognized_text}")

    if 'tell_me_about_yourself_start' not in st.session_state:
        st.session_state.tell_me_about_yourself_start = 0

    if st.button("🎤 Record Tell Me About Yourself"):
        if st.session_state.tell_me_about_yourself_start == 0:
            st.session_state.tell_me_about_yourself_start = time.time()
        elif time.time() - st.session_state.tell_me_about_yourself_start < 60:
            recognized_text = recognize_speech()
            if recognized_text:
                st.session_state['tell_me_about_yourself'] = recognized_text
                st.success(f"Recognized Tell Me About Yourself: {recognized_text}")
        else:
            st.error("Time is up! You can no longer record your response for 'Tell Me About Yourself'.")

    with st.form(key='form_submission', clear_on_submit=False):
        st.markdown('<label class="black-label">Name</label>', unsafe_allow_html=True)
        name = st.text_input("Name", value=st.session_state.get('name', ""), placeholder="Enter your name", key="name_input", label_visibility="collapsed")

        st.markdown('<label class="black-label">Phone Number</label>', unsafe_allow_html=True)
        phone_number = st.text_input("Phone Number", value=st.session_state.get('phone_number', ""), placeholder="Enter your phone number", key="phone_input", label_visibility="collapsed")

        st.markdown('<label class="black-label">Email</label>', unsafe_allow_html=True)
        email = st.text_input("Email", value=st.session_state.get('email', ""), placeholder="Enter your email", key="email_input", label_visibility="collapsed")

        st.markdown('<label class="black-label">Tell Me About Yourself</label>', unsafe_allow_html=True)
        about_yourself = st.text_area("Tell Me About Yourself", value=st.session_state.get('tell_me_about_yourself', ""), height=100, placeholder="Share something about yourself", key="about_input", label_visibility="collapsed")

        languages = {
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml"
}

        selected_language = st.selectbox("Translate 'Tell Me About Yourself' to:", list(languages.keys()))

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        st.success("Form submitted successfully!")
        st.markdown(f"""
        <div style="color: black; background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h3 style="color: #1E88E5;">Submitted Information:</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Phone Number:</strong> {phone_number}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Tell Me About Yourself:</strong> {about_yourself}</p>
        </div>
        """, unsafe_allow_html=True)

        target_language_code = languages[selected_language]
        translation = translator.translate(about_yourself, dest=target_language_code)
        st.markdown(f"""
        <div style="color: black; background-color: #e6f3ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h3 style="color: #1565C0;">Translated Text ({selected_language}):</h3>
            <p>{translation.text}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-top: 20px;">
        <h3 style="color: #1565C0;">📌 How to use:</h3>
        <ol style="color: #424242;">
            <li>Click on the 'Record' button for each field.</li>
            <li>Speak clearly into your microphone.</li>
            <li>Review the recognized text and edit if needed.</li>
            <li>Submit the form when you're ready!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
