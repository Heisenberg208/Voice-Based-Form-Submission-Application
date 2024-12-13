

# Voice-Based Form Submission 🎤

This is a voice-based form submission app built using Streamlit. Users can record their voice, which is then transcribed into text, and the extracted information is used to automatically fill in the form fields. The app allows you to record your name, phone number, and email address.

## Features
- **Record Audio**: Record audio for 10 seconds via your microphone.
- **Automatic Transcription**: Converts the recorded audio to text using Google Speech Recognition API.
- **Information Extraction**: Extracts name, phone number, and email from the transcription.
- **Form Submission**: Fills out a form based on the transcribed data.
- **Customizable Styling**: Styled using a custom `style.css` file.

## Prerequisites
- **Python 3.8+**
- **Virtual Environment** (Optional, but recommended)

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Heisenberg208/voice-based-form-submission.git
   cd voice-based-form-submission
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   #On ubuntu,use
   source venv/bin/activate   
   # On Windows, use:
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**
   ```bash
   streamlit run main.py
   ```

## Usage
1. Click **"Start Recording"** and speak your name, phone number, and email.
2. Review the transcribed information and edit if needed.
3. Click **"Submit Form"** to complete the submission.

