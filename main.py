from fastapi import FastAPI, UploadFile, File from fastapi.responses import JSONResponse from speech_recognition import Recognizer, AudioFile import uuid import os

app = FastAPI() UPLOAD_DIR = "temp" os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/myanmar-voice-to-text/") async def transcribe_audio(file: UploadFile = File(...)): file_id = str(uuid.uuid4()) file_path = os.path.join(UPLOAD_DIR, f"{file_id}.wav")

with open(file_path, "wb") as out_file:
    out_file.write(await file.read())

try:
    recognizer = Recognizer()
    with AudioFile(file_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language="my-MM")
        return {"text": text}
except Exception as e:
    return JSONResponse(content={"error": str(e)}, status_code=400)
finally:
    os.remove(file_path)

