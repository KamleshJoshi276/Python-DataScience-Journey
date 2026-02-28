import random, time
from tts import speak

def check_obstacle():
    distance = random.randint(20, 150)
    print("Distance:", distance, "cm")
    if distance < 50:
        speak("Warning! Obstacle ahead.")
    time.sleep(2)
