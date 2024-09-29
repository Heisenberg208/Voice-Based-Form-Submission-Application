import streamlit as st
import speech_recognition as sr
from googletrans import Translator

# Initialize translator
translator = Translator()

# Function to recognize speech in English
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

# Set page config
st.set_page_config(page_title="Voice-Based Form Submission",  page_icon="🎤",layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #acaeb0;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .st-emotion-cache-1wivap2 {
        padding-top: 3rem;
    }
    .header {
        color: #1E88E5;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 30px;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subheader {
        color: #424242;
        font-size: 24px;
        margin-bottom: 20px;
        text-align: center;
    }
    .form-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 5px solid #1E88E5;  /* Highlighted border with increased thickness */
    }
    .black-label {
        color: black !important;
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
    }
</style>
""", unsafe_allow_html=True)


# Streamlit UI
st.markdown('<h1 class="header">🎙️ Voice-Based Form Submission</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Speak your responses and watch them appear like magic!</p>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([2, 1])

with col1:
    # Voice input fields
    for field in ["Name", "Phone Number", "Email", "Tell Me About Yourself"]:
        if st.button(f"🎤 Record {field}"):
            recognized_text = recognize_speech()
            if recognized_text:
                st.session_state[field.lower().replace(" ", "_")] = recognized_text
                st.success(f"Recognized {field}: {recognized_text}")

    # Creating the form with fields, wrapped in .form-container div
    # Opening div for form-container
    with st.form(key='form_submission', clear_on_submit=False) :
        # Name field with black label
        st.markdown('<label class="black-label">Name</label>', unsafe_allow_html=True)
        name = st.text_input("Name", value=st.session_state.get('name', ""), placeholder="Enter your name", key="name_input", label_visibility="collapsed")

        # Phone Number field with black label
        st.markdown('<label class="black-label">Phone Number</label>', unsafe_allow_html=True)
        phone_number = st.text_input("Phone Number", value=st.session_state.get('phone_number', ""), placeholder="Enter your phone number", key="phone_input", label_visibility="collapsed")

        # Email field with black label
        st.markdown('<label class="black-label">Email</label>', unsafe_allow_html=True)
        email = st.text_input("Email", value=st.session_state.get('email', ""), placeholder="Enter your email", key="email_input", label_visibility="collapsed")

        # Tell Me About Yourself field with black label
        st.markdown('<label class="black-label">Tell Me About Yourself</label>', unsafe_allow_html=True)
        about_yourself = st.text_area("Tell Me About Yourself", value=st.session_state.get('tell_me_about_yourself', ""), height=100, placeholder="Share something about yourself", key="about_input", label_visibility="collapsed")

        # Language selection for translation
        languages = {"Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de", "Kannada": "kn"}
        selected_language = st.selectbox("Translate 'Tell Me About Yourself' to:", list(languages.keys()))

        # Submit button
        submit_button = st.form_submit_button(label="Submit")

    # Closing div for form-container
    st.markdown('</div>', unsafe_allow_html=True)

    # Handling form submission
    if submit_button:
        st.success("Form submitted successfully!")
        # Display submitted information
        st.markdown(f"""
        <div style="color: black; background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h3 style="color: #1E88E5;">Submitted Information:</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Phone Number:</strong> {phone_number}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Tell Me About Yourself:</strong> {about_yourself}</p>
        </div>
        """, unsafe_allow_html=True)

        # Translation
        target_language_code = languages[selected_language]
        translation = translator.translate(about_yourself, dest=target_language_code)
        st.markdown(f"""
        <div style="color: black; background-color: #e6f3ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
            <h3 style="color: #1565C0;">Translated Text ({selected_language}):</h3>
            <p>{translation.text}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Add some information or instructions
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
