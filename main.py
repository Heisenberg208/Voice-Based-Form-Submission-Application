import streamlit as st
import speech_recognition as sr
from googletrans import Translator

translator = Translator()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown('<div class="info-text">Listening...</div>', unsafe_allow_html=True)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
        try:
            text = recognizer.recognize_google(audio, language='en-IN')
            return text
        except sr.UnknownValueError:
            st.markdown('<div class="error-message">Sorry, I could not understand the audio.</div>', unsafe_allow_html=True)
            return None
        except sr.RequestError:
            st.markdown('<div class="error-message">Could not request results from Google Speech Recognition service.</div>', unsafe_allow_html=True)
            return None

st.set_page_config(page_title="Voice-Based Form Submission", page_icon="🎤", layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add CSS to change info text color


load_css('style.css')

st.markdown('<h1 class="header">🎙️ Voice-Based Form Submission</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Speak your responses and watch them appear like magic!</p>', unsafe_allow_html=True)

st.markdown("""
<div style="display: flex; justify-content: center;">
    <div style="background-color: #E3F2FD; padding: 20px; border-radius: 10px; margin-top: 20px; max-width: 600px;">
        <h3 style="color: #1565C0; text-align: center;">📌 How to use:</h3>
        <ol style="color: #424242;">
            <li>Click on the 'Record' button for each field.</li>
            <li>Speak clearly into your microphone.</li>
            <li>The recognized text will automatically appear in the field.</li>
            <li>Edit the text if needed.</li>
            <li>Submit the form when you're ready!</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<label class="black-label">Name</label>', unsafe_allow_html=True)
    name = st.text_input("Name", value=st.session_state.get('name', ""), placeholder="Enter your name", key="name_input", label_visibility="collapsed")
    if st.button("🎤 Record Name", key="record_name"):
        recognized_text = recognize_speech()
        if recognized_text:
            st.session_state['name'] = recognized_text
            st.experimental_rerun()

    st.markdown('<label class="black-label">Phone Number</label>', unsafe_allow_html=True)
    phone_number = st.text_input("Phone Number", value=st.session_state.get('phone_number', ""), placeholder="Enter your phone number", key="phone_input", label_visibility="collapsed")
    if st.button("🎤 Record Phone", key="record_phone"):
        recognized_text = recognize_speech()
        if recognized_text:
            st.session_state['phone_number'] = recognized_text
            st.experimental_rerun()

    st.markdown('<label class="black-label">Email</label>', unsafe_allow_html=True)
    email = st.text_input("Email", value=st.session_state.get('email', ""), placeholder="Enter your email", key="email_input", label_visibility="collapsed")
    if st.button("🎤 Record Email", key="record_email"):
        recognized_text = recognize_speech()
        if recognized_text:
            st.session_state['email'] = recognized_text
            st.experimental_rerun()

    st.markdown('<label class="black-label">Tell Me About Yourself</label>', unsafe_allow_html=True)
    about_yourself = st.text_area("Tell Me About Yourself", value=st.session_state.get('tell_me_about_yourself', ""), height=100, placeholder="Share something about yourself", key="about_input", label_visibility="collapsed")
    if st.button("🎤 Record About", key="record_about"):
        recognized_text = recognize_speech()
        if recognized_text:
            st.session_state['tell_me_about_yourself'] = recognized_text
            st.experimental_rerun()

    languages = {
        "Hindi": "hi",
        "Kannada": "kn",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml"
    }

    st.markdown('<label class="black-label">Translate Tell Me About Yourself:</label>', unsafe_allow_html=True)
    selected_language = st.selectbox("", list(languages.keys()), key="language_select")
    
    if st.button("Submit"):
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

        if about_yourself.strip():  
            target_language_code = languages[selected_language]
            translation = translator.translate(about_yourself, dest=target_language_code)
            st.markdown(f"""
    <div style="color: black; background-color: #e6f3ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
        <h3 style="color: #1565C0;">Translated Text ({selected_language}):</h3>
        <p>{translation.text}</p>
    </div>
    """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">Please provide text for Tell Me About Yourself before translating</div>', unsafe_allow_html=True)
            

