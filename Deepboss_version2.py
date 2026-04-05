import speech_recognition as sr
import webbrowser
import pyttsx3
import pyautogui
import time
import subprocess
import tkinter as tk
from threading import Thread
import urllib.parse

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
            subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"])
        elif "notepad" in app_name:
            subprocess.Popen(["open", "-a", "TextEdit"])
        elif "vscode" in app_name or "code" in app_name:
            subprocess.Popen(["code"])
        elif "calculator" in app_name:
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            speak("App not configured")
    except:
        speak("Error opening app")


# -------------------- LOGIN --------------------
def voice_login(url):
    webbrowser.open(url)
    speak("Page opened")
    time.sleep(5)

    speak("Speak your username")
    username = listen_command()
    pyautogui.write(username)
    pyautogui.press("tab")

    speak("Speak your password")
    password = listen_command()
    pyautogui.write(password)
    pyautogui.press("enter")


# -------------------- SEARCH --------------------
def search_google(query):
    speak(f"Searching Google for {query}")
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)

def search_chatgpt(query):
    speak(f"Searching ChatGPT for {query}")
    url = "https://chatgpt.com/?q=" + urllib.parse.quote(query)
    webbrowser.open(url)


# -------------------- COMMAND PROCESSOR --------------------
def process_command(command):
    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")

    elif "facebook login" in command:
        voice_login("https://facebook.com/login")

    elif "instagram login" in command:
        voice_login("https://instagram.com/accounts/login/")

    elif command.startswith("search google"):
        query = command.replace("search google", "").strip()
        search_google(query)

    elif command.startswith("search chatgpt"):
        query = command.replace("search chatgpt", "").strip()
        search_chatgpt(query)

    elif "open" in command:
        app = command.replace("open", "").strip()
        open_app(app)

    else:
        speak("Command not recognized")


# -------------------- MAIN LOOP WITH WAKE WORD --------------------
def start_listening():
    speak("Assistant is sleeping. Say hello to wake me up.")

    while True:
        command = listen_command()

        if not command:
            continue

        # 🔑 Wake word
        if any(word in command for word in ["hello", "hey", "hi"]):
            speak("Yes, I am listening")

            while True:
                command = listen_command()

                if not command:
                    continue

                # ❌ Exit listening mode
                if any(word in command for word in ["stop", "sleep", "exit"]):
                    speak("Going to sleep")
                    break

                process_command(command)


# -------------------- GUI --------------------
root = tk.Tk()
root.title("Deepboss AI Assistant")
root.geometry("500x400")

output_box = tk.Text(root, bg="black", fg="green", font=("Courier", 10))
output_box.pack(fill=tk.BOTH, expand=True)

start_button = tk.Button(root, text="Start Assistant",
                         command=lambda: Thread(target=start_listening).start())
start_button.pack()

root.mainloop()
