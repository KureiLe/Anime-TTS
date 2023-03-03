import speech_recognition as sr
import keyboard
import voicevox
import googletrans
import asyncio
import playsound


# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
# Configure google translate real
translator = googletrans.Translator()

# Define a function to handle the button press event
async def button_pressed():
    # So that button click dont work when its in process
    inProcess = 0
    # File count
    fileCount = 1
    while True:
        if keyboard.is_pressed("f") and inProcess == 0:
            with sr.Microphone() as source:
                inProcess = 1
                print("Speak now...")
                audio = r.listen(source, timeout=3, phrase_time_limit=20)
            try:
                # Use the speech recognition engine to convert speech to text
                voiceResult = r.recognize_google(audio)
                print("You said: " + voiceResult)

                # Translate text
                resultTranslated = translator.translate(voiceResult, dest="ja").text
                print(f"Translated: {resultTranslated}")

                # Put it to mp3 file
                async with voicevox.Client() as client:
                    audio_query = await client.create_audio_query(
                        resultTranslated, speaker=20
                    )
                    with open(f"./results/result{fileCount}.wav", "wb") as f:
                        f.write(await audio_query.synthesis())
                        f.close()
                
                print(f"Done {fileCount}.wav")
                # Play audio
                playsound.playsound(f"./results/result{fileCount}.wav")
                
                fileCount += 1
                inProcess = 0
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")
                inProcess = 0
            except sr.RequestError as e:
                print("Error: " + str(e))
                inProcess = 0

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(button_pressed())
    loop.run_until_complete()