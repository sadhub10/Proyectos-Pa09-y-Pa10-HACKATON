from fastapi import APIRouter, HTTPException

__all__ = ["chequeo"]

from sqlmodel import select

from Proyectos_Hackathon.Pa10.Glass.api.ResponseModel import PacienteBaseModel, ChequeoBaseModel
from Proyectos_Hackathon.Pa10.Glass.api.db import SessionDep
from Proyectos_Hackathon.Pa10.Glass.api.tables import Chequeo, Paciente

chequeo = APIRouter(prefix ="/chequeo", tags = ["Chequeo"])

@chequeo.get("")
def get_all_chequeos(
        session: SessionDep
):
    chequeos = session.exec(select(Chequeo)).all()

    if not chequeos:
        raise HTTPException(status_code=404, detail= "No hay chequeos")

    return chequeos

@chequeo.post("")
def create_chequeo(
        session: SessionDep,
        chequeo: ChequeoBaseModel
):
    paciente = session.get(Paciente, chequeo.cedula_paciente)
    if not paciente:
        raise HTTPException(status_code=404, detail= "El paciente no existe")
    new_chequeo = Chequeo(
        cedula_paciente=chequeo.cedula_paciente,
        tipo=chequeo.tipo,
        descripcion=chequeo.descripcion
    )
    session.add(new_chequeo)
    session.commit()
    session.refresh(new_chequeo)

    return {'message': 'Expediente creado correctamente'}