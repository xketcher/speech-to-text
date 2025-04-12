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
        # Save uploaded file
        filename = f"temp_{uuid.uuid4().hex}.wav"
        with open(filename, "wb") as f:
            f.write(await file.read())

        # Use speech recognition
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="my-MM")

        os.remove(filename)
        return {"text": text}
    except sr.UnknownValueError:
        return JSONResponse(content={"error": "Could not understand audio"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
