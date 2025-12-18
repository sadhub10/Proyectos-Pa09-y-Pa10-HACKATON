import numpy as np
from fastapi import APIRouter, FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from tensorflow.keras.models import load_model

from ChequeoController import chequeo
from PacienteController import paciente
from contextlib import asynccontextmanager
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
from db import engine
import Proyectos_Hackathon.Pa10.Glass.api.tables



@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.modelo_neumonia = load_model("model_pneumonia.keras")
    app.state.modelo_tumor = load_model("modeloBrainTumor.keras")
    yield

healthy_station = FastAPI(
    title="healthy station",
    description="Final project SIC 2025",
    lifespan=lifespan,
)

healthy_station.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

healthy_station_v0 = APIRouter(prefix="/v0", tags=["v0"])

SQLModel.metadata.create_all(bind=engine)

healthy_station.include_router(paciente)
healthy_station.include_router(chequeo)

@healthy_station.get("/")
def root():
    """Example endpoint."""
    return {"message": "Welcome to Healthy Station"}


@healthy_station.post("/model-pneumonia")
async def model_pneumonia(file: UploadFile = File(...)):
    modelo = healthy_station.state.modelo_neumonia

    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    resultado = modelo.predict(x)

    clases = ["Saludable", "Neumonía Bacterial", "Neumonía Viral"]
    indice = np.argmax(resultado, axis=1)[0]
    clase_predicha = clases[indice]

    return clase_predicha

@healthy_station.post("/model-tumor")
async def model_tumor(file: UploadFile = File(...)):
    modelo = healthy_station.state.modelo_tumor

    contents = await file.read()
    img = Image.open(BytesIO(contents)).convert("RGB")
    img = img.resize((224,224))

    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)

    resultado = modelo.predict(x)
    probabilidad = float(resultado[0][0])

    clase_predicha = "Tumor" if probabilidad > 0.5 else "Sano"

    return clase_predicha
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=healthy_station, host="0.0.0.0", port=8001)
