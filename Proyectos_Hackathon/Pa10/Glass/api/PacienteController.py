from fastapi import APIRouter, HTTPException

__all__ = ["paciente"]

from sqlmodel import select

from Proyectos_Hackathon.Pa10.Glass.api.ResponseModel import PacienteBaseModel
from Proyectos_Hackathon.Pa10.Glass.api.db import SessionDep
from Proyectos_Hackathon.Pa10.Glass.api.tables import Paciente

paciente = APIRouter(prefix = "/paciente", tags = ["Paciente"])

@paciente.get("")
def get_all_paciente(
        session: SessionDep
):
    pacientes = session.exec(select(Paciente)).all()

    if not pacientes:
        raise HTTPException(status_code=404, detail= "No hay expedientes")

    return pacientes

@paciente.post("")
def create_paciente(
        session: SessionDep,
        paciente: PacienteBaseModel
):
    new_paciente = Paciente.model_validate(paciente)
    session.add(new_paciente)
    session.commit()
    session.refresh(new_paciente)

    return {'message': 'Expediente creado correctamente'}