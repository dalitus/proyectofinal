import reflex as rx
from typing import Optional
from sqlmodel import SQLModel, Field

class Gerente(SQLModel, table=True):
    __tablename__ = "gerentes"  # Nombre exacto de la tabla en la BD
    id_gerente: int = Field(default=None, primary_key=True)
    nombre: str
    email: str
    contrasenia: str
    telefono: int
