import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import pyautogui
import requests
import time
import tempfile
import pygame
from gtts import gTTS
import os
import uuid
import pygame
from PIL import Image, ImageTk, ImageSequence


pygame.init()
pygame.mixer.init()

# Initialize pygame mixer for audio playb
def speak(text):
    print(f"🗣️ Mini Siri speaking: {text}")
    response_label.config(text=text)
    try:
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        # Wait until playback finishes
        while pygame.mixer.music.get_busy():
            window.update()  # Keep GUI responsive
            time.sleep(0.1)
        os.remove(filename)
    except Exception as e:
        print(f"Error in TTS playback: {e}")

# GUI Setup
window = tk.Tk()
window.title("Mini Siri - Student Assistant")
window.geometry("800x800")

# Load animated robot GIF
gif_path = "robot.gif"  # Name of your animated robot file
robot_gif = Image.open(gif_path)

# Create label for animation
robot_label = tk.Label(window, bg="white")
robot_label.pack()

# Store frames
frames = [ImageTk.PhotoImage(frame.copy().resize((300, 300))) for frame in ImageSequence.Iterator(robot_gif)]
frame_index = 0

# Animate robot function
def animate_robot():
    global frame_index
    robot_label.config(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    window.after(100, animate_robot)  # Change 100 to speed up/slow down

animate_robot()

import os
from PIL import Image

def find_image(filename, search_path="D:\\"):  # Start search from D: drive
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

# Try to find robot.png automatically
img_path = find_image("robot.png")

if img_path:
    img = Image.open(img_path)
    print(f"✅ Found image at: {img_path}")
else:
    print("❌ Could not find robot.png. Please place it in the script folder.")


response_label = tk.Label(window, text="I'm ready to help!", wraplength=280, font=("Arial", 10))
response_label.pack(pady=10)

heard_text = tk.Label(window, text="", fg="blue", wraplength=280, font=("Arial", 9, "italic"))
heard_text.pack()

recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
            return ""
    try:
        command = recognizer.recognize_google(audio)
        heard_text.config(text=f"You said: {command}")
        print(f"🗣️ You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Could not request results; check your internet connection.")
        return ""

notes = []
todo_list = []
flashcards = {
    "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
    "ml": "Machine Learning is a subset of AI focused on models that learn from data.",
    "robotics": "Robotics is the branch of technology dealing with robots.",
    "data": "Data is information collected for analysis or reference."
}

def tell_time():
    speak(datetime.datetime.now().strftime("The time is %I:%M %p"))

def tell_date():
    speak(datetime.datetime.now().strftime("Today is %B %d, %Y"))

def open_website(command):
    if 'youtube' in command and 'search' in command:
        speak("What do you want to search on YouTube?")
        search = listen()
        if search:
            url = f"https://www.youtube.com/results?search_query={search.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Searching YouTube for {search}")
    elif 'youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif 'google' in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif 'college' in command:
        webbrowser.open("https://patnawomenscollege.in")
        speak("Opening your college website")
    elif 'search' in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")
    else:
        webbrowser.open(f"https://www.google.com/search?q={command}")
        speak("Searching online")

def wiki_search(command):
    topic = command.replace("wikipedia", "").strip()
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(result)
    except:
        speak("Sorry, I couldn't find that on Wikipedia.")

def add_note():
    speak("What should I note down?")
    note = listen()
    if note:
        notes.append(note)
        speak("Note added.")

def show_notes():
    if notes:
        for n in notes:
            speak(n)
    else:
        speak("No notes found.")

def add_todo():
    speak("What task do you want to add?")
    task = listen()
    if task:
        todo_list.append(task)
        speak("Task added to to-do list.")

def show_todos():
    if todo_list:
        for t in todo_list:
            speak(t)
    else:
        speak("To-do list is empty.")

def flashcard_quiz():
    for q in flashcards:
        speak(f"What is {q}?")
        _ = listen()
        speak(f"The correct answer is: {flashcards[q]}")

def define_word():
    speak("Which word?")
    word = listen()
    try:
        summary = wikipedia.summary(word, sentences=1)
        speak(summary)
    except:
        speak("Word not found.")

def screenshot():
    file = "screenshot.png"
    pyautogui.screenshot(file)
    speak("Screenshot taken.")

def show_help():
    speak("I can tell time, date, take notes, to-dos, flashcards, definitions, search Wikipedia, Google, YouTube, translate words, tell weather, and do math!")

def get_weather():
    speak("Which city's weather do you want?")
    city = listen()
    if city:
        try:
            url = f"https://wttr.in/{city}?format=3"
            res = requests.get(url)
            speak(res.text)
        except:
            speak("Couldn't fetch weather.")

def set_alarm():
    speak("Set timer for how many seconds?")
    seconds = listen()
    try:
        sec = int(seconds)
        speak(f"Setting timer for {sec} seconds")
        time.sleep(sec)
        speak("Time's up!")
    except:
        speak("Sorry, couldn't set timer.")

def solve_math():
    speak("Say your math question.")
    problem = listen()
    try:
        answer = eval(problem)
        speak(f"The answer is {answer}")
    except:
        speak("Sorry, I couldn't solve that.")

def translate():
    speak("What word or phrase?")
    phrase = listen()
    if phrase:
        url = f"https://api.mymemory.translated.net/get?q={phrase}&langpair=en|hi"
        res = requests.get(url).json()
        translated = res['responseData']['translatedText']
        speak(f"The Hindi translation is: {translated}")

def fallback(command):
    speak(f"Let me try searching Google for: {command}")
    webbrowser.open(f"https://www.google.com/search?q={command}")

def process_command(command):
    command = command.lower()

    if "freedom fighter" in command:
        answer = ("Some of our great freedom fighters are Mahatma Gandhi, Bhagat Singh, "
                  "Subhas Chandra Bose, Jawaharlal Nehru, and Rani Lakshmibai.")
        speak(answer)

    elif "why do we celebrate independence day" in command:
        answer = ("We celebrate Independence Day to honor the day India gained freedom from British rule "
                  "on August 15, 1947. It marks the country's sovereignty and is a reminder of the sacrifices made by freedom fighters.")
        speak(answer)

    elif "how was our constitution formed" in command:
        answer = ("Our Constitution was formed by the Constituent Assembly which was elected in 1946. "
                  "It was drafted by a committee led by Dr. B.R. Ambedkar and came into effect on January 26, 1950, "
                  "establishing India as a sovereign democratic republic.")
        speak(answer)

    elif "time" in command:
        tell_time()
    elif "date" in command:
        tell_date()
    elif "note" in command:
        add_note()
    elif "show notes" in command:
        show_notes()
    elif "to-do" in command or "task" in command:
        add_todo()
    elif "show to-do" in command or "list" in command:
        show_todos()
    elif "flashcard" in command or "quiz" in command:
        flashcard_quiz()
    elif "define" in command:
        define_word()
    elif "screenshot" in command:
        screenshot()
    elif "wikipedia" in command:
        wiki_search(command)
    elif "weather" in command:
        get_weather()
    elif "timer" in command or "alarm" in command:
        set_alarm()
    elif "math" in command or "calculate" in command:
        solve_math()
    elif "translate" in command:
        translate()
    elif "search" in command or "open" in command:
        open_website(command)
    elif "help" in command:
        show_help()
    elif "bye" in command:
        speak("Goodbye!")
        window.quit()
    else:
        fallback(command)

def ask_mini_siri():
    command = listen()
    if command:
        process_command(command)

button = tk.Button(window, text="Ask Mini Siri", command=ask_mini_siri, font=("Arial", 12))
button.pack(pady=20)

entry = tk.Entry(window)
entry.pack(pady=5)

def manual_command():
    cmd = entry.get().lower()
    heard_text.config(text=f"You typed: {cmd}")
    process_command(cmd)

tk.Button(window, text="Submit Text Command", command=manual_command).pack(pady=10)

# Greet after GUI loads to ensure pygame audio works
def greet():
    speak("Hello! I'm your Mini Siri student assistant. How can I help you today?")

window.after(1000, greet)  # Wait 1 second, then run greet()


window.mainloop()

