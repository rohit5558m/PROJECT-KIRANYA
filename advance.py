import pyttsx3  
import speech_recognition as sr  
import datetime 
import wikipedia 
import webbrowser 
import os 
import random 
import pyautogui 
import requests 
import time 
import pywhatkit as kit
import com as command

time = datetime.datetime.now().strftime("%H:%M:%S")
boss = "rohit" or "rohith"



engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id) 
engine.setProperty('rate', 150) 

def speak(audio): 
    engine.say(audio) 
    engine.runAndWait() 
speak("security check is need to complete so just plese wait...          on the way")
speak("checking database for the boss...")

def access():
        query = takeCommand().lower()
        if boss in query:
            speak("ohh you are my rohit boss unlock with your master code")
            query = takeCommand().lower()
            while True:
                if "master code 0010" or 'master code 001' or '001' or'0010' in query:
                    wishMe()
                    commands()
                else:
                    speak("access deneined. try again..")
                    break
        else:
            speak("sorry try again with your name")

def security():
    
    while True:
        access()

def wishMe(): 
    hour = int(datetime.datetime.now().hour) 
    if hour >= 0 and hour < 12: 
        speak("Good Morning!") 
    elif hour >= 12 and hour < 18: 
        speak("Good Afternoon!")    
    else: 
        speak("Good Evening!") 
    speak("Ready To Comply. What can I do for you?") 

def takeCommand(): 
    r = sr.Recognizer() 
    with sr.Microphone() as source: 
        print("Listening...") 
        r.pause_threshold = 1 
        audio = r.listen(source) 
    try: 
        print("Recognizing...")     
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n") 
    except Exception as e:     
        print("Say that again, please...")   
        return "None" 
    return query 

def search_wikipedia(query):
    speak('Searching Wikipedia...') 
    query = query.replace("wikipedia", "") 
    results = wikipedia.summary(query, sentences=2) 
    speak("According to Wikipedia") 
    print(results) 
    speak(results)

def open_browser_with_query(query):
    query = query.replace("search on youtube", "") 
    webbrowser.open(f"www.youtube.com/results?search_query={query}")

def open_google_with_query(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def perform_system_action(action):
    if action == "shut down":
        os.system("shutdown /s /t 5")
    elif action == "restart":
        os.system("shutdown /r /t 5")
    elif action == "lock":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def commands():
    while True: 
        query = takeCommand().lower() 
        if 'wikipedia' in query: 
            search_wikipedia(query)
        elif 'open youtube' in query: 
            speak("What would you like to watch?") 
            qrry = takeCommand().lower() 
            kit.playonyt(f"{qrry}") 
        elif 'open google' in query: 
            speak("What should I search?") 
            qry = takeCommand().lower() 
            open_google_with_query(qry)
        elif 'shutdown the system' in query: 
            perform_system_action("shut down")
        elif 'kiranya' in query:
            speak('yes boss, i am online')
        elif 'time' in query:
            speak(f"The time is {time}")

if __name__ == "__main__": 
    security()
    