from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import get_session
from sqlmodel import select


def get_items_por_usuario(user_id: int) -> list[Carrito]:
    with get_session() as session:
        query = select(Carrito).where(Carrito.id_users == user_id)
        return session.exec(query).all()

def agregar_item_al_carrito(user_id: int, producto_id: int):
    with get_session() as session:
        item = Carrito(id_usuario=user_id, id_producto=producto_id)
        session.add(item)
        session.commit()

def eliminar_item_del_carrito(user_id: int, producto_id: int):
    with get_session() as session:
        query = select(Carrito).where(
            Carrito.id_usuario == user_id,
            Carrito.id_producto == producto_id
        )
        item = session.exec(query).first()
        if item:
            session.delete(item)
            session.commit()