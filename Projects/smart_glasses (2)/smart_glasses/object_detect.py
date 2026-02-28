import random, time
from tts import speak

objects = ["person", "chair", "bottle", "dog", "car"]

def detect_object():
    # random simulate detection
    obj = random.choice(objects)
    speak(f"{obj} detected ahead")
    time.sleep(2)
