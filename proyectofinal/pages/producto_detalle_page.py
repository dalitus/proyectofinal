import reflex as rx
from proyectofinal.service.producto_servicio import obtener_productos
from proyectofinal.repository.producto_repocitory import get_producto_by_id

class DetalleProductoState(rx.State):
    producto: dict = {}

    def cargar_producto(self, producto_id: int):
        productos = obtener_productos()
        for p in productos:
            if p.id_producto == producto_id:
                self.producto = p.__dict__
                break
@rx.page(route="/detalle_producto")
def detalle_producto_page(producto_id: int = 0) -> rx.Component:
    """
    Muestra los detalles de un producto.
    Recibe opcionalmente producto_id por query param.
    """
    # Intentar obtener el producto
    producto = None
    if producto_id:
        producto = get_producto_by_id(producto_id)

    # Si no se encontró producto
    if not producto:
        return rx.box(
            rx.text("Producto no encontrado.", font_size="xl", font_weight="bold"),
            style={"textAlign": "center", "marginTop": "50px"}
        )

    # Mostrar detalles del producto
    return rx.flex(
        rx.image(src=producto.imagen, alt=producto.nombre, width="300px", height="300px"),
        rx.vstack(
            rx.heading(producto.nombre, size="2xl"),
            rx.text(f"Marca: {producto.marca}", font_size="md"),
            rx.text(f"Categoría: {producto.categoria}", font_size="md"),
            rx.text(f"Talle: {producto.talle}", font_size="md"),
            rx.text(f"Precio: ${producto.precio}", font_size="lg", font_weight="bold"),
            rx.text(producto.descripcion, font_size="md"),
            rx.button("Volver al Catálogo", on_click=lambda: rx.redirect("/catalogo")),
            spacing="4",
            margin_top="20px"
        ),
        direction="row",
        justify_content="center",
        align_items="flex-start",
        style={"gap": "40px", "marginTop": "50px"}
    )

