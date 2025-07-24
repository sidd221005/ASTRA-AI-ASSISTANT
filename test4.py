
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import google.generativeai as genai
import music_library

genai.configure(api_key="AIzaSyBvFGiJPh6IoSQT-9CSZsCwbcKBfxi_s7U")


engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 1.0)  # Max volume


def speak(text):
    print("Astra:", text)
    engine.say(text)
    engine.runAndWait()


def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='en-in')
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""


def gemini_process(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Sorry, there was a problem with the Gemini API."


def get_news():
    url = "https://newsapi.org/v2/top-headlines?country=in&category=technology&pageSize=5&apiKey=0cf4bb12f92e4e0e959c71769cf6ba5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                speak("Here are the top news headlines.")
                for i, article in enumerate(articles[:5], 1):
                    title = article.get("title", "No title")
                    speak(f"Headline {i}: {title}")
            else:
                speak("No news articles found.")
        else:
            speak("Failed to fetch news.")
    except Exception as e:
        speak("Error while fetching news.")


def process_command(command): 
    command=command.lower()
    
    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open instagram" in command:
        speak("opening instagram")
        webbrowser.open("https://www.instagram.com")
    elif"open linkedin" in command:
        speak("opening linkedin")
        webbrowser.open("https://www.linkedin.com/in/siddhesh-yadav-b4500a278")
    elif "news" in command:
        get_news()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = music_library.music[song]
        webbrowser.open(link)

    else:
        speak("Let me think...")
        answer = gemini_process(command)
        speak(answer)




if __name__ == "__main__":
    speak("Hello, I am Astra, your assistant.")
    while True:
        text = listen_command()
        if text:
            process_command(text)
