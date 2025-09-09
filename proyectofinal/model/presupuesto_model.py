import reflex as rx
from typing import Optional
from sqlmodel import Field

class Presupuestos(rx.Model, table=True):
    __tablename__ = "presupuestos"
    id_presupuesto: Optional[int] = Field(default=None, primary_key=True)
    total_presupuesto: int
    id_users: int
