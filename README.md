# Voice-Based Form Submission Application

## Overview

This project implements a voice-based form submission application using Python and Streamlit. Users can provide their information by speaking, and the app recognizes the speech and displays the input in real-time. The application also supports translation of the "Tell Me About Yourself" field into several Indian languages.

## Features

- **Voice Recognition:** Users can record their responses using a microphone.
- **Real-time Display:** Recognized text is displayed immediately in the respective fields.
- **Translation:** Users can translate their response to the "Tell Me About Yourself" field into five main Indian languages: Kannada, Hindi, Tamil, Telugu, and Malayalam.
- **Responsive Design:** The application is designed to be user-friendly and responsive.

## Technologies Used

- **Python 3.x**
- **Streamlit:** A library to create interactive web applications.
- **SpeechRecognition:** A library for recognizing speech.
- **Googletrans:** A library for translating text.
  
## Requirements

- Python 3.x
- Required packages can be installed using `pip`.

## Installation

1. **Clone this repository to your local machine:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory:**
   ```bash
   cd <project-directory>
   ```

3. **Install the required packages:**
   ```bash
   pip install streamlit SpeechRecognition googletrans==4.0.0-rc1
   ```

## Usage

1. **Run the application:**
   ```bash
   streamlit run main.py
   ```

2. **Open the provided local URL in your web browser.**

3. **Use the buttons to record your responses for each field, and submit the form once you're ready.**

## CSS Styling

The application uses a custom CSS file named `style.css` for styling. This file controls the appearance of various components, including the form layout and buttons.

### Custom CSS Highlights

- **Header Styles:** Custom styles for headers and subheaders to enhance visual appeal.
- **Form Container:** Styles for the form container, including padding, border-radius, and background color.
- **Button Styles:** Custom styles for buttons, including hover effects and background color changes.

## Code Structure

- **`main.py:`** Contains the main logic for the application, including voice recognition, form submission, and translation features.
- **`style.css`:** Contains custom styles for the application, improving user experience.

## Limitations

- The application currently only supports the five specified Indian languages for translation.
- The speech recognition feature may vary in accuracy based on the quality of the microphone and background noise.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Streamlit Documentation](https://docs.streamlit.io/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [Googletrans Documentation](https://pypi.org/project/googletrans/)

## Contact

For any questions or feedback, feel free to reach out via:

- Email: [poornachandra308@gmail.com](mailto:poornachandra308@gmail.com)
- LinkedIn: [Poornachandra A N](https://www.linkedin.com/in/poornachandra-a-n-602aa1233/)

```

