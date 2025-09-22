from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal

if TYPE_CHECKING:
    from proyectofinal.model.stock_model import Stocks
    from proyectofinal.model.carrito_model import Carrito

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id_producto: int = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio: Decimal
    marca: str
    categoria: str
    talle: str
    image_url: Optional[str] = Field(default=None, description="URL pública de la imagen en Google Drive")
    id_stock: Optional[int] = Field(default=None, foreign_key="stocks.id_stock")

    stock: Optional["Stocks"] = Relationship(back_populates="productos")
    
    # Relación con Carrito
    carritos: List["Carrito"] = Relationship(back_populates="producto")

