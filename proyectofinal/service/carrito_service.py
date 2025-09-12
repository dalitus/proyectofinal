from proyectofinal.repository.carrito_repository import agregar_item_al_carrito

def agregar_al_carrito(user_id: int, producto_id: int):
    agregar_item_al_carrito(user_id, producto_id)