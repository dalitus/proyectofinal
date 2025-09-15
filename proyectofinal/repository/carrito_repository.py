from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import get_session
from sqlmodel import select

# ✅ Agregar un producto al carrito
def agregar_item_al_carrito(user_id: int, producto_id: int):
    nuevo_item = Carrito(id_users=user_id, id_producto=producto_id)
    with get_session() as session:
        session.add(nuevo_item)
        session.commit()

# ✅ Obtener todos los ítems del carrito de un usuario
def get_items_por_usuario(user_id: int) -> list[Carrito]:
    with get_session() as session:
        query = select(Carrito).where(Carrito.id_users == user_id)
        return session.exec(query).all()

# ✅ Eliminar un ítem del carrito por ID
def eliminar_item_del_carrito(id_carrito: int) -> bool:
    with get_session() as session:
        item = session.get(Carrito, id_carrito)
        if item:
            session.delete(item)
            session.commit()
            return True
        return False