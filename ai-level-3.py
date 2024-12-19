import speech_recognition as sr
import pyttsx3
import os
import openai
from tkinter import Tk, Label
import threading
import time

# OpenAI API key (Replace with your API key)
openai.api_key = "asst_IaBVTcJv0wh6zbZ1X5G9MGUi"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("There is a problem with the speech recognition service.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# Function to process commands
def process_command(command):
    if "play music" in command:
        speak("Playing music.")
        os.system("start wmplayer")  # Opens Windows Media Player
    elif "what is" in command or "who is" in command:
        response = ask_openai(command)
        speak(response)
    elif "time" in command:
        from datetime import datetime
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        response = ask_openai(command)
        speak(response)

# Function to integrate with OpenAI
def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# GUI to mimic Alexa blinking
def create_gui():
    global root, alexa_label
    root = Tk()
    root.title("Alexa-Like Assistant")
    root.geometry("300x300")
    root.configure(bg="black")

    alexa_label = Label(root, text="Listening...", font=("Helvetica", 18), bg="black", fg="white")
    alexa_label.pack(expand=True)

    threading.Thread(target=voice_loop).start()
    root.mainloop()

# Function to animate the "blinking" effect
def blink():
    colors = ["black", "blue", "cyan"]
    while True:
        for color in colors:
            alexa_label.configure(fg=color)
            time.sleep(0.5)

# Continuous voice interaction loop
def voice_loop():
    threading.Thread(target=blink, daemon=True).start()
    while True:
        command = listen_command()
        if command:
            process_command(command)

# Run the assistant
if __name__ == "__main__":
    create_gui()
