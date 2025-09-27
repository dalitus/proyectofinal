from proyectofinal.repository.detalle_repository import get_producto_por_id
from proyectofinal.model.product_model import Producto

def producto_to_dict(p: Producto) -> dict:
    return {
        "id_producto": p.id_producto,
        "nombre": p.nombre,
        "descripcion": p.descripcion,
        "precio": float(p.precio),
        "marca": p.marca,
        "categoria": p.categoria,
        "talle": p.talle,
        "imagen": p.imagen or "",
    }

def obtener_detalle_producto(producto_id: int) -> dict:
    producto = get_producto_por_id(producto_id)
    if producto is None:
        return {}
    return producto_to_dict(producto)