from sqlmodel import select
from proyectofinal.model.product_model import Producto
from proyectofinal.repository.conect_db import get_session

def get_all_productos() -> list[Producto]:
    with get_session() as session:
        return session.exec(select(Producto)).all()

def buscar_productos_por_texto(texto: str) -> list[Producto]:
    with get_session() as session:
        query = select(Producto).where(
            Producto.nombre.ilike(f"%{texto}%") |
            Producto.marca.ilike(f"%{texto}%") |
            Producto.precio.cast(str).ilike(f"%{texto}%")
        )
        return session.exec(query).all()