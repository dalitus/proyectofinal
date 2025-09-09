from sqlmodel import SQLModel, Field
from typing import Optional

class Consulta(SQLModel, table=True):
    __tablename__ = "consultas"

    id_consulta: Optional[int] = Field(default=None, primary_key=True)
    pregunta: str
    respuesta: Optional[str] = None
    id_users: int
    id_gerente: Optional[int] = None
    fecha_creacion: Optional[str] = None
    fecha_respuesta: Optional[str] = None