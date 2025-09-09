import reflex as rx
from typing import Optional
from sqlmodel import Field

class Envios(rx.Model, table=True):
    __tablename__ = "envios"
    id_envio: Optional[int] = Field(default=None, primary_key=True)
    postal: str
    provincia: str
    ciudad: str
    total: int
