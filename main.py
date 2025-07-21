import speech_recognition as sr 
import webbrowser
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai
import pywhatkit as kit

#voice model speaks
def speak(text):
    tts=gTTS(text)
    tts.save("temp.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

#plays song using pywhatkit on YouTube 
def play_song(song):
    try:
        speak(f"Playing {song} on YouTube")
        kit.playonyt(song)
    except:
        speak("Sorry, I couldn't play the song.")

newsapi="news_api_key" #create from newsAPI

#for simple questions (used in else statement)
Google_API="YOUR_API_KEY" #created from google
genai.configure(api_key=Google_API)
def aiProcess(command):
    model=genai.GenerativeModel("gemini-2.5-flash")
    response=model.generate_content(command)
    return response.text

#for opening any application(add the applications according to your requirement)
def open_application(app_name):
    if "chrome" in app_name:
        os.system("start chrome")
    elif("notepad" in app_name):
        os.system("start notepad")
    elif("vs code" in app_name):
        os.system("start code")
    elif "calculator" in app_name:
        os.system("start calc")
    elif "camera" in app_name:
        os.system("start microsoft.windows.camera:")
    elif "this pc" or "file explorer" or "explorer" in app_name:
        os.system("start explorer shell:MyComputerFolder")
    else:
        speak("sorry, i'm unable to open it!")


#for opening websites directly on browser
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
        
    #playing yt videos by importing musicLibrary(add the music video links according to requirement
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
        
    #playing music by using pywhatkit
    elif "start music" in c.lower():
        song=c.lower().replace("start music","").strip()
        play_song(song)

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get("articles",[])
            for article in articles:
                print("Title:", article.get('title'))
                speak(article.get('title'))
    elif "open" in c.lower():
        app_name=c.lower().replace("open","").strip()
        open_application(app_name)
    else:
        output=aiProcess(c)
        speak(output)


if __name__=="__main__":
    speak("Initializing Alexa...")
    while True:
        #Listen for the wakeup word "Alexa" and listens audio from microphone
        r=sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio=r.listen(source,timeout=2,phrase_time_limit=5)
                #timeout:waits for x amount of seconds to speak 
                #phrase_time_limit: listens for x amount of seconds even we talk more than that
            word=r.recognize_google(audio)
            print(word.lower())
            if("stop" in word.lower()): #stops listening
                break
            if("alexa" in word.lower()):
                speak("yeah")
                with sr.Microphone() as source:
                    print("Alexa Activated...")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)
            
            
        except Exception as e:
            print("ERROR;{0}".format(e))
