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

class comm:
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
                open_browser_with_query(qry)
            elif 'shutdown the system' in query: 
                perform_system_action("shut down")
            elif 'kiranya' in query:
                speak('yes boss, i am online')
            elif 'time' in query:
                speak(f"The time is {time}")