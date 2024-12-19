import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyautogui 
import wikipedia
import cv2
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("voice", engine.getProperty("voices")[0].id)  # Select voice

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            voice = recognizer.listen(source)
            command = recognizer.recognize_google(voice).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            return ""
        except sr.RequestError:
            speak("There is an issue with the speech recognition service.")
            return ""

# Function to handle commands
def handle_command(command):
    if "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching Wikipedia for {query}")
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "open camera" in command:
        speak("Opening the camera.")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Camera", frame)
            # Exit camera when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    elif "good morning" in command:
        speak("Good morning! How can I assist you today?")
    elif "your name" in command:
        speak("I am your assistant, here to help you with tasks.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to help with that.")

# Main function
def main():
    speak("Hello! I am your assistant. How can I help you today?")
    while True:
        command = take_command()
        handle_command(command)

# Run the assistant
if __name__ == "__main__":
    main()
