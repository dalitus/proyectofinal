from sqlmodel import Session, select
from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import engine

def get_items_por_usuario(id_users: int) -> list[dict]:
    with Session(engine) as session:
        query = select(Carrito).where(Carrito.id_users == id_users)
        resultados = session.exec(query).all()
        return [carrito.producto.dict() for carrito in resultados if carrito.producto]

def agregar_item_al_carrito(id_users: int, id_producto: int) -> None:
    with Session(engine) as session:
        nuevo_item = Carrito(id_users=id_users, id_producto=id_producto)
        session.add(nuevo_item)
        session.commit()

def eliminar_item_del_carrito(id_users: int, id_producto: int) -> None:
    with Session(engine) as session:
        query = select(Carrito).where(
            Carrito.id_users == id_users,
            Carrito.id_producto == id_producto
        )
        item = session.exec(query).first()
        if item:
            session.delete(item)
            session.commit()

def vaciar_carrito(id_users: int) -> None:
    with Session(engine) as session:
        query = select(Carrito).where(Carrito.id_users == id_users)
        items = session.exec(query).all()
        for item in items:
            session.delete(item)
        session.commit()