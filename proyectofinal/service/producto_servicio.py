from sqlmodel import Session, select
from proyectofinal.model.product_model import Producto
from proyectofinal.repository import producto_repocitory
from proyectofinal.repository.conect_db import engine

def obtener_productos() -> list[Producto]:
    with Session(engine) as session:
        productos_raw = session.exec(select(Producto)).all()
        return productos_raw

def crear_producto(nombre, descripcion, precio, marca, categoria, talle, imagen) -> Producto:
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

def eliminar_producto(id_producto: int) -> bool:
    return producto_repocitory.delete_producto(id_producto)

def editar_producto(id_producto: int, data: dict) -> Producto | None:
    return producto_repocitory.update_producto(id_producto, data)

def buscar_productos(nombre: str) -> list[Producto]:
    return producto_repocitory.buscar_productos_por_nombre(nombre)