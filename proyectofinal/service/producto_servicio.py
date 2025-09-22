
from sqlmodel import Session, select
from proyectofinal.model.product_model import Producto
from proyectofinal.repository import producto_repocitory
from proyectofinal.repository.conect_db import engine, session
from proyectofinal.repository.producto_repocitory import create_producto
from proyectofinal.service.google_drive_service import upload_image_to_drive
import tempfile


def _detect_image_kind(blob: bytes) -> str | None:
    """Detecta tipo de imagen por los bytes iniciales (magic bytes).

    Devuelve 'jpeg', 'png', 'gif', 'webp', 'bmp' o None si no parece imagen.
    """
    if not blob or len(blob) < 4:
        return None
    # JPEG
    if blob[0:2] == b"\xff\xd8":
        return "jpeg"
    # PNG
    if blob[0:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    # GIF (GIF87a or GIF89a)
    if blob[0:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    # WEBP (RIFF....WEBP)
    if blob[0:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return "webp"
    # BMP
    if blob[0:2] == b"BM":
        return "bmp"
    return None

# Obtener todos los productos
def obtener_productos() -> list[Producto]:
    with Session(engine) as session:
        productos_raw = session.exec(select(Producto)).all()
        return productos_raw

# Obtener producto por ID
def obtener_producto_por_id(id_producto: int) -> Producto | None:
    return producto_repocitory.get_producto_by_id(id_producto)


def crear_producto(nombre, descripcion, precio, marca, categoria, talle, imagen_bytes: bytes, imagen_filename: str = None) -> Producto:
    if not nombre or precio is None:
        raise ValueError("Nombre y precio son obligatorios.")
    image_url = None
    if imagen_bytes:
        # Guardar temporalmente la imagen para subirla a Drive
        with tempfile.NamedTemporaryFile(delete=False, suffix=imagen_filename or ".jpg") as tmp:
            tmp.write(imagen_bytes)
            tmp.flush()
            image_url = upload_image_to_drive(tmp.name, imagen_filename)
        # Eliminar archivo temporal
        try:
            os.remove(tmp.name)
        except Exception:
            pass
    nuevo = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        marca=marca,
        categoria=categoria,
        talle=talle,
        image_url=image_url
    )
    return create_producto(nuevo)


# Editar producto existente
def editar_producto(producto_id: int, data: dict) -> bool:
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return False

    for campo, valor in data.items():
        if hasattr(producto, campo) and valor is not None and valor != "":
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

