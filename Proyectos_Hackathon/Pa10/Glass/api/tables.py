from datetime import date

from sqlmodel import SQLModel, Field, Column, ForeignKey
from sqlalchemy import String, Integer, Date


class Paciente(SQLModel, table=True):

    __tablename__ = "paciente"

    cedula: str = Field(
        sa_column= Column(String, primary_key=True, nullable=False)
    )
    name: str = Field(
        sa_column=Column(String, index=True)
                      )
    altura: int = Field(Column(Integer, index=True)
                        )
    peso: int = Field(Column(Integer, index=True)
                      )

class Chequeo(SQLModel, table=True):

    __tablename__ = "chequeo"

    id: int = Field(
        sa_column= Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    )
    cedula_paciente: str = Field(
        sa_column= Column(String, ForeignKey(Paciente.cedula, ondelete="CASCADE"), nullable=False),
    )
    tipo: str = Field(
        sa_column=Column(String, index=True)
                      )
    descripcion: str = Field(Column(String, index=True)
                             )
    fecha: date = Field(
        sa_column=Column(Date, nullable=False, default=date.today)
    )
