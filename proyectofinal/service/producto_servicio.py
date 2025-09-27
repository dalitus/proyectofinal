from sqlmodel import Session, select
import os
from typing import Optional
from proyectofinal.service.gdrive_service import upload_image_to_drive
from proyectofinal.model.product_model import Producto
from proyectofinal.repository import producto_repocitory
from proyectofinal.repository.conect_db import engine, session

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

    imagen_url: Optional[str] = None
    # Si 'imagen' parece ruta de archivo local, subirla a Drive.
    try:
        print(f"[PRODUCTO] crear_producto: imagen entrada={imagen}")
        if imagen and os.path.isfile(imagen):
            folder_id = os.getenv("GDRIVE_FOLDER_ID")
            print(f"[PRODUCTO] Subiendo imagen local a Drive. folder_id={folder_id}")
            imagen_url = upload_image_to_drive(imagen, folder_id=folder_id, producto_nombre=nombre)
            print(f"[PRODUCTO] URL recibida de Drive: {imagen_url}")
        else:
            # Si no es archivo local, asumimos que ya es una URL
            imagen_url = imagen
    except Exception as e:
        import traceback
        print(f"[PRODUCTO] Error subiendo imagen: {e}")
        traceback.print_exc()
        # Si la imagen no es URL válida, evitar guardar la ruta local
        imagen_url = imagen if (isinstance(imagen, str) and imagen.startswith("http")) else ""
    nuevo = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        marca=marca,
        categoria=categoria,
        talle=talle,
        imagen=imagen_url
    )
    return producto_repocitory.create_producto(nuevo)

# Editar producto existente
def editar_producto(producto_id: int, data: dict) -> bool:
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False

    for campo, valor in data.items():
        if hasattr(producto, campo) and valor is not None and valor != "":
            if campo == "imagen":
                try:
                    print(f"[PRODUCTO] editar_producto: campo imagen valor={valor}")
                    if valor and os.path.isfile(valor):
                        folder_id = os.getenv("GDRIVE_FOLDER_ID")
                        print(f"[PRODUCTO] Subiendo imagen local a Drive. folder_id={folder_id}")
                        valor = upload_image_to_drive(valor, folder_id=folder_id, producto_nombre=producto.nombre)
                        print(f"[PRODUCTO] URL recibida de Drive: {valor}")
                except Exception:
                    print("[PRODUCTO] Error subiendo imagen, se mantiene valor.")
            setattr(producto, campo, valor)

    session.add(producto)
    session.commit()
    return True


# Eliminar producto por ID
def eliminar_producto(id_producto: int) -> bool:
    return producto_repocitory.delete_producto(id_producto)

# Buscar productos por nombre
def buscar_productos(nombre: str) -> list[Producto]:
    return producto_repocitory.buscar_productos_por_nombre(nombre)

# Búsqueda general por texto (nombre, marca, categoría, etc.)
def buscar_productos_por_texto(texto: str) -> list[Producto]:
    return producto_repocitory.buscar_productos_por_texto(texto)