import speech_recognition as sr
import pyttsx3
import os
import subprocess
import pywhatkit
import wikipedia
from datetime import datetime
import openai  # Install using: pip install openai
import psutil  # For system monitoring
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

# Initialize OpenAI API
openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        output_text.insert(tk.END, "Listening...\n")
        try:
            voice = recognizer.listen(source)
            command = recognizer.recognize_google(voice).lower()
            output_text.insert(tk.END, f"You said: {command}\n")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            output_text.insert(tk.END, "Sorry, I didn't understand. Please try again.\n")
            return ""
        except sr.RequestError:
            speak("There is an issue with the speech recognition service.")
            output_text.insert(tk.END, "There is an issue with the speech recognition service.\n")
            return ""

# Function to handle GPT-based responses
def advanced_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

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
        output_text.insert(tk.END, f"Wikipedia summary: {summary}\n")
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
        output_text.insert(tk.END, f"The time is {current_time}\n")
    elif "open" in command:
        if "notepad" in command:
            speak("Opening Notepad")
            os.system("notepad")
        elif "calculator" in command:
            speak("Opening Calculator")
            os.system("calc")
        elif "browser" in command:
            speak("Opening Browser")
            os.system("start chrome")
        else:
            speak("Application not found.")
    elif "schedule" in command:
        event = command.replace("schedule", "").strip()
        scheduled_tasks.append(event)
        output_text.insert(tk.END, f"Task scheduled: {event}\n")
        speak(f"Task '{event}' has been scheduled.")
    elif "monitor" in command:
        monitor_system()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        response = advanced_response(command)
        speak(response)
        output_text.insert(tk.END, f"AI: {response}\n")

# Function for system monitoring
def monitor_system():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    system_info = (
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory.percent}%\n"
        f"Disk Usage: {disk.percent}%\n"
    )
    speak("Here is your system information.")
    output_text.insert(tk.END, system_info + "\n")

# GUI functions
def process_command():
    command = command_entry.get()
    output_text.insert(tk.END, f"You said: {command}\n")
    handle_command(command)
    command_entry.delete(0, tk.END)

def voice_command():
    command = take_command()
    if command:
        handle_command(command)

# Initialize GUI
root = tk.Tk()
root.title("Advanced AI Assistant")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

command_entry = tk.Entry(frame, width=50)
command_entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(frame, text="Send", command=process_command)
send_button.grid(row=0, column=1, padx=5)

voice_button = tk.Button(frame, text="Voice Command", command=voice_command)
voice_button.grid(row=0, column=2, padx=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state='normal')
output_text.pack(pady=10)

scheduled_tasks = []

root.mainloop()
