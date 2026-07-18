import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# ==========================================
# STEP 1: INITIALIZE THE TEXT-TO-SPEECH
# ==========================================
engine = pyttsx3.init()

def speak(text):
    """Helper function to make the assistant talk"""
    print(f"Assistant: {text}") 
    engine.say(text)
    engine.runAndWait()

# ==========================================
# STEP 2: CAPTURE AND LISTEN TO VOICE INPUT
# ==========================================
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # Adjusts for ambient room noise before listening
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}\n")
        return command.lower()
    except sr.UnknownValueError:
        speak("I didn't quite catch that. Could you please repeat it?")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down right now.")
        return ""

# ==========================================
# STEP 3: BUILD THE ACTION LOGIC
# ==========================================
def process_command(command):
    if not command:
        return True # Keep the loop running even if input was empty

    # Feature: Respond to "Hello"
    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
    
    # Feature: Tell current time and date
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
        
    # Feature: Perform a web search
    elif "search" in command or "google" in command:
        speak("What would you like me to search for?")
        search_query = listen_command()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
            speak(f"Here are the search results for {search_query}")

    # Feature: Stop the assistant
    elif "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye! Have a great day.")
        return False # Breaks the infinite loop
        
    return True

# ==========================================
# STEP 4: MAIN EXECUTION LOOP
# ==========================================
if __name__ == "__main__":
    speak("Voice assistant activated. How can I help?")
    is_running = True
    
    while is_running:
        user_command = listen_command()
        is_running = process_command(user_command)` `