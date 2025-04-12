from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import speech_recognition as sr
import os, uuid

app = FastAPI()

@app.post("/myanmar-voice-to-text/")
async def myanmar_voice_to_text(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        ext = file.filename.split('.')[-1]
        temp_input = f"temp_{uuid.uuid4().hex}.{ext}"
        temp_wav = f"temp_{uuid.uuid4().hex}.wav"

        with open(temp_input, "wb") as f:
            f.write(await file.read())

        # Convert to WAV
        sound = AudioSegment.from_file(temp_input)
        sound.export(temp_wav, format="wav")

        # Recognize
        r = sr.Recognizer()
        with sr.AudioFile(temp_wav) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="my-MM")

        os.remove(temp_input)
        os.remove(temp_wav)

        return {"text": text}
    
    except sr.UnknownValueError:
        return JSONResponse(content={"error": "Could not understand audio"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
