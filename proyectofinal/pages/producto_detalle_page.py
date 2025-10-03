import reflex as rx
from proyectofinal.service.detalle_service import obtener_detalle_producto
from proyectofinal.state.catalogo_state import CatalogoState

class DetalleProductoState(rx.State):
    producto: dict = {}
    producto_no_encontrado: bool = False
    producto_id_actual: int = 0  # ← para evitar múltiples llamadas

    @rx.event
    def cargar_producto_con_id(self, producto_id: int):
        # Evita recargar si ya se cargó el mismo producto
        if self.producto_id_actual == producto_id and self.producto.get("id_producto", 0) > 0:
            return
        self.producto_id_actual = producto_id

        resultado = obtener_detalle_producto(producto_id)
        if resultado and resultado.get("id_producto", 0) > 0:
            self.producto = resultado
            self.producto_no_encontrado = False
        else:
            self.producto = {}
            self.producto_no_encontrado = True

    @rx.event
    def volver_al_catalogo(self):
        return rx.redirect("/catalogo")

@rx.page(route="/detalle_producto/[producto_id]")
def detalle_producto_page(producto_id: int = 0) -> rx.Component:
    return rx.center(
        rx.fragment(
            rx.script(f"window.dispatchEvent(new CustomEvent('rx_event', {{ detail: {{ name: 'DetalleProductoState.cargar_producto_con_id', args: {{ producto_id: {producto_id} }} }} }}));"),
            rx.cond(
                DetalleProductoState.producto_no_encontrado,
                rx.text("❌ Producto no disponible"),
                rx.cond(
                    DetalleProductoState.producto.get("id_producto", 0) == 0,
                    rx.spinner(color="blue", thickness="4px", size="3"),
                    rx.card(
                        rx.vstack(
                            rx.image(
                                src=DetalleProductoState.producto.get("imagen", "/static/default.jpg"),
                                alt=DetalleProductoState.producto.get("nombre", ""),
                                width="300px",
                                height="300px",
                                border_radius="10px",
                                object_fit="cover"
                            ),
                            rx.heading(DetalleProductoState.producto.get("nombre", ""), size="5"),
                            rx.text(f"Marca: {DetalleProductoState.producto.get('marca', '')}", font_size="md"),
                            rx.text(f"Precio: ${DetalleProductoState.producto.get('precio', 0):.2f}", font_size="lg"),
                            rx.text(f"Categoría: {DetalleProductoState.producto.get('categoria', '')}", font_size="md"),
                            rx.text(f"Talle: {DetalleProductoState.producto.get('talle', '')}", font_size="md"),
                            rx.text(DetalleProductoState.producto.get("descripcion", ""), font_size="sm"),
                            rx.button(
                                "🛒 Agregar al Carrito",
                                on_click=CatalogoState.agregar_carrito_con_id(
                                    DetalleProductoState.producto.get("id_producto", 0)
                                )
                            ),
                            rx.button("← Volver al Catálogo", on_click=DetalleProductoState.volver_al_catalogo)
                        ),
                        padding="30px",
                        box_shadow="xl",
                        width="500px",
                        spacing="4"
                    )
                )
            )
        )
    )