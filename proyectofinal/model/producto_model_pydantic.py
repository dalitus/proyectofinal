from pydantic import BaseModel

class ProductoModel(BaseModel):
    id_producto: int
    nombre: str
    descripcion: str
    precio: float
    marca: str
    categoria: str
    talle: str
    imagen: str = ""
