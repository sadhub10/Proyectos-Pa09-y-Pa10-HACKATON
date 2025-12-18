import os
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report

from src.features.audio_features import extract_audio_features

# ============================
# CONFIG
# ============================
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = Path("data/samples/audio/AudioWAV") 
MODEL_PATH = BASE_DIR / "audio_model.pkl"
SCALER_PATH = BASE_DIR / "audio_scaler.pkl"

LABELS = {
    "ANG": "Ansiedad",
    "SAD": "Depresión",
    "NEU": "Normal",
}

# ============================
# CARGAR DATASET
# ============================
X, y = [], []

for file in os.listdir(DATASET_DIR):
    if not file.endswith(".wav"):
        continue

    parts = file.split("_")
    emotion_code = parts[2]  # CREMA-D format

    if emotion_code not in LABELS:
        continue

    path = DATASET_DIR / file
    features = extract_audio_features(str(path))

    X.append(features)
    y.append(LABELS[emotion_code])

X = np.array(X)
y = np.array(y)

# ============================
# SPLIT
# ============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ============================
# NORMALIZACIÓN
# ============================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ============================
# MODELO
# ============================
model = SVC(
    kernel="rbf",
    probability=True,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# ============================
# EVALUACIÓN
# ============================
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ============================
# GUARDAR
# ============================
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("Modelo de audio y scaler guardados ✔")
