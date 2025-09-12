import reflex as rx
from proyectofinal.repository.carrito_repository import get_items_por_usuario
from proyectofinal.service.catalogo_service import producto_to_dict

class CarritoState(rx.State):
    productos_carrito: list[dict] = []
    user_id: int = 0

    @rx.event
    def set_user(self, user_id: int):
        self.user_id = user_id

    @rx.event
    def cargar_carrito(self):
        from proyectofinal.repository.carrito_repository import get_items_por_usuario
        self.productos_carrito = get_items_por_usuario(self.user_id)

    @rx.event
    def eliminar_producto(self, producto_id: int):
        from proyectofinal.repository.carrito_repository import eliminar_item_del_carrito, get_items_por_usuario
        eliminar_item_del_carrito(self.user_id, producto_id)
        self.productos_carrito = get_items_por_usuario(self.user_id)

    @rx.event
    def finalizar_compra(self):
        self.productos_carrito = []

    @rx.var
    def total(self) -> float:
        return sum(p.get("precio", 0) for p in self.productos_carrito)


@rx.page(route="/carrito", title="Mi Carrito", on_load=CarritoState.cargar_carrito)
def carrito_page() -> rx.Component:
    return rx.vstack(
        rx.heading(" Mi Carrito", size="6"),
        rx.cond(
            CarritoState.user_id is not None,
            rx.vstack(
                rx.flex(
                    rx.foreach(
                        CarritoState.productos_carrito,
                        lambda producto: rx.card(
                            rx.vstack(
                                rx.cond(
                                    producto["imagen"] != "",
                                    rx.image(src=producto["imagen"], width="100px", border_radius="8px"),
                                    rx.box()
                                ),
                                rx.text(producto["nombre"], font_size="lg", font_weight="bold"),
                                rx.text(f"Precio: ${producto['precio']}", font_size="md"),
                                rx.text(f"Stock: {producto['stock']}", font_size="sm"),
                                rx.button(
                                    "Eliminar",
                                    on_click=CarritoState.eliminar_producto(producto["id"]),
                                    color_scheme="red",
                                    size="2"
                                ),
                                spacing="3",
                                align="center"
                            ),
                            padding="12px",
                            width="220px",
                            text_align="center",
                            margin="10px"
                        )
                    ),
                    wrap="wrap",
                    justify="center"
                ),
                rx.text(f"Total: ${CarritoState.total:.2f}", font_size="xl", font_weight="bold", margin_top="20px"),
                rx.button("Finalizar Compra", on_click=CarritoState.finalizar_compra, margin_top="10px", color_scheme="green"),
                spacing="4",
                align_items="center"
            ),
            rx.text(" No hay usuario logueado", font_size="lg", color="red")
        ),
        spacing="6",
        align_items="center",
        padding="20px"
    )