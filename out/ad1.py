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

time = datetime.datetime.now().strftime("%H:%M:%S")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id) 
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
    
    query = takeCommand().lower()
    
    if any(boss in normalized_query for boss in bosses):
        speak(f"Ohh, you are my {normalized_query} boss. Unlock with your master code.")
        while True:
            query = takeCommand().lower()
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
    # Replace the word 'plus' with '+'
    phone_number = phone_number.lower().replace('plus', '+')
    # Remove all spaces and non-numeric characters except '+'
    sanitized_number = re.sub(r'[^\d+]', '', phone_number)
    return sanitized_number

def send_whatsapp_message(phone_number, message, hour, minute):
    sanitized_number = sanitize_phone_number(phone_number)
    try:
        kit.sendwhatmsg(sanitized_number, message, hour, minute)
        speak(f"Message scheduled to be sent to {sanitized_number} at {hour}:{minute}.")
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
        query = takeCommand().lower() 
        if 'open youtube' in query: 
            speak("What would you like to watch?") 
            qrry = takeCommand().lower() 
            kit.playonyt(f"{qrry}") 
        elif 'open google' in query: 
            speak("What should I search?") 
            qry = takeCommand().lower() 
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

        if 'send whatsapp message' in query:
            speak("Please provide the phone number including the country code.")
            phone_number = takeCommand().strip()  # Capture phone number
            speak("What is the message?")
            message = takeCommand().strip()  # Capture message
            speak("At what hour and minute should I send the message? Use the format hour:minute.")
            time_info = takeCommand().strip()  # Capture time in the format "hour:minute"
            
            try:
                hour, minute = map(int, time_info.split(':'))  # Split by colon and convert to integers
                send_whatsapp_message(phone_number, message, hour, minute)
            except (ValueError, IndexError):
                speak("Please provide valid time information in the format 'hour minute'.")

        
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
    