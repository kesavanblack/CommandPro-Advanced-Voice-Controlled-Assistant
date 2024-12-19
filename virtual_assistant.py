import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import cv2
import os
from datetime import datetime
import subprocess

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

# Function to take a photo using the camera
def take_photo():
    speak("Opening the camera to take a photo.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to access the camera.")
            break
        cv2.imshow("Press 's' to save the photo or 'q' to quit", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            speak(f"Photo saved as {filename}.")
            break
        elif key == ord('q'):
            speak("Exiting the camera without saving.")
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to open Notepad and type dictated text
# def open_notepad():
    speak("Opening Notepad. Please dictate your text.")
    subprocess.Popen(["notepad.exe"])
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            while True:
                speak("Listening for your text.")
                voice = recognizer.listen(source)
                text = recognizer.recognize_google(voice)
                print(f"You said: {text}")
                with open("temp_notepad.txt", "a") as file:
                    file.write(text + "\n")
                os.system(f"type temp_notepad.txt > Notepad")
                speak("Text written to Notepad. Continue dictating or say 'stop' to exit.")
                if "stop" in text.lower():
                    speak("Closing Notepad.")
                    break
        except Exception:
            speak("An error occurred while typing in Notepad.")
        finally:
            if os.path.exists("temp_notepad.txt"):
                os.remove("temp_notepad.txt")
import pyautogui
import subprocess
import time
import win32gui
import win32con
import win32api


def focus_notepad():
    """
    Brings Notepad to the foreground by finding its window handle.
    """
    try:
        hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error focusing Notepad: {e}")
        return False


def open_notepad():
    """
    Opens Notepad and enables real-time dictation of text.
    """
    speak("Opening Notepad. Please dictate your text.")
    
    # Open Notepad
    subprocess.Popen(["notepad.exe"])
    time.sleep(2)  # Wait for Notepad to fully load
    
    if not focus_notepad():
        speak("Could not focus on Notepad. Please make sure it is open.")
        return

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            speak("Listening for your text. Say 'stop' to exit.")
            try:
                voice = recognizer.listen(source)
                text = recognizer.recognize_google(voice)
                print(f"You said: {text}")
                
                if "stop" in text.lower():
                    speak("Exiting Notepad dictation.")
                    break
                
                # Send text to Notepad
                pyautogui.typewrite(text + "\n")
            except sr.UnknownValueError:
                speak("Sorry, I didn't understand that. Please try again.")
            except sr.RequestError:
                speak("There was a problem with the speech recognition service.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                speak("An error occurred while typing in Notepad.")


# Function to open any application
def open_application(app_name):
    app_paths = {
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
    }
    app_path = app_paths.get(app_name.lower())
    if app_path:
        speak(f"Opening {app_name}.")
        subprocess.Popen(app_path)
    else:
        speak(f"Application {app_name} is not configured. Please add it to the list.")

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
        take_photo()
    elif "open notepad" in command:
        open_notepad()
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
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
