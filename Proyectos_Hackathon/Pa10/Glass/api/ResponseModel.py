from datetime import date

from sqlmodel import SQLModel

class PacienteBaseModel(SQLModel):

    cedula: str
    name: str
    altura: int
    peso: int

class ChequeoBaseModel(SQLModel):

    cedula_paciente: str
    tipo: str
    descripcion: str