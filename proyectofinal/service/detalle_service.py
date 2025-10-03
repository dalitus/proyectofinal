import reflex as rx
from proyectofinal.model.product_model import Producto
from proyectofinal.repository.producto_repocitory import get_producto_by_id

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
    try:
        producto = get_producto_by_id(producto_id)
        if producto:
            return producto_to_dict(producto)
        else:
            print(f"[ERROR] obtener_detalle_producto: Producto con ID {producto_id} no encontrado.")
            return {}
    except Exception as e:
        print(f"[ERROR] obtener_detalle_producto: {e}")
        return {}