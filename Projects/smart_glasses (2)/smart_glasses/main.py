from tts import speak
from object_detect import detect_object
from obstacle import check_obstacle
from currency_detect import detect_currency
import time


if __name__ == "__main__":
    speak("Smart Glasses system starting")
    time.sleep(1)

    while True:
        detect_object()       # object detection demo
        check_obstacle()      # obstacle detection demo
        detect_currency()     # currency detection demo
        speak("System running normally")
        time.sleep(3)
