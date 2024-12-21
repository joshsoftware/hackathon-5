from fastapi import FastAPI, HTTPException,UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from audio_service import translate_with_whisper
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import shutil
from pathlib import Path
import os
import tempfile
import pickle

app = FastAPI()

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root_route():
    return 'Hello, this is the root route for lingo ai server'

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-audio")
async def upload_audio(audioFile: UploadFile = File(...)):
    try:

        # Check file type
        if not audioFile.filename.endswith(('m4a', 'mp4','mp3','webm','mpga','wav','mpeg')):
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Create a temporary file to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audioFile.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            # Save the file
            with open(temp_file_path, "wb") as buffer:
                buffer.write(await audioFile.read())

        #translation = translate_with_ollama(transcription)
        translation = translate_with_whisper(temp_file_path)
        os.remove(temp_file_path)
        # Load model and vectorizer
        
        model1 = joblib.load('/home/josh/Hackthon/hackathon-team-4/service/model (2).pkl')
        print("model loaded")
        vectorizer = TfidfVectorizer()
        vect = vectorizer.transform([translation])
        prediction = model1.predict(vect)

        # Return prediction result
        return JSONResponse(content={"spam": bool(prediction[0])}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

