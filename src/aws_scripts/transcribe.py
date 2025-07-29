
from fastapi import FastAPI, File, UploadFile
import whisper, tempfile

app = FastAPI()
model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp.flush()
    result = model.transcribe(tmp.name)
    return {"transcript": result["text"]}
