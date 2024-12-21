import whisper

#load the whisper model from net if it isn't stored locally
def load_model(model_id, model_path):
    model = whisper.load_model(model_id, download_root=model_path)
    return model