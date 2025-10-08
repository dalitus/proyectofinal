import reflex as rx
from proyectofinal.repository.carrito_repository import (
    get_items_por_usuario,
    agregar_item_al_carrito,
    eliminar_item_del_carrito,
    vaciar_carrito
)
from proyectofinal.state.shared_user import get_user_id
from collections import Counter
from sqlmodel import Session
from proyectofinal.repository.conect_db import engine

class CarritoState(rx.State):
    productos_carrito: list[dict] = []
    total: float = 0.0
    mensaje_compra: str = ""
    @rx.event
    async def cargar_carrito_agrupado(self):
        from proyectofinal.repository.carrito_repository import obtener_carrito_agrupado_por_usuario
        user_id = await get_user_id(self)
        with Session(engine) as db:
            self.productos_carrito = obtener_carrito_agrupado_por_usuario(db, user_id)
            self.total = sum(p["subtotal"] for p in self.productos_carrito)

    @rx.event
    def cargar_carrito_detallado(self):
        from proyectofinal.repository.carrito_repository import obtener_carrito_completo_por_usuario
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
    def cargar_carrito(self):
        self.productos_carrito = get_items_por_usuario(self.user_id)

    @rx.event
    async def vaciar_carrito_completo(self):
        user_id = await get_user_id(self)
        vaciar_carrito(user_id)
        self.productos_carrito = []
        self.total = 0.0
        self.mensaje_compra = "🧹 Carrito vaciado correctamente."

    @rx.event
    async def eliminar_producto(self, id_producto: int):
        user_id = await get_user_id(self)
        eliminar_item_del_carrito(user_id, id_producto)
        await self.cargar_carrito()

    @rx.event
    async def finalizar_compra(self):
        user_id = await get_user_id(self)
        vaciar_carrito(user_id)
        self.productos_carrito = []
        self.total = 0.0
        self.mensaje_compra = "✅ ¡Compra finalizada con éxito!"

    @rx.event
    async def agregar_carrito_con_id(self, id_producto: int):
        user_id = await get_user_id(self)
        print(f"🛒 Agregando producto {id_producto} al carrito del usuario {user_id}")
        agregar_item_al_carrito(user_id, id_producto)
        await self.cargar_carrito()

    @rx.var
    def productos_agrupados(self) -> list[dict]:
        contador = Counter(p["id_producto"] for p in self.productos_carrito)
        agrupados = []
        vistos = set()

        for producto in self.productos_carrito:
            pid = producto["id_producto"]
            if pid not in vistos:
                vistos.add(pid)
                agrupados.append({
                    "id_producto": pid,
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "imagen": producto["imagen"],
                    "cantidad": contador[pid],
                    "subtotal": producto["precio"] * contador[pid]
                })
        return agrupados