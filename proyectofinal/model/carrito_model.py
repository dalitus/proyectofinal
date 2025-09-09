from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from proyectofinal.model.product_model import Producto
from proyectofinal.model.users_model import Users

class Carrito(SQLModel, table=True):
    __tablename__ = "carritos"

    id_carrito: Optional[int] = Field(default=None, primary_key=True)
    id_users: int = Field(foreign_key="users.id_users")
    id_producto: int = Field(foreign_key="productos.id_producto")  # <- corregido

    usuario: Optional[Users] = Relationship(back_populates="carritos")
    producto: Optional[Producto] = Relationship(back_populates="carritos")

