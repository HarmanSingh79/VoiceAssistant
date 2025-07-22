# VoiceAssistant
It's a simple voice model something like AmazonAlexa

# Voice Assistant in Python 🎙️
This is a simple voice assistant project built using Python.

## Features:
- Opens websites via voice.
- Opens system apps via voice.
- Speaks replies using gTTS(works online, pyttsx3 can also be used which works offline also).
- Plays songs from predefined musicLibrary.
- Uses Gemini-2.5-flash for responses.
- Can be extended with Spotify/YT APIs but here pywhatkit is used.4
- Latest headlines.

## API's used:
-News API-https://newsapi.org/ 
-Google Gemini-https://aistudio.google.com (HuggingFace API's can also be used, but the implementation would be a bit different for that)

## How to run:
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate it:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install requirements:
   ```bash
   pip install -r requirements.txt
