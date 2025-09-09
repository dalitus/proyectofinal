import reflex as rx
from proyectofinal.service.producto_servicio import obtener_productos

class DetalleProductoState(rx.State):
    producto: dict = {}

    def cargar_producto(self, producto_id: int):
        print("→ ID recibido:", producto_id)  # Debug opcional
        productos = obtener_productos()
        for p in productos:
            if p.id_producto == producto_id:
                self.producto = {
                    "id": p.id_producto,
                    "nombre": p.nombre,
                    "descripcion": p.descripcion,
                    "precio": p.precio,
                    "marca": p.marca,
                    "categoria": p.categoria,
                    "talle": p.talle,
                    "imagen": getattr(p, "imagen", ""),
                }
                print("→ Producto cargado:", self.producto)  # Debug opcional
                break
@rx.page(route="/detalle_producto")
def detalle_producto_page(producto_id: int = 0) -> rx.Component:
    # Ejecutar la carga del producto dentro del cuerpo
    DetalleProductoState.cargar_producto(producto_id)

    return rx.cond(
        DetalleProductoState.producto != {},
        rx.flex(
            rx.image(
                src=DetalleProductoState.producto.get("imagen", ""),
                alt=DetalleProductoState.producto.get("nombre", ""),
                width="300px",
                height="300px"
            ),
            rx.vstack(
                rx.heading(DetalleProductoState.producto.get("nombre", ""), size="5"),
                rx.text(f"Marca: {DetalleProductoState.producto.get('marca', '')}"),
                rx.text(f"Categoría: {DetalleProductoState.producto.get('categoria', '')}", font_size="md"),
                rx.text(f"Talle: {DetalleProductoState.producto.get('talle', '')}", font_size="md"),
                rx.text(f"Precio: ${DetalleProductoState.producto.get('precio', '')}", font_size="lg", font_weight="bold"),
                rx.text(DetalleProductoState.producto.get("descripcion", ""), font_size="md"),
                rx.button("Volver al Catálogo", on_click=lambda: rx.redirect("/catalogo")),
                spacing="4",
                margin_top="20px"
            ),
            direction="row",
            justify_content="center",
            align_items="flex-start",
            style={"gap": "40px", "marginTop": "50px"}
        ),
        rx.text("Cargando producto...")
    )