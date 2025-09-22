from proyectofinal.repository.detalle_repository import get_producto_por_id
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
        "imagen": _blob_to_data_url(p.imagen_blob) if hasattr(p, "imagen_blob") else "",
    }


def obtener_detalle_producto(producto_id: int) -> dict:
    producto = get_producto_por_id(producto_id)
    if producto is None:
        return {}
    return producto_to_dict(producto)