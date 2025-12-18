import librosa
import numpy as np

def extract_audio_features(audio_path: str, sr: int = 22050) -> np.ndarray:
    """
    Extrae features acústicos clásicos desde un archivo WAV
    """
    y, sr = librosa.load(audio_path, sr=sr)

    # MFCCs
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)

    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    # Spectral contrast
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = np.mean(contrast, axis=1)

    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = np.mean(zcr)

    features = np.concatenate([
        mfcc_mean,
        chroma_mean,
        contrast_mean,
        [zcr_mean]
    ])

    return features
