import reflex as rx
from sqlmodel import Session
from proyectofinal.repository.conect_db import engine
from proyectofinal.repository.carrito_repository import (
    obtener_carrito_completo_por_usuario,
    vaciar_carrito,
    eliminar_item_del_carrito
)

class AppState(rx.State):
    user_id: int = 0
    logeado: bool = False
    productos_carrito: list[dict] = []
    total: float = 0.0
    mensaje_compra: str = ""

    @rx.event
    def login(self, usuario_id: int):
        self.user_id = usuario_id
        self.logeado = True
        self.cargar_carrito_detallado()

    @rx.event
    def cargar_carrito_detallado(self):
        with Session(engine) as db:
            resultados = obtener_carrito_completo_por_usuario(db, self.user_id)
            self.productos_carrito = [
                {
                    "nombre": producto.nombre,
                    "precio": producto.precio,
                    "id_producto": producto.id_producto,
                    "id_carrito": carrito.id_carrito
                }
                for carrito, producto, usuario in resultados
            ]
            self.total = sum(p["precio"] for p in self.productos_carrito)

    @rx.event
    def eliminar_producto(self, id_producto: int):
        eliminar_item_del_carrito(self.user_id, id_producto)
        self.cargar_carrito_detallado()

    @rx.event
    def finalizar_compra(self):
        if self.user_id == 0:
            self.mensaje_compra = "Debes iniciar sesión para finalizar la compra."
            return
        vaciar_carrito(self.user_id)
        self.productos_carrito = []
        self.total = 0.0
        self.mensaje_compra = "✅ ¡Compra realizada con éxito!"