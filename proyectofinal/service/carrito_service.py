from proyectofinal.repository.carrito_repository import (
    get_items_por_usuario,
    agregar_item_al_carrito,
    eliminar_item_del_carrito,
    vaciar_carrito
)

def cargar_carrito_service(id_users: int) -> list[dict]:
    return get_items_por_usuario(id_users)

def agregar_producto_service(id_users: int, id_producto: int) -> None:
    agregar_item_al_carrito(id_users, id_producto)

def eliminar_producto_service(id_users: int, id_producto: int) -> None:
    eliminar_item_del_carrito(id_users, id_producto)

def finalizar_compra_service(id_users: int) -> None:
    vaciar_carrito(id_users)