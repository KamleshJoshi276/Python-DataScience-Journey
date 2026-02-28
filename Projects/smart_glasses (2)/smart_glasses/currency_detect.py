import random, time
from tts import speak

currencies = ["10 rupees", "20 rupees", "50 rupees", "100 rupees", "500 rupees"]

def detect_currency():
    note = random.choice(currencies)
    speak(f"{note} note detected")
    time.sleep(2)
