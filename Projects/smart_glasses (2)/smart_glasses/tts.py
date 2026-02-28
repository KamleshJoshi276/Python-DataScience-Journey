"""import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # बोलने की गति सेट करें

def speak(text):
    print("SPEAK:", text)
    engine.say(text)
    engine.runAndWait()"""

from gtts import gTTS
from playsound import playsound
import os
import threading
import time
import random

def speak(text):
    def run():
        try:
            print("SPEAK:", text)
            # हर बार नया filename ताकि conflict न हो
            filename = f"voice_{random.randint(1000,9999)}.mp3"
            tts = gTTS(text=text, lang='en')
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            print("Error in speak:", e)

    threading.Thread(target=run, daemon=True).start()
