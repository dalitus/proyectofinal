from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import engine
from proyectofinal.model.product_model import Producto
from proyectofinal.model import Carrito, Producto, Users

from collections import defaultdict

def obtener_carrito_agrupado_por_usuario(db: Session, id_users: int) -> list[dict]:
    resultados = obtener_carrito_completo_por_usuario(db, id_users)
    agrupados = defaultdict(lambda: {"cantidad": 0, "subtotal": 0.0})

    for carrito, producto, usuario in resultados:
        pid = producto.id_producto
        if "nombre" not in agrupados[pid]:
            agrupados[pid].update({
                "id_producto": pid,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "imagen": producto.imagen
            })
        agrupados[pid]["cantidad"] += 1
        agrupados[pid]["subtotal"] += producto.precio

    return list(agrupados.values())

def obtener_carrito_completo_por_usuario(db: Session, id_users: int):
    return (
        db.query(Carrito, Producto, Users)
        .join(Producto, Carrito.id_producto == Producto.id_producto)
        .join(Users, Carrito.id_users == Users.id_users)
        .filter(Carrito.id_users == id_users)
        .all()
    )

def get_items_por_usuario(user_id: int) -> list[dict]:
    with Session(engine) as session:
        resultados = session.exec(
            select(Carrito).where(Carrito.id_users == user_id)  # ✅ corregido
        ).all()
        return [r.dict() for r in resultados]

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