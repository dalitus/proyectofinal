import reflex as rx
from proyectofinal.service.carrito_service import (
    cargar_carrito_service,
    eliminar_producto_service,
    finalizar_compra_service
)

class CarritoState(rx.State):
    productos_carrito: list[dict] = []
    user_id: int = 0

    @rx.event
    def set_user(self, value: str):
        self.user_id = int(value) if value.isdigit() else 0
        self.cargar_carrito()

    @rx.event
    def cargar_carrito(self):
        self.productos_carrito = cargar_carrito_service(self.user_id)

    @rx.event
    def eliminar_producto(self, producto_id: int):
        eliminar_producto_service(self.user_id, producto_id)
        self.productos_carrito = cargar_carrito_service(self.user_id)

    @rx.event
    def finalizar_compra(self):
        finalizar_compra_service(self.user_id)
        self.productos_carrito = []

    @rx.var
    def total(self) -> float:
        return sum(p.get("precio", 0) for p in self.productos_carrito)

def producto_card(p: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.image(
                src=p.get("imagen", "/static/default.jpg"),
                alt=p.get("nombre", ""),
                width="150px",
                height="150px",
                border_radius="8px",
                object_fit="cover"
            ),
            rx.text(p.get("nombre", ""), font_size="lg", font_weight="bold"),
            rx.text(f"Precio: ${p.get('precio', '')}", font_size="md"),
            rx.button(
                "Eliminar",
                on_click=lambda: CarritoState.eliminar_producto(p["id_producto"]),
                color_scheme="red"
            )
        ),
        padding="10px",
        width="220px",
        margin="10px"
    )

@rx.page(route="/carrito", title="Carrito")
def carrito_page() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.script("""
                window.addEventListener('load', () => {
                    const id = localStorage.getItem('user_id');
                    if (id) {
                        fetch('/_api/set_user', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ value: id })
                        });
                    }
                });
            """),
            rx.heading("Tu Carrito", size="6"),
            rx.cond(
                CarritoState.productos_carrito.length() == 0,
                rx.text("No hay productos en tu carrito."),
                rx.flex(
                    rx.foreach(CarritoState.productos_carrito, producto_card),
                    wrap="wrap",
                    justify="center"
                )
            ),
            rx.text(f"Total: ${CarritoState.total}", font_size="xl", margin_top="20px"),
            rx.button(
                "Finalizar Compra",
                on_click=CarritoState.finalizar_compra,
                color_scheme="green",
                margin_top="10px"
            ),
            spacing="4",
            align_items="center",
            padding="20px"
        )
    )