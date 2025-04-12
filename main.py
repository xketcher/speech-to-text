# server.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

app = FastAPI()

@app.post("/myanmar-voice-to-text/")
async def myanmar_voice_to_text(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily (assumed to be .3gp)
        original_ext = file.filename.split('.')[-1]
        raw_filename = f"temp_{uuid.uuid4().hex}"
        input_path = f"{raw_filename}.{original_ext}"
        wav_path = f"{raw_filename}.wav"

        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Convert 3gp to WAV (16-bit PCM)
        audio = AudioSegment.from_file(input_path)
        audio.export(wav_path, format="wav", parameters=["-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000"])

        # Recognize the WAV audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="my-MM")

        # Clean up temporary files
        os.remove(input_path)
        os.remove(wav_path)

        return {"text": text}

    except sr.UnknownValueError:
        return JSONResponse(content={"error": "Could not understand audio"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
