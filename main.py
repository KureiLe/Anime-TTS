import speech_recognition as sr
import pyttsx3
import keyboard

# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# So that button click dont work when its in process
inProcess = 0

# Define a function to handle the button press event
def button_press():
    with sr.Microphone() as source:
        inProcess = 1
        print("Speak now...")
        audio = r.listen(source)
    try:
        # Use the speech recognition engine to convert speech to text
        voiceResult = r.recognize_google(audio)
        print("You said: " + voiceResult)

        engine.runAndWait()
        inProcess = 0
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        inProcess = 0
    except sr.RequestError as e:
        print("Error: " + str(e))
        inProcess = 0

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed("f") and inProcess == 0:
            # Call the button_press() function to start listening for speech
            button_press()