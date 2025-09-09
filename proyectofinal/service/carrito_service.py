from proyectofinal.repository.carrito_repository import get_carrito_by_user
from proyectofinal.model.product_model import Producto
from sqlmodel import Session, select
from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import engine  # tu engine

from proyectofinal.repository.carrito_repository import insert_carrito, select_carrito_by_user
from proyectofinal.service.users_service import get_usuario_logueado

from proyectofinal.model.carrito_model import Carrito
from proyectofinal.repository.conect_db import get_session  # tu sesión de BD

def eliminar_producto_carrito(user_id: int, producto_id: int):
    # Busca el producto en el carrito del usuario
    item = get_session.query(Carrito).filter_by(user_id=user_id, producto_id=producto_id).first()
    if item:
        get_session.delete(item)
        get_session.commit()



def agregar_carrito_service(producto_id: int):
    user = get_usuario_logueado()
    if not user:
        raise Exception("No hay usuario logueado")
    return insert_carrito(user.id_users, producto_id)


def obtener_productos_carrito():
    user = get_usuario_logueado()
    if not user:
        return []
    return select_carrito_by_user(user.id_users)

    
def obtener_carrito_usuario(user_id: int) -> list[Producto]:
    """
    Servicio para obtener los productos del carrito de un usuario.
    """
    return get_carrito_by_user(user_id)


def agregar_al_carrito(user_id: int, producto_id: int):
    with Session(engine) as session:
        existente = session.exec(
            select(Carrito).where(
                Carrito.id_users == user_id,
                Carrito.id_producto == producto_id
            )
        ).first()
        
        if existente:
            print("Producto ya agregado")
            return
        
        nuevo_item = Carrito(id_users=user_id, id_producto=producto_id)
        session.add(nuevo_item)
        session.commit()
        print(f"Producto {producto_id} agregado al carrito del usuario {user_id}")
