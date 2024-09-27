import streamlit as st
import speech_recognition as sr
from googletrans import Translator

# Initialize translator
translator = Translator()


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='en-IN')  # Recognize in English
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return None

# Initialize session state if it doesn't exist
if 'name' not in st.session_state:
    st.session_state['name'] = ""
if 'phone_number' not in st.session_state:
    st.session_state['phone_number'] = ""
if 'email' not in st.session_state:
    st.session_state['email'] = ""
if 'about_yourself' not in st.session_state:
    st.session_state['about_yourself'] = ""

# Streamlit UI - Form Layout
st.title("Voice-Based Form Submission")

# Name input with button outside the form
col1, col2 = st.columns([3, 1])
with col1:
    name = st.text_input("Name", value=st.session_state['name'])
with col2:
    if st.button("🎙️ Record Name"):
        recognized_name = recognize_speech()
        if recognized_name:
            st.session_state['name'] = recognized_name

# Phone Number input with button outside the form
col1, col2 = st.columns([3, 1])
with col1:
    phone_number = st.text_input("Phone Number", value=st.session_state['phone_number'])
with col2:
    if st.button("🎙️ Record Phone Number"):
        recognized_phone = recognize_speech()
        if recognized_phone:
            st.session_state['phone_number'] = recognized_phone

# Email input with button outside the form
col1, col2 = st.columns([3, 1])
with col1:
    email = st.text_input("Email", value=st.session_state['email'])
with col2:
    if st.button("🎙️ Record Email"):
        recognized_email = recognize_speech()
        if recognized_email:
            st.session_state['email'] = recognized_email

# "Tell Me About Yourself" input with button outside the form
col1, col2 = st.columns([3, 1])
with col1:
    about_yourself = st.text_area("Tell Me About Yourself", value=st.session_state['about_yourself'])
with col2:
    if st.button("🎙️ Record About Yourself"):
        recognized_about = recognize_speech()
        if recognized_about:
            st.session_state['about_yourself'] = recognized_about

# Form for submitting the user details
with st.form(key='form_submission'):
    # Display the input fields (now read-only)
    st.text_input("Name", value=st.session_state['name'], disabled=True)
    st.text_input("Phone Number", value=st.session_state['phone_number'], disabled=True)
    st.text_input("Email", value=st.session_state['email'], disabled=True)
    st.text_area("Tell Me About Yourself", value=st.session_state['about_yourself'], disabled=True)

    # Language selection for translation of "Tell Me About Yourself"
    languages = {
        "Hindi": "hi",
        "Kannada": "kn",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml",
        "Marathi": "mr",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Punjabi": "pa",
        "Odia": "or",
        "Urdu": "ur",
        "Assamese": "as",
        "Sanskrit": "sa"
    }

    selected_language = st.selectbox("Translate 'Tell Me About Yourself' to:", list(languages.keys()))

    # Submit button inside the form
    submit_button = st.form_submit_button(label="Submit")

# Handling form submission
if submit_button:
    st.success("Form submitted successfully!")
    st.write(f"Name: {st.session_state['name']}")
    st.write(f"Phone Number: {st.session_state['phone_number']}")
    st.write(f"Email: {st.session_state['email']}")
    st.write(f"Tell Me About Yourself: {st.session_state['about_yourself']}")

    # Translation after form submission
    target_language_code = languages[selected_language]
    translation = translator.translate(st.session_state['about_yourself'], dest=target_language_code)
    st.write(f"Translated Text ({selected_language}): {translation.text}")
