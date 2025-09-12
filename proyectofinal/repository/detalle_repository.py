from proyectofinal.model.product_model import Producto
from proyectofinal.repository.conect_db import get_session

def get_producto_por_id(producto_id: int) -> Producto | None:
    with get_session() as session:
        return session.get(Producto, producto_id)