import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# 🔊 Voice settings
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[6].id)
#engine.setProperty('rate', 120)
engine.setProperty('volume', 1.0)

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    c = c.lower()
    print("Processing:", c)

    if "google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    elif "instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")

    elif "youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "chat gpt" in c or "chatgpt" in c:
        speak("Opening ChatGPT")
        webbrowser.open("https://chatgpt.com")

    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musiclib.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")

    else:
        speak(f"You said {c}, but I don't understand yet")


if __name__ == "__main__":
    speak("Starting Deepboss...")

    while True:
        try:
            print("\nWaiting for wake word...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.8)

                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                except sr.WaitTimeoutError:
                    continue

            try:
                word = recognizer.recognize_google(audio)
                print("Heard:", word)
                speak(f"I heard {word}")
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Internet issue")
                continue

            # 🔑 Wake word
            if "hello" in word.lower():
                speak("Yes, I am listening")

                # 🔥 Continuous listening mode
                while True:
                    try:
                        print("Listening for command...")

                        with sr.Microphone() as source:
                            recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            audio = recognizer.listen(source)

                        try:
                            command = recognizer.recognize_google(audio)
                            print("Command:", command)
                            speak(f"You said {command}")
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't understand that")
                            continue
                        except sr.RequestError:
                            speak("Network error")
                            continue

                        # ❌ Exit condition
                        if "stop" in command.lower() or "exit" in command.lower():
                            speak("Going to sleep")
                            break

                        processCommand(command)

                    except Exception as e:
                        print("Inner Error:", repr(e))
                        continue

        except Exception as e:
            print("Error:", repr(e))