from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
import os

app = FastAPI()

# Directory where audio files will be saved
UPLOAD_DIRECTORY = "uploaded_audio_files"

# Ensure the directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Get the file type based on file extension
        if not file.filename.endswith(('.m4a', '.mp4', '.mp3', '.webm', '.mpga', '.wav', '.mpeg', '.ogg')):
            raise HTTPException(status_code=400, detail="Invalid file type")

        # Define the path to save the uploaded file
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Save the uploaded file locally without using shutil
        with open(file_path, "wb") as f:
            # Read the file in chunks and write directly to the file
            while chunk := await file.read(1024):  # Read 1024 bytes at a time
                f.write(chunk)

        # Return a response with the file location
        return JSONResponse(content={"message": "File uploaded successfully!", "file_path": file_path}, status_code=200)

    except Exception as e:
        # Handle any unexpected errors
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.get("/")
def index():
    return {"message": "Hello World!"}

# Function for webhook responses
async def results(request: Request):
    try:
        # Parse JSON request body
        req = await request.json()

        # Extract action from the request
        # action = req.get('queryResult', {}).get('action', 'unknown')
        response_text = req.get('queryResult', {}).get('fulfillmentText', 'Default response')
        return JSONResponse(content={"fulfillmentText": response_text})
        # Return a fulfillment response
        # return {"fulfillmentText": f"This is a response from webhook. Action: {action}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")

# Route for webhook
@app.post("/webhook")
async def webhook(request: Request):
    response = await results(request)
    return JSONResponse(content=response)