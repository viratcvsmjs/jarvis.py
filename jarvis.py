import psutil
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import tkinter as tk
from threading import Thread
from tkinter import PhotoImage
import subprocess
import pywhatkit

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change to voices[1].id for a female voice
engine.setProperty('rate', 150)  # Speed of speech

stop_flag = False

# Phonebook
phonebook = {
    "father": "987377990, 9310313328",
    "mother": "7042480990"
}

# Close browser tabs function
def close_browser_tabs():
    """Close all browser tabs using psutil."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if 'chrome' in proc.info['name'].lower() or 'firefox' in proc.info['name'].lower():
                proc.terminate()  # Close the process (browser)
                print(f"Closed {proc.info['name']} with PID {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# GUI setup
def setup_gui():
    """Setup the graphical user interface."""
    root = tk.Tk()
    root.title("Vansh")
    root.geometry("700x500")
    root.configure(bg="#1e1e2f")

    label = tk.Label(root, text="Jarvis AI Assistant", font=("Arial", 30), fg="#00ff00", bg="#1e1e2f")
    label.pack(pady=20)

    output = tk.Text(root, height=15, width=80, wrap=tk.WORD, bg="#2e2e3f", fg="#ffffff", font=("Courier", 12))
    output.pack(pady=10)

    def log_message(message):
        output.insert(tk.END, message + "\n")
        output.see(tk.END)

    return root, log_message

root, log_message = setup_gui()

# Speak function
def speak(text):
    """Speak the given text and log to GUI."""
    log_message(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    """Listen to the user's voice and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        log_message("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            log_message("Recognizing...")
            command = recognizer.recognize_google(audio)
            log_message(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with the service.")
            return ""
        except Exception as e:
            log_message(f"Error: {e}")
            return ""

# Greet the user and ask for code
def greet():
    """Greet the user based on the time of day and ask for code."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("Please provide the code to continue.")

# Check code
def check_code(command):
    """Check if the code is correct or incorrect (single attempt)."""
    correct_code = "1479"
    if correct_code in command:
        speak("Code accepted. Access granted.")
        return True  # Code is correct
    else:
        speak("Nikal yahan se.")  # Incorrect code
        return False

# Execute command
def execute_command(command):
    """Execute commands based on user input."""
    global stop_flag

    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}.")
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open notepad" in command:
        speak("Opening Notepad.")
        subprocess.Popen("notepad.exe")  # Opens Notepad
    elif "open vs code" in command:
        speak("Opening Visual Studio Code.")
        code_path = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  # Update path if needed
        os.startfile(code_path)
    elif "close all tabs" in command:
        speak("Closing all browser tabs.")
        close_browser_tabs()  # Close all browser tabs
    elif "open whatsapp" in command:
        speak("Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com")
    elif "open facebook" in command:
        speak("Opening Facebook.")
        webbrowser.open("https://www.facebook.com")
    elif "open website" in command or "open vanshfirecontrol.com" in command:
        speak("Opening the Vansh Fire Control website.")
        webbrowser.open("https://vanshfirecontrol.com")
    elif "pc shutdown" in command:
        speak("Shutting down the PC.")
        os.system("shutdown /s /t 1")
    elif "pc restart" in command:
        speak("Restarting the PC.")
        os.system("shutdown /r /t 1")
    elif "open settings" in command:
        speak("Opening Settings.")
        subprocess.Popen("start ms-settings:", shell=True)
    elif "call father" in command:
        speak("Calling Father.")
        numbers = phonebook.get("father", "")
        for number in numbers.split(","):
            pywhatkit.sendwhatmsg_instantly(f"+91{number.strip()}", "Hello Father, this is an automated call.")
            speak(f"Calling {number.strip()}")
    elif "call mother" in command:
        speak("Calling Mother.")
        numbers = phonebook.get("mother", "")
        for number in numbers.split(","):
            pywhatkit.sendwhatmsg_instantly(f"+91{number.strip()}", "Hello Mother, this is an automated call.")
            speak(f"Calling {number.strip()}")
    elif "papa time" in command:
        speak("Sending message to Papa: When are you coming?")
        numbers = ["987377990", "9310313328"]
        for number in numbers:
            pywhatkit.sendwhatmsg_instantly(f"+91{number.strip()}", "Papa, when are you coming?")
            speak(f"Message sent to {number.strip()}.")
    elif "i am a late" in command:
        speak("Sending message to Papa, Mother, and others: I will be home by 7:40 PM from tuition.")
        numbers = ["987377990", "7042480990", "9310313328"]
        for number in numbers:
            pywhatkit.sendwhatmsg_instantly(f"+91{number.strip()}", "Main tution se let aaunga 7:40 Tak.")
            speak(f"Message sent to {number.strip()}.")
    elif "close" in command:
        speak("Stopping all operations. Have a great day!")
        stop_flag = True
    else:
        speak("Sorry, I don't understand that command yet.")

# Background thread to listen for commands
def listen_loop():
    greet()
    code_verified = False
    while not stop_flag and not code_verified:
        user_command = listen()
        if user_command:
            code_verified = check_code(user_command)  # Check if the code is correct
    if code_verified:
        while not stop_flag:
            user_command = listen()
            if user_command:
                execute_command(user_command)

# Start the application
if __name__ == "__main__":
    Thread(target=listen_loop, daemon=True).start()
    root.mainloop()
