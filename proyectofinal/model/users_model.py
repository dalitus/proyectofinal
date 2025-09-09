import reflex as rx
from typing import Optional,List,TYPE_CHECKING
from sqlmodel import SQLModel, Field, Field, Relationship

if TYPE_CHECKING:
    from proyectofinal.model.carrito_model import Carrito

class Users(rx.Model, table=True):
    __tablename__ = "users"
    id_users: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    contrasena: str
    email: str
    telefono: str
    
    carritos: List["Carrito"] = Relationship(back_populates="usuario")