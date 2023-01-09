import speech_recognition as sr
from google_trans_new import google_translator
from gtts import gTTS
from playsound import playsound
import subprocess

r = sr.Recognizer()
translator = google_translator()

input_file ="/home/shalu/Downloads/hello.mp3"
output_file = "/home/shalu/PycharmProjects/textsetiment/hello.wav"

# Run ffmpeg as a subprocess to convert the file
subprocess.run(["ffmpeg", "-i", input_file, output_file])


# Open the audio file using the SpeechRecognition library
with sr.AudioFile(output_file) as source:
    # Read the audio file into memory
    audio = r.record(source)

# Now you can use the `recognize_google()` method to transcribe the audio as before
    try:
        speech_text = r.recognize_google(audio)
        print("english test",speech_text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Error connecting to the API")

# You can also use the `translate()` method from the Google Cloud Translation API to translate the text
    translated_text = translator.translate(speech_text,lang_tgt='hi')
    print("Hindi sentences",translated_text)
    voice = gTTS(translated_text,lang = "hi")
    voice.save("voice.mp3")
    playsound("voice.mp3")