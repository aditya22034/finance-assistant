from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import whisper
from gtts import gTTS
import tempfile
import os
import uuid

app = FastAPI()

model = whisper.load_model("base")

@app.post("/stt")
def transcribe_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)
        os.remove(tmp_path)

        return {"transcript": result["text"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/tts")
def speak(text: str):
    try:
        audio_filename = f"response_{uuid.uuid4().hex}.mp3"

        tts = gTTS(text)
        tts.save(audio_filename)

        return FileResponse(
            path=audio_filename,
            media_type="audio/mpeg",
            filename=audio_filename,
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
