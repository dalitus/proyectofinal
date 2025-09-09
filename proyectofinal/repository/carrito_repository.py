from sqlmodel import Session, select
from proyectofinal.model.carrito_model import Carrito
from proyectofinal.model.product_model import Producto

from proyectofinal.repository.conect_db import engine

def get_carrito_by_user(user_id: int):
    with Session(engine) as session:
        query = select(Carrito).where(Carrito.id_users == user_id)
        carritos = session.exec(query).all()

        # traer productos asociados
        productos = [c.producto for c in carritos if c.producto is not None]
        return productos

from sqlmodel import Session, select
from proyectofinal.model.carrito_model import Carrito
from proyectofinal.model.product_model import Producto
from proyectofinal.repository.conect_db import engine


def insert_carrito(id_users: int, id_producto: int):
    with Session(engine) as session:
        # Verificar si ya existe
        existente = session.exec(
            select(Carrito).where(
                Carrito.id_users == id_users,
                Carrito.id_producto == id_producto
            )
        ).first()

        if existente:
            return existente  # ya estaba agregado

        nuevo_item = Carrito(id_users=id_users, id_producto=id_producto)
        session.add(nuevo_item)
        session.commit()
        session.refresh(nuevo_item)
        return nuevo_item


def select_carrito_by_user(id_users: int) -> list[Producto]:
    """Devuelve los productos del carrito de un usuario"""
    with Session(engine) as session:
        carrito_items = session.exec(
            select(Carrito).where(Carrito.id_users == id_users)
        ).all()

        productos = []
        for item in carrito_items:
            producto = session.get(Producto, item.id_producto)
            if producto:
                productos.append(producto)

        return productos
