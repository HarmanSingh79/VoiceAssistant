import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai
import pywhatkit as kit


recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="75c0f0543973487d93aef07ce3896fd9"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

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

def play_song(song):
    try:
        speak(f"Playing {song} on YouTube")
        kit.playonyt(song)
    except:
        speak("Sorry, I couldn't play the song.")

#it's for chatgpt api
# def aiProcess(command):
#     client=OpenAI(api_key="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")

# completion=client.chat.completions.create(
#     model="gpt-4.1",
#     messages=[
#         {"role":"system","content":"You are a virtual assistant named Jarvis skilled in genral tasks like Alexa and Google Cloud.Give short responses please"},
#         {"role":"user","content":command}
#     ]
# )
# return(completion.choices[0].message)

#By Gemini API
Google_API="AIzaSyBzrEgqhf89DWqfvGSbGZQWrLeH_KPrwEs"
genai.configure(api_key=Google_API)
def aiProcess(command):
    model=genai.GenerativeModel("gemini-2.5-flash")
    response=model.generate_content(command)
    return response.text
# for m in genai.list_models():
#     print(m.name)


#by huggingface api
# API_KEY = "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"
# def aiProcess(command):
#     API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # or another chatbot model
#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }
#     payload = {
#         "inputs": command
#     }
#     response = requests.post(API_URL, headers=headers, json=payload)

#     print("Status:",response.status_code)
#     print("Response:",response.text)
    
#     if response.status_code == 200:
        
#         # Extracting text depending on model output format
#         try:
#             result = response.json()
#             if isinstance(result,list):
#                 return result[0]
#             else:
#                 return str(result)
#         except Exception as e:
#             return f"Parsing Error:{e}"
#     else:
#         return f"Error: {response.status_code} - {response.text}"


#for opening any application
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


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    #playing yt videos by importing musicLibrary
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
        # #openAI will handle now
        # output=aiProcess(c)
        # speak(output)
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
            if("stop" in word.lower()):
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