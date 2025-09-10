import reflex as rx
from proyectofinal.service.producto_servicio import obtener_productos

class DetalleProductoState(rx.State):
    producto: dict = {}
    producto_id: int = 0

    def cargar_producto(self):
        productos = obtener_productos()
        for p in productos:
            if p.id_producto == self.producto_id:
                self.producto = {
                    "id": p.id_producto,
                    "nombre": p.nombre,
                    "descripcion": p.descripcion,
                    "precio": float(p.precio),  # Convertir Decimal a float
                    "marca": p.marca,
                    "categoria": p.categoria,
                    "talle": p.talle,
                    "imagen": p.imagen or "",
                }
                break

@rx.page(route="/detalle_producto", on_load=DetalleProductoState.cargar_producto)
def detalle_producto_page(producto_id: int = 0) -> rx.Component:
    DetalleProductoState.producto_id = producto_id

    return rx.cond(
        DetalleProductoState.producto != {},
        rx.center(
            rx.card(
                rx.hstack(
                    rx.image(
                        src=DetalleProductoState.producto.get("imagen", ""),
                        alt=DetalleProductoState.producto.get("nombre", ""),
                        width="300px",
                        height="300px",
                        border_radius="8px",
                        box_shadow="lg"
                    ),
                    rx.vstack(
                        rx.heading(DetalleProductoState.producto.get("nombre", ""), size="6"),
                        rx.text(f"Marca: {DetalleProductoState.producto.get('marca', '—')}"),
                        rx.text(f"Categoría: {DetalleProductoState.producto.get('categoria', '—')}"),
                        rx.text(f"Talle: {DetalleProductoState.producto.get('talle', '—')}"),
                        rx.text(f"Precio: ${DetalleProductoState.producto.get('precio', 0):.2f}", font_size="lg", font_weight="bold"),
                        rx.text("Descripción:", font_weight="medium", margin_top="10px"),
                        rx.text(DetalleProductoState.producto.get("descripcion", ""), font_size="md", white_space="pre-wrap"),
                        rx.button("← Volver al Catálogo", on_click=lambda: rx.redirect("/catalogo"), margin_top="20px")
                    ),
                    spacing="6"
                ),
                padding="30px",
                border_radius="12px",
                box_shadow="xl",
                max_width="900px",
                width="100%"
            )
        ),
        rx.center(
            rx.card(
                rx.heading("Producto no encontrado", size="5"),
                rx.text("No se pudo cargar el producto. Verificá el ID o volvé al catálogo."),
                rx.button("Volver al Catálogo", on_click=lambda: rx.redirect("/catalogo"), margin_top="20px"),
                padding="30px",
                box_shadow="md"
            )
        )
    )