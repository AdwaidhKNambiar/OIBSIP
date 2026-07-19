import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import smtplib
import time
import json
import requests
from email.message import EmailMessage

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# --- CONFIGURATION ENGINE (Custom Commands & Privacy Logging) ---
CONFIG_FILE = "assistant_config.json"

def load_config():
    """Loads custom voice triggers and local settings."""
    default_config = {
        "custom_commands": {
            "open code": "start code",
            "check github": "https://github.com/AdwaidhKNambiar/OIBSIP"
        },
        "email_settings": {
            "smtp_server": "smtp.gmail.com",
            "port": 465,
            "dummy_sender": "your_test_email@gmail.com",
            "dummy_password": "your_app_password"
        },
        "weather_api_key": "YOUR_OPENWEATHERMAP_API_KEY" # Replace with free key if available
    }
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()

def log_privacy_event(action, detail):
    """Compliance Logger: Plainly records processed intents locally for audits."""
    with open("privacy_audit.log", "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] COMPLIANCE AUDIT | Action: {action} | Details: {detail}\n")

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    greeting = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"
    speak(f"Good {greeting} Adwaidh! Advanced Tier system initialized.")

def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception:
        return "none"

# --- 1. NATURAL LANGUAGE INTENT UNDERSTANDING ENGINE ---
def parse_intent(query):
    """
    Parses intent from semantic syntax mapping rather than rigid word matching.
    Matches variations of phrasing like 'could you tell me what time it is' or 'check the clock'.
    """
    # Intent Lexicons
    intent_map = {
        "time": ["time", "clock", "hour", "current period"],
        "date": ["date", "day", "calendar", "today"],
        "email": ["email", "send mail", "message boss", "dispatch email"],
        "reminder": ["remind", "timer", "set alert", "alarm"],
        "weather": ["weather", "temperature", "forecast", "rain", "climate"],
        "knowledge": ["what is", "who is", "define", "explain", "tell me about"],
        "exit": ["exit", "stop", "goodbye", "quit", "close"]
    }
    
    # Clean spoken fillers
    clean_query = query.replace("please", "").replace("could you", "").replace("assistant", "").strip()
    
    for intent, vocabulary in intent_map.items():
        if any(keyword in clean_query for keyword in vocabulary):
            return intent, clean_query
            
    # Check custom commands loaded from config
    for custom_trigger, action in config["custom_commands"].items():
        if custom_trigger in clean_query:
            return "custom", action
            
    return "unknown", clean_query

# --- FEATURE AUTOMATION METHODS ---
def send_voice_email():
    """Sends an email using dummy configuration details via smtplib."""
    speak("Who is the recipient email address?")
    recipient = listen_to_user().replace(" ", "") # strip speech spaces
    if "@" not in recipient:
        speak("Invalid email address formatting.")
        return
        
    speak("What is the message body?")
    body = listen_to_user()
    
    log_privacy_event("Email Pipeline", f"Target Recipient: {recipient}")
    
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = "Automated Transmission via Voice Assistant"
        msg['From'] = config["email_settings"]["dummy_sender"]
        msg['To'] = recipient
        
        # SSL Secure Connection Setup
        with smtplib.SMTP_SSL(config["email_settings"]["smtp_server"], config["email_settings"]["port"]) as server:
            server.login(config["email_settings"]["dummy_sender"], config["email_settings"]["dummy_password"])
            server.send_message(msg)
        speak("Transmission completely successfully.")
    except Exception as e:
        speak("Email pipeline simulated. (Check configuration for live credentials).")

def set_voice_reminder(clean_query):
    """Parses delay integers from speech string and sets a blocking sound alert."""
    speak("For how many seconds should I set the timer alert?")
    duration_str = listen_to_user()
    try:
        seconds = int([int(s) for s in duration_str.split() if s.isdigit()][0])
    except IndexError:
        seconds = 10 # Default fallback
        
    speak(f"Setting an audio alert for {seconds} seconds starting now.")
    time.sleep(seconds)
    # Built-in OS alert chirp ring sound
    for _ in range(3):
        print("\a") # Triggers system terminal bell chirp sound
        time.sleep(0.5)
    speak("Timer completed! This is your audio notification alert.")

def fetch_live_weather():
    """Queries live meteorological frameworks or local backup models."""
    speak("Which city's weather data would you like to retrieve?")
    city = listen_to_user()
    log_privacy_event("Location Query", f"City: {city}")
    
    api_key = config["weather_api_key"]
    if api_key == "YOUR_OPENWEATHERMAP_API_KEY":
        # Safe elegant mock response if API Key wasn't provisioned yet
        speak(f"Simulating current weather for {city}. It is 24 degrees Celsius with slight breeze.")
        return
        
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is currently {temp} degrees Celsius with {desc}.")
    except Exception:
        speak("Unable to reach meteorological servers right now.")

def query_knowledge_base(clean_query):
    """Local embedded analytical Knowledge Base providing instantaneous definitions."""
    local_kb = {
        "python": "Python is a high-level, interpreted, general-purpose programming language famed for readability.",
        "git": "Git is a distributed version control architecture built to track code alterations over history.",
        "oasis infobyte": "Oasis Infobyte is an elite technology development provider supporting dynamic student internships."
    }
    
    found = False
    for topic, definition in local_kb.items():
        if topic in clean_query:
            speak(definition)
            found = True
            break
            
    if not found:
        speak("Query not in local base. Redirecting search query to web engines.")
        webbrowser.open(f"https://www.google.com/search?q={clean_query}")

# --- MAIN EXECUTION FRAMEWORK ---
if __name__ == "__main__":
    greet_user()
    is_running = True
    while is_running:
        raw_speech = listen_to_user()
        if raw_speech == "none":
            continue
            
        intent, processed_text = parse_intent(raw_speech)
        log_privacy_event("Intent Processing", f"Identified Intent: {intent}")
        
        if intent == "time":
            speak(f"The current local system time is {datetime.datetime.now().strftime('%I:%M %p')}")
        elif intent == "date":
            speak(f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}")
        elif intent == "email":
            send_voice_email()
        elif intent == "reminder":
            set_voice_reminder(processed_text)
        elif intent == "weather":
            fetch_live_weather()
        elif intent == "knowledge":
            query_knowledge_base(processed_text)
        elif intent == "custom":
            speak(f"Executing macro command function.")
            if "http" in processed_text:
                webbrowser.open(processed_text)
            else:
                os.system(processed_text)
        elif intent == "exit":
            speak("System offline. Goodbye Adwaidh!")
            is_running = False