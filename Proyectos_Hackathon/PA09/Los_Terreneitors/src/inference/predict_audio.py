from src.models.audio.service import predict_audio

def predict_audio_unified(audio_path: str):
    return predict_audio(audio_path)
