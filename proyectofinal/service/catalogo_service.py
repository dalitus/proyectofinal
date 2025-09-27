from proyectofinal.repository.catalogo_repository import get_all_productos, buscar_productos_por_texto
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

def obtener_catalogo() -> list[dict]:
    return [producto_to_dict(p) for p in get_all_productos()]

def buscar_en_catalogo(texto: str) -> list[dict]:
    return [producto_to_dict(p) for p in buscar_productos_por_texto(texto)]