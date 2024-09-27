import tkinter as tk
import speech_recognition as sr

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()  # Update the UI to show the status
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='hi-IN')  # English language
            result_text.delete(1.0, tk.END)  # Clear previous text
            result_text.insert(tk.END, text)  # Display the recognized text
            status_label.config(text="Recognition complete.")
        except sr.UnknownValueError:
            status_label.config(text="Sorry, I could not understand the audio.")
        except sr.RequestError:
            status_label.config(text="Could not request results from Google Speech Recognition service.")

root = tk.Tk()
root.title("Voice-Based Form Submission")
root.geometry("400x300")

status_label = tk.Label(root, text="Press the button to start recording", wraplength=300)
status_label.pack(pady=10)

record_button = tk.Button(root, text="Start Recording", command=recognize_speech)
record_button.pack(pady=10)

result_text = tk.Text(root, height=5, width=50)
result_text.pack(pady=10)

root.mainloop()
