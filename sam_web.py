from fastapi import (
    FastAPI,
    UploadFile,
    File
)
# from starlette.responses import FileResponse
from fastapi.responses import FileResponse
import speech_recognition as sr
from gtts import gTTS
import subprocess
from deep_translator import GoogleTranslator
import translators as ts
import os
import shutil
app = FastAPI()
def translate_audio(file_location):
    # input_file ="hry_us.mp3"
    input_file = file_location
    output_file = "files/hello.wav"
    if os.path.isfile('files/hello.wav'):
        os.remove('files/hello.wav')
    if os.path.isfile('files/voice.mp3'):
        os.remove('files/voice.mp3')
    # Run ffmpeg as a subprocess to convert the file
    subprocess.run(["ffmpeg", "-i", input_file, output_file])
    # Open the audio file using the SpeechRecognition library
    r = sr.Recognizer()
    with sr.AudioFile(output_file) as source:
        # Read the audio file into memory
        audio = r.record(source)
    # Now you can use the `recognize_google()` method to transcribe the audio as before
        try:
            speech_text = r.recognize_google(audio)
            print('speec t ', speech_text)
            translator = GoogleTranslator(source='auto', target='hi')
            translated_text = translator.translate(speech_text)
            voice = gTTS(translated_text, lang = "hi")
            voice.save("files/voice.mp3")
            return FileResponse('files/voice.mp3', media_type='audio/mpeg',filename="voice.mp3")
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError:
            print("Error connecting to the API")
def upload_audio(audioFile):
    file_location = f"files/{audioFile.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(audioFile.file, buffer)
    return file_location
@app.post("/translate", summary="Translate audio to hindi")
async def translate(audioFile: UploadFile = File(...)):
    file_location = upload_audio(audioFile) #upload audio file
    audio = translate_audio(file_location)
    if os.path.isfile(file_location):
        os.remove(file_location)
    return audio







