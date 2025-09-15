from proyectofinal.repository.carrito_repository import agregar_item_al_carrito
from proyectofinal.repository.users_repository import get_user_by_id
from proyectofinal.repository.producto_repocitory import get_producto_by_id

def agregar_al_carrito(user_id: int, producto_id: int) -> dict:
    usuario = get_user_by_id(user_id)
    producto = get_producto_by_id(producto_id)

    if not usuario:
        return {"status": "error", "mensaje": "Usuario no encontrado"}

    if not producto:
        return {"status": "error", "mensaje": "Producto no encontrado"}

    try:
        agregar_item_al_carrito(user_id, producto_id)
        return {"status": "ok", "mensaje": "Producto agregado al carrito"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "mensaje": f"Error al agregar al carrito: {e}"}