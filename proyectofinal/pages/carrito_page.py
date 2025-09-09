import reflex as rx
from proyectofinal.service.carrito_service import obtener_productos_carrito, eliminar_producto_carrito

from sqlmodel import SQLModel, Field
from typing import Optional

import reflex as rx
from typing import Optional

class CarritoState(rx.State):
    user_id: Optional[int] = None
    productos_carrito: list[dict] = []

    def cargar_carrito(self):
        if self.user_id:
            productos = obtener_productos_carrito(self.user_id)
            self.productos_carrito = [
                {
                    "id": p.id_producto,
                    "nombre": p.nombre,
                    "precio": p.precio,
                    "stock": p.stock,
                    "imagen": getattr(p, "imagen", ""),
                }
                for p in productos
            ]

    def eliminar_producto(self, producto_id: int):
        if self.user_id:
            eliminar_producto_carrito(self.user_id, producto_id)
            self.cargar_carrito()

    @rx.var
    def total(self) -> str:
        return f"${sum(p['precio'] for p in self.productos_carrito)}"

    def finalizar_compra(self):
        print("Comprar ahora!")

    # Total dinámico
    @rx.var
    def total(self) -> str:
        return f"${sum(p['precio'] for p in self.productos_carrito)}"

    # Finalizar compra
    def finalizar_compra(self):
        print("Comprar ahora!")  # aquí va tu lógica de compra

@rx.page(route="/carrito", title="Mi Carrito", on_load=CarritoState.cargar_carrito)
def carrito_page() -> rx.Component:
    return rx.vstack(
        rx.heading(" Mi Carrito"),
        rx.cond(
            CarritoState.user_id != None,
            rx.vstack(
                rx.flex(
                    rx.foreach(
                        CarritoState.productos_carrito,
                        lambda producto: rx.box(
                            rx.vstack(
                                rx.cond(
                                    producto["imagen"] != "",
                                    rx.image(src=producto["imagen"], width="100px"),
                                    rx.box()
                                ),
                                rx.text(producto["nombre"], font_size="lg", font_weight="bold"),
                                rx.text(f"Precio: ${producto['precio']}", font_size="md"),
                                rx.text(f"Stock: {producto['stock']}", font_size="sm"),
                                rx.button(
                                    "Eliminar",
                                    on_click=lambda _, pid=producto["id"]: CarritoState.eliminar_producto(pid),
                                    color_scheme="red"
                                ),
                                spacing="3",
                                align="center"
                            ),
                            padding="10px",
                            border="1px solid #ccc",
                            border_radius="8px",
                            width="200px",
                            text_align="center",
                            margin="10px"
                        )
                    ),
                    wrap="wrap",
                    justify="center"
                ),
                rx.text(CarritoState.total, font_size="xl", font_weight="bold", margin_top="20px"),
                rx.button("Finalizar Compra", on_click=CarritoState.finalizar_compra, margin_top="10px"),
                spacing="4",
                align_items="center"
            ),
            rx.text("No hay usuario logueado", font_size="lg", color="red")
        ),
        spacing="6",
        align_items="center",
        padding="20px"
    )