from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from Proyectos_Hackathon.Pa10.Glass.api.ChequeoController import chequeo
from Proyectos_Hackathon.Pa10.Glass.api.PacienteController import paciente
from db import engine
import Proyectos_Hackathon.Pa10.Glass.api.tables

healthy_station = FastAPI(
    title="healthy station",
    description="Final project SIC 2025",
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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=healthy_station, host="0.0.0.0", port=8001)