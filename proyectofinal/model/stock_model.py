from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from proyectofinal.model.product_model import Producto

class Stocks(SQLModel, table=True):
    __tablename__ = "stocks"

    id_stock: int = Field(default=None, primary_key=True)
    cantidad_disponible: int

    productos: List["Producto"] = Relationship(back_populates="stock")
