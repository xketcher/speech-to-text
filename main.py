import subprocess
import uuid
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
import os

app = FastAPI()
model = WhisperModel("small")

@app.post("/myanmar-voice-to-text/")
async def transcribe_audio(file: UploadFile = File(...)):
    original_path = f"temp/{uuid.uuid4()}.3gp"
    wav_path = original_path.replace(".3gp", ".wav")

    with open(original_path, "wb") as f:
        f.write(await file.read())

    # Convert to WAV using ffmpeg
    convert_cmd = ["ffmpeg", "-i", original_path, "-ar", "16000", "-ac", "1", wav_path]
    try:
        subprocess.run(convert_cmd, check=True)
    except subprocess.CalledProcessError:
        return JSONResponse(content={"error": "Failed to convert audio to WAV"}, status_code=400)

    try:
        segments, _ = model.transcribe(wav_path)
        text = ''.join([seg.text for seg in segments])
        return {"text": text}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(original_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)
