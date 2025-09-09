import reflex as rx
from typing import Optional
from sqlmodel import Field

class Solicitan(rx.Model, table=True):
    __tablename__ = "solicitan"
    id_solicita: Optional[int] = Field(default=None, primary_key=True)
    precio: int
    cantidad: int
    id_producto: int
    id_presupuesto: int
