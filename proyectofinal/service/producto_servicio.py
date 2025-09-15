from sqlmodel import Session, select
from proyectofinal.model.product_model import Producto
from proyectofinal.repository import producto_repocitory
from proyectofinal.repository.conect_db import engine

# Obtener todos los productos
def obtener_productos() -> list[Producto]:
    with Session(engine) as session:
        productos_raw = session.exec(select(Producto)).all()
        return productos_raw

# Obtener producto por ID
def obtener_producto_por_id(id_producto: int) -> Producto | None:
    return producto_repocitory.get_producto_by_id(id_producto)

# Crear nuevo producto con validación mínima
def crear_producto(nombre, descripcion, precio, marca, categoria, talle, imagen) -> Producto:
    if not nombre or precio is None:
        raise ValueError("Nombre y precio son obligatorios.")
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

# Editar producto existente
def editar_producto(id_producto: int, data: dict) -> Producto | None:
    return producto_repocitory.update_producto(id_producto, data)

# Eliminar producto por ID
def eliminar_producto(id_producto: int) -> bool:
    return producto_repocitory.delete_producto(id_producto)

# Buscar productos por nombre
def buscar_productos(nombre: str) -> list[Producto]:
    return producto_repocitory.buscar_productos_por_nombre(nombre)

# Búsqueda general por texto (nombre, marca, categoría, etc.)
def buscar_productos_por_texto(texto: str) -> list[Producto]:
    return producto_repocitory.buscar_productos_por_texto(texto)