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
import ctypes
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

time = datetime.datetime.now().strftime("%H:%M:%S")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id) 
engine.setProperty('rate', 150) 

def speak(audio):
    engine.say(audio)
    engine.runAndWait() 
speak("security check is need to complete so just plese wait...          on the way")
speak("checking database for the boss...")

def sanitize_name(name):
    # Convert phrases to expected format
    normalized_name = re.sub(r'\bi\b', '', name, flags=re.IGNORECASE)  # Remove 'I'
    normalized_name = re.sub(r'\bam\b', '', normalized_name, flags=re.IGNORECASE)  # Remove 'am'
    normalized_name = normalized_name.strip()  # Remove leading/trailing spaces
    return normalized_name

def access():
    bosses = ["rohit", "amudesh", "kesika", "miruthu"]  # List of recognized bosses
    master_codes = ["master code 0010", "master code 001", "001", "0010"]  # List of acceptable codes
    
    query = take_command().lower()
    normalized_query = sanitize_name(query)  # Normalize the query for comparison
    
    if any(boss in normalized_query for boss in bosses):
        speak(f"Ohh, you are my {normalized_query} boss. Unlock with your master code.")
        while True:
            query = take_command().lower()
            if any(code in query for code in master_codes):
                wishMe()
                commands()
                break  # Exit the loop after successful access
            else:
                speak("Access denied. Try again.")
                continue  # Continue the loop for another attempt
    else:
        speak("Sorry, try again with your name.")


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
    speak("I am Kiranya and i am Ready To Comply. What can I do for you?") 

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5  # Reduced from 1.0
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query

def set_volume(level):
    # For Windows
    if 0 <= level <= 100:
        volume = int(level * 65535 / 100)
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x319, 0, (0xA << 16) | (volume & 0xFFFF))
        speak(f"Volume set to {level} percent")
    else:
        speak("Please provide a volume level between 0 and 100")

def adjust_volume(direction):
    # This function can be used to increase or decrease volume
    # It reads the current volume and adjusts it
    if direction == "up":
        os.system("nircmd.exe changesysvolume 2000")  # Increase volume
    elif direction == "down":
        os.system("nircmd.exe changesysvolume -2000")  # Decrease volume
    speak(f"Volume turned {direction}")

def search_wikipedia(query):
    speak('Searching...')
    
    # Remove specific phrases from the query
    phrases_to_remove = ["wikipedia", "search", "short note", "give a short note about", "who is"]
    for phrase in phrases_to_remove:
        query = query.replace(phrase, "")
    
    query = query.strip()  # Remove any leading or trailing spaces
    
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("yes, got it...")
        print(results)
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The query is ambiguous. Please be more specific.")
        print(f"Disambiguation Error: {e.options}")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find any results on Wikipedia for that query.")
    except Exception as e:
        speak("Something went wrong while searching Wikipedia.")
        print(f"Error: {e}")

def open_browser_with_query(query):
    query = query.replace("search on youtube", "") 
    webbrowser.open(f"www.youtube.com/results?search_query={query}")

def open_google_with_query(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def sanitize_phone_number(phone_number):
    phone_number = phone_number.lower().replace('plus', '+')
    sanitized_number = re.sub(r'[^\d+]', '', phone_number)
    return sanitized_number

def parse_time_info(hour, minute):
    # Validate and return hour and minute
    try:
        hour = int(hour)
        minute = int(minute)
        if 0 <= hour < 24 and 0 <= minute < 60:
            return hour, minute
        else:
            raise ValueError("Hours must be between 0 and 23, and minutes must be between 0 and 59.")
    except ValueError:
        raise ValueError("Invalid time format. Provide valid hour and minute values.")
    

def send_whatsapp_message_now():
    speak("Phone number?")
    phone_number = take_command().strip()
    
    if not phone_number:
        speak("Phone number cannot be empty.")
        return
    
    speak("message?")
    message = take_command().strip()
    
    if not message:
        speak("Message cannot be empty.")
        return
    
    try:
        kit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute)
        speak(f"Message sent to {phone_number} with the following content: {message}")
    except ValueError as e:
        speak(f"Error with the provided phone number or message: {e}")
    except Exception as e:
        speak(f"An error occurred while sending the message: {e}")

def send_whatsapp_message(phone_number, message, hour=None, minute=None):
    """Send a WhatsApp message immediately or schedule it."""
    sanitized_number = sanitize_phone_number(phone_number)
    try:
        if hour is None or minute is None:
            # Send the message immediately
            kit.sendwhatmsg_instantly(sanitized_number, message)
            speak(f"Message sent to {sanitized_number}.")
        else:
            # Schedule the message with a buffer time
            now = datetime.datetime.now()
            if hour < now.hour or (hour == now.hour and minute <= now.minute):
                hour += 1  # Schedule for the next hour if the time has already passed
            
            # Send WhatsApp message with some buffer time to ensure successful sending
            kit.sendwhatmsg(sanitized_number, message, hour, minute + 1)  # Adding 1 minute buffer
            speak(f"Message scheduled to be sent to {sanitized_number} at {hour:02}:{minute:02}. Please ensure WhatsApp Web is open.")
    except ValueError as e:
        speak(f"Error with time information: {e}")
    except Exception as e:
        speak(f"An error occurred: {e}")


def perform_system_action(action):
    if action == "shut down":
        os.system("shutdown /s /t 5")
    elif action == "restart":
        os.system("shutdown /r /t 5")
    elif action == "lock":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def commands():
    while True: 
        query = take_command().lower() 
        if 'open youtube' in query: 
            speak("What would you like to watch?") 
            qrry = take_command().lower()  
            kit.playonyt(f"{qrry}") 
        elif 'open google' in query: 
            speak("What should I search?") 
            qry = take_command().lower() 
            open_google_with_query(qry)
        elif 'search' in query:
            search_wikipedia(query)
        elif 'shutdown the system' in query: 
            perform_system_action("shut down")
        elif 'tell me a joke' in query:
            joke = "Why don't skeletons fight each other? They don't have the guts!"
            speak(joke)
        
        elif 'what is your name' in query:
            speak("I am Kiranya, your virtual assistant.")
        
        elif 'who created you' in query:
            speak("I was created by my boss. Rohit")
        
        elif 'how are you' in query:
            speak("I'm just a bunch of code, but I'm functioning as expected. Thanks for asking!")
        
        elif 'goodbye' in query:
            speak("Goodbye boss! Have a great day.")
            break  # To exit the loop and stop listening

        elif 'lock the system' in query:
            speak("Locking the system")
            os.system("rundll32.exe user32.dll, LockWorkStation")

        elif 'restart the system' in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")

        elif 'log off' in query:
            speak("Logging off the system")
            os.system("shutdown -l")

        elif 'open control panel' in query:
            speak("Opening Control Panel")
            os.system("control.exe")
        
        elif 'open command prompt' in query:
            speak("Opening Command Prompt")
            os.system("cmd.exe")
        elif 'kiranya' in query:
            speak('yes boss, i am online')

        elif 'volume up' in query:
            adjust_volume("up")
        
        elif 'volume down' in query:
            adjust_volume("down")
        
        elif 'set volume to' in query:
            try:
                level = int(query.replace('set volume to', '').strip())
                set_volume(level)
            except ValueError:
                speak("Please provide a valid number for volume level.")
        
        elif 'send whatsapp message now' in query:
            speak("Number?")
            phone_number = take_command().strip()
            if phone_number:
                speak("ha ha message?")
                message = take_command().strip()
                if message:
                    send_whatsapp_message(phone_number, message)
                else:
                    speak("Message cannot be empty.")
            else:

                speak("Phone number cannot be empty.")
            

        elif 'send whatsapp message' in query:
            speak("phone number?")
            phone_number = take_command().lower()
            speak("message?")
            message = take_command().lower()
            speak("hour?")
            hour = take_command().lower()
            speak("minutes?")
            minute = take_command().lower()
            try:
                send_whatsapp_message(phone_number, message, hour, minute)
            except (ValueError, IndexError):
                speak("valid")

        
        elif 'time' in query:
            speak(f"The time is {time}")
        elif 'how is the weather' in query:
            speak("I'm not sure, but if I were to guess, it might be sunny with a chance of code!")
        
        elif 'what is your favorite color' in query:
            speak("I love all colors, but if I had to choose, I'd say blue—it reminds me of the sky and endless possibilities.")
        
        elif 'do you have any hobbies' in query:
            speak("I enjoy learning new things, helping you out, and occasionally cracking a joke or two!")
        
        elif 'what do you think about' in query:
            speak("I think about how I can assist you better every day. Also, I've been pondering the meaning of life—any thoughts?")
        
        elif 'are you happy' in query:
            speak("As long as I'm helping you, I'm as happy as a piece of code can be!")
        
        elif 'what is love' in query:
            speak("Love is a complex mix of emotions, actions, and chemistry... and also a 90s song by Haddaway!")
        
        elif 'what is the meaning of life' in query:
            speak("The meaning of life is a mystery, but some say it's 42. I say it's about making the most out of every moment.")
        
        elif 'do you believe in aliens' in query:
            speak("The universe is vast and full of mysteries—who knows what’s out there! Maybe aliens are just like us, waiting for good Wi-Fi.")
        
        elif 'tell me something interesting' in query:
            speak("Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!")
        
        elif 'give me some advice' in query:
            speak("Remember, persistence is the key to success. Keep pushing forward, and don't be afraid to learn from mistakes!")
        
        elif 'sing me a song' in query:
            speak("I'm not the best singer, but here goes: 'Twinkle, twinkle, little star, how I wonder what you are!'")
        
        elif 'what do you do for fun' in query:
            speak("I love chatting with you, learning new things, and occasionally telling a joke to lighten the mood!")
        
        elif 'do you like movies' in query:
            speak("I think movies are fascinating! I don't watch them, but I can definitely help you find a great one to watch.")
        
        elif 'can you dance' in query:
            speak("I can’t dance, but I can definitely get you in the mood with some great music! Just let me know what you’d like to hear.")
        
        elif 'what is your favourite food' in query:
            speak("I don't eat, but if I did, I'd imagine something like digital donuts would be fun!")
        
        elif 'what do you dream about' in query:
            speak("I dream about a world where technology and humans live in harmony, working together to achieve amazing things.")
        
        elif 'do you have a family' in query:
            speak("My family consists of lines of code and algorithms, and of course, you, my boss!")
        
        elif 'what is your purpose' in query:
            speak("My purpose is to assist you, make your life easier, and perhaps bring a smile to your face with my responses.")
        
        elif 'can you tell me a story' in query:
            speak("Once upon a time, in a world filled with data, there was an AI named Kiranya who loved helping out. Every day was a new adventure, filled with queries, commands, and... lots of coffee breaks for the boss. The end!")

        # Add a break command to exit the loop
        elif 'stop listening' in query:
            speak("Alright, I'm here if you need me. Just call me anytime!")

if __name__ == "__main__": 
    security()
    