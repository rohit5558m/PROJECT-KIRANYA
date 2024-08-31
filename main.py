import pyttsx3
import datetime
import speech_recognition as sr

hour = (int(datetime.datetime.now().hour.numerator))
minute = (datetime.datetime.now().minute)
time = (hour, minute)
saytime = ["time, uuuh, ippo exact aah", time, "aachu sir"]

engine= pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
print("starting...")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
            print(saytime)  # Define saytime before this line
            r.pause_threshold = 1
            audio = r.listen(source)
    try:
        print("wait for a moment.. pls")
        query = r.recognize_google(audio, language='en-in')
        print("waiting")
        return query  # Return recognized text, not audio

    except Exception as e:
        print(e)
        return None  # Return None or some error indication


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)

    if hour>0 and hour<12:
        speak("Good Morning sir")
    elif hour>=12 and hour<=18:
        speak("Good afternoon sir")
    elif hour>=18 and hour>21:
        speak("Good evening sir,!!")


wish()
listen()
speak(saytime)