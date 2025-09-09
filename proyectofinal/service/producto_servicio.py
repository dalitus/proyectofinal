import reflex as rx
from proyectofinal.model.product_model import Producto
from proyectofinal.repository import producto_repocitory
from sqlmodel import Session
from sqlmodel import select

from proyectofinal.model.product_model import Producto
from sqlmodel import Session, select
from proyectofinal.repository.conect_db import engine  # o donde tengas definido tu engine

def obtener_productos():
    with Session(engine) as session:
        productos_raw = session.exec(select(Producto)).all()
        return productos_raw

def crear_producto(nombre, descripcion, precio, marca, categoria, talle, imagen):
    nuevo = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        marca=marca,
        categoria=categoria,
        talle=talle,
        imagen=imagen
    )
    return producto_repocitory.create_producto(nuevo)

def eliminar_producto(id_producto: int):
    return producto_repocitory.delete_producto(id_producto)

def editar_producto(id_producto: int, data: dict):
    return producto_repocitory.edit_producto(id_producto, data)

def buscar_productos(nombre: str) -> list[Producto]:
    """Busca productos cuyo nombre contenga el texto dado."""
    with Session(engine) as session:
        statement = select(Producto).where(Producto.nombre.ilike(f"%{nombre}%"))
        return session.exec(statement).all()
