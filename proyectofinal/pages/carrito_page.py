import reflex as rx
from proyectofinal.state.carrito_state import  CarritoState
from proyectofinal.state.app_state import AppState

@rx.page(route="/carrito", on_load=CarritoState.cargar_carrito_agrupado)
def carrito_page() -> rx.Component:
    return rx.vstack(
        rx.heading("🛒 Tu carrito", size="6"),
        rx.text(
            CarritoState.mensaje_compra,
            color=rx.cond(
                CarritoState.mensaje_compra.contains("✅"),
                "green",
                "red"
            ),
            font_weight="bold"
        ),
        rx.divider(),

        rx.cond(
            CarritoState.productos_carrito,
            rx.vstack(
                rx.hstack(
                    rx.text("🧾 Producto", font_weight="bold", width="25%"),
                    rx.text("Cantidad", font_weight="bold", width="10%"),
                    rx.text("Precio", font_weight="bold", width="15%"),
                    rx.text("Subtotal", font_weight="bold", width="15%"),
                    rx.text("Acción", font_weight="bold", width="15%"),
                    spacing="4"
                ),
                rx.foreach(
                    CarritoState.productos_carrito,
                    lambda p: rx.hstack(
                        rx.text(p["nombre"], width="25%"),
                        rx.text(str(p["cantidad"]), width="10%"),
                        rx.text(f"${p['precio']:.2f}", width="15%"),
                        rx.text(f"${p['subtotal']:.2f}", width="15%"),
                        rx.button(
                            "Eliminar",
                            color_scheme="red",
                            size="3",
                            on_click=lambda: CarritoState.eliminar_producto(p["id_producto"]),
                            width="15%"
                        ),
                        spacing="4"
                    )
                ),
                spacing="2"
            ),
            rx.text("🧺 El carrito está vacío.")
        ),

        rx.divider(),
        rx.text(f"💰 Total: ${CarritoState.total:.2f}", font_size="lg", font_weight="bold"),
        rx.hstack(
            rx.button("Finalizar compra", on_click=CarritoState.finalizar_compra, color_scheme="green"),
            rx.button("Vaciar carrito", on_click=CarritoState.vaciar_carrito_completo, color_scheme="gray"),
        ),
        rx.button("← Volver al catálogo", on_click=rx.redirect("/catalogo")),
        padding="6",
        spacing="4"
    )