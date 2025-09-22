from proyectofinal.repository.catalogo_repository import get_all_productos, buscar_productos_por_texto
from proyectofinal.model.product_model import Producto
import base64


def _detect_image_kind(blob: bytes) -> str | None:
    if not blob or len(blob) < 4:
        return None
    if blob[0:2] == b"\xff\xd8":
        return "jpeg"
    if blob[0:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if blob[0:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if blob[0:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return "webp"
    if blob[0:2] == b"BM":
        return "bmp"
    return None


def _blob_to_data_url(blob: bytes) -> str:
    """Convierte bytes de imagen en un data URL (base64)."""
    if not blob:
        return ""
    kind = _detect_image_kind(blob)
    if kind is None:
        mime = "application/octet-stream"
    else:
        mime = "image/jpeg" if kind == "jpeg" else f"image/{kind}"
    b64 = base64.b64encode(blob).decode("ascii")
    return f"data:{mime};base64,{b64}"


def producto_to_dict(p: Producto) -> dict:
    return {
        "id_producto": p.id_producto,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio": float(p.precio),
        "marca": p.marca,
        "categoria": p.categoria,
        "talle": p.talle,
        # convertimos el blob almacenado en la DB a un data URL para la UI
        "imagen": _blob_to_data_url(p.imagen_blob) if hasattr(p, "imagen_blob") else "",
    }

def obtener_catalogo() -> list[dict]:
    return [producto_to_dict(p) for p in get_all_productos()]

def buscar_en_catalogo(texto: str) -> list[dict]:
    return [producto_to_dict(p) for p in buscar_productos_por_texto(texto)]