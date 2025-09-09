import reflex as rx
from typing import Optional
from sqlmodel import Field

class Detalles(rx.Model, table=True):
    __tablename__ = "detalles"
    id_detalle: Optional[int] = Field(default=None, primary_key=True)
    precio: int
    cantidad: int
    id_producto: int
    id_carrito: int
    id_envio: int
