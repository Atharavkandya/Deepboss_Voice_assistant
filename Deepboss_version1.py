import speech_recognition as sr
import webbrowser
import pyttsx3
import pyautogui
import time
import subprocess
import tkinter as tk
from threading import Thread

# -------------------- TTS --------------------
def init_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)
    return engine

engine = init_tts()

def speak(text):
    output_box.insert(tk.END, f"Bot: {text}\n")
    output_box.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# -------------------- SPEECH --------------------
recognizer = sr.Recognizer()

def listen_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        output_box.insert(tk.END, f"You: {command}\n")
        return command.lower()
    except:
        return ""

# -------------------- APP CONTROL --------------------
def open_app(app_name):
    speak(f"Opening {app_name}")
    try:
        if "chrome" in app_name:
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
        elif "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
        elif "vscode" in app_name:
            subprocess.Popen(["code"])
        elif "calculator" in app_name:
            subprocess.Popen(["calc.exe"])
        else:
            speak("App not configured")
    except Exception as e:
        speak("Error opening app")

# -------------------- LOGIN --------------------
def voice_login(url):
    webbrowser.open(url)
    speak("Page opened")
    time.sleep(5)

    username = listen_command()
    pyautogui.write(username)
    pyautogui.press("tab")

    password = listen_command()
    pyautogui.write(password)
    pyautogui.press("enter")

# -------------------- COMMAND PROCESSOR --------------------
def process_command(command):
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "facebook login" in command:
        voice_login("https://facebook.com/login")

    elif "instagram login" in command:
        voice_login("https://instagram.com/accounts/login/")

    elif "open" in command:
        app = command.replace("open", "").strip()
        open_app(app)

    elif "exit" in command:
        speak("Goodbye")
        root.quit()

    else:
        speak("Command not recognized")

# -------------------- MAIN LOOP --------------------
def start_listening():
    speak("Assistant started")
    while True:
        command = listen_command()
        if command:
            process_command(command)

# -------------------- GUI --------------------
root = tk.Tk()
root.title("Deepboss AI Assistant")
root.geometry("500x400")

output_box = tk.Text(root, bg="black", fg="green", font=("Courier", 10))
output_box.pack(fill=tk.BOTH, expand=True)

start_button = tk.Button(root, text="Start Assistant", command=lambda: Thread(target=start_listening).start())
start_button.pack()

root.mainloop()
