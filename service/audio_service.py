from fastapi import UploadFile
from dotenv import load_dotenv
from config import  model_id, model_path
from load_model import load_model
import numpy as np
from pydub import AudioSegment
from io import BytesIO
import soundfile as sf


# Load environment variables
load_dotenv()
#Load whisher model
model = load_model(model_id, model_path)

async def convert_uploadfile_to_ndarray(upload_file: UploadFile) -> np.ndarray:

    # Read the audio file from UploadFile
    audio_data = await upload_file.read()

    # Use soundfile to read the audio data into a NumPy array
    # We use a BytesIO object because soundfile expects a file-like object
    audio_file = BytesIO(audio_data)
    
    # Read audio data and sample rate
    data, sample_rate = sf.read(audio_file)

    # Convert the data to single precision (float32)
    data = data.astype(np.float32)

    # Return the numpy array
    return data

#translate the audio file to English language using whisper model
def translate_with_whisper(audioPath):
    options = dict(beam_size=5, best_of=5)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audioPath,**translate_options)
    return result["text"]
