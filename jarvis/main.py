import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
# from gtts import gTTS
# import pygame
# import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
recognizer.energy_threshold = 4000 
newsapi = "<YourApi>"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    

def aiProcess(command):
    client = OpenAI(api_key="<YourKey>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open github" in command.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
        
    elif "news" in command.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            
            articles = data.get('articles',[])
            
            for article in articles:
                speak(article['title'])
                
    else:
        output = aiProcess(command)
        speak(output)

    # Add your command processing logic here

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for wake word 'jarvis'
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated...")
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print("Error : {}".format(e))
