import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pywhatkit
import wikipedia
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("voice", engine.getProperty("voices")[0].id)

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

# Function to open applications
def open_application(command):
    if "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "browser" in command:
        speak("Opening Browser")
        os.system("start chrome")  # Replace 'chrome' with your preferred browser
    elif "excel" in command:
        speak("Opening Excel")
        subprocess.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"])  # Update the path if necessary
    elif "word" in command:
        speak("Opening Word")
        subprocess.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"])  # Update the path if necessary
    else:
        speak("I couldn't find the application. Please check the name.")

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
    elif "open" in command:
        open_application(command)
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
