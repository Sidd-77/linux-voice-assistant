import speech_recognition as sr
import sys
import logging
from dotenv import load_dotenv
import os
import pyttsx3
import google.generativeai as genai

# =========================
# Configuration
# =========================

# Load environment variables from .env file
load_dotenv()

# Gemini API Configuration
API_KEY = os.getenv("GEMINI_API_KEY")  # Your Gemini API key

# Check if API credentials are set
if not API_KEY:
    print("Error: Gemini API key not set. Please set API_KEY in the .env file.")
    sys.exit(1)

# Configure the Gemini API using the SDK
genai.configure(api_key=API_KEY)

# Logging Configuration
LOG_FILE = "gemini_voice_executor_windows.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()

def speak(text):
    """
    Converts text to speech.
    Args:
        text (str): The text to be spoken.
    """
    tts_engine.say(text)
    tts_engine.runAndWait()

# =========================
# Function Definitions
# =========================

def capture_voice_input():
    """
    Captures voice input from the microphone and converts it to text.
    Returns:
        str: Transcribed text from the voice input.
    """
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    try:
        microphone = sr.Microphone()
    except OSError:
        print("No microphone found. Please ensure a microphone is connected.")
        logging.error("Microphone not found.")
        sys.exit(1)

    print("Please say your task after the beep.")
    speak("Please say your task after the beep.")
    logging.info("Listening for voice input.")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        task_text = recognizer.recognize_google(audio)
        print(f"You said: {task_text}")
        logging.info(f"Transcribed voice input: {task_text}")
        return task_text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        logging.error("Speech Recognition could not understand audio.")
        speak("Sorry, I could not understand the audio.")
        sys.exit(1)
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")
        logging.error(f"Speech Recognition service error: {e}")
        speak("Sorry, there was an error with the speech recognition service.")
        sys.exit(1)

def send_task_to_gemini(task_description):
    """
    Sends the task description to the Gemini API using the Google Generative AI SDK and retrieves the command.
    Args:
        task_description (str): The task description provided by the user.
    Returns:
        str: The command received from Gemini.
    """
    try:
        print("Sending task to Gemini API...")
        logging.info(f"Sending task to Gemini API: {task_description}")
        speak("Sending your task to Gemini.")

        # Initialize the GenerativeModel
        model = genai.GenerativeModel("gemini-1.5-flash")  # Ensure this model exists

        # Generate content based on the task description
        # Adjust the prompt to ensure the model returns a command
        prompt = f"Provide the linux command to perform the following task:\n\n{task_description}\n\nCommand:"
        response = model.generate_content(prompt)

        command = response.text.strip()

        if not command:
            print("No command received from Gemini.")
            logging.error("No command received from Gemini API.")
            speak("No command received from Gemini.")
            sys.exit(1)

        print(f"Received command from Gemini: {command}")
        logging.info(f"Command received from Gemini: {command}")
        speak(f"Received command: {command}")
        return command

    except genai.GeminiError as ge:
        print(f"Gemini API error occurred: {ge}")
        logging.error(f"Gemini API error occurred: {ge}")
        speak("There was an error communicating with Gemini.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")
        speak("An unexpected error occurred.")
        sys.exit(1)

def main():
    """
    Main function to execute the Gemini Voice Task Executor.
    """
    print("=== Gemini Voice Task Executor (Windows) ===")
    speak("Welcome to the Gemini Voice Task Executor.")
    logging.info("Program started.")

    # Step 1: Capture Voice Input
    task_description = capture_voice_input()

    # Step 2: Send Task to Gemini API and Get Command
    command = send_task_to_gemini(task_description)

    # For this step, we'll just print and speak the command.
    # Execution of the command will be handled in subsequent steps.
    print(f"Gemini Command: {command}")
    logging.info(f"Gemini Command: {command}")
    speak(f"Gemini command: {command}")

    print("=== Task Completed ===")
    logging.info("Program finished.")
    speak("Task completed.")

if __name__ == "__main__":
    main()
