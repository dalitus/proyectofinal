import reflex as rx
from proyectofinal.repository.producto_repocitory import get_producto_by_id

class DetalleProductoState(rx.State):
    producto: dict = {}

    @rx.event
    def cargar_producto_con_id(self, producto_id: int):
        producto = get_producto_by_id(producto_id)
        if producto is None:
            self.producto = {}
            return
        self.producto = {
            "id": producto.id_producto,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": float(producto.precio),
            "marca": producto.marca,
            "categoria": producto.categoria,
            "talle": producto.talle,
            "imagen": producto.imagen or "",
        }

    @rx.event
    def volver_al_catalogo(self):
        return rx.redirect("/catalogo")
    
@rx.page(route="/detalle_producto")
def detalle_producto_page(producto_id: int = 0) -> rx.Component:
    DetalleProductoState.cargar_producto_con_id(producto_id)

    return rx.center(
        rx.card(
            rx.vstack(
                rx.image(
                    src=DetalleProductoState.producto.get("imagen", ""),
                    alt=DetalleProductoState.producto.get("nombre", ""),
                    width="300px",
                    height="300px"
                ),
                rx.heading(DetalleProductoState.producto.get("nombre", ""), size="5"),
                rx.text(f"Precio: ${DetalleProductoState.producto.get('precio', 0):.2f}", font_size="lg"),
                rx.text(f"Marca: {DetalleProductoState.producto.get('marca', '')}", font_size="md"),
                rx.text(f"Talle: {DetalleProductoState.producto.get('talle', '')}", font_size="md"),
                rx.text(f"Categoría: {DetalleProductoState.producto.get('categoria', '')}", font_size="md"),
                rx.text(DetalleProductoState.producto.get("descripcion", ""), font_size="sm"),
                rx.button("← Volver al Catálogo", on_click=DetalleProductoState.volver_al_catalogo)
            ),
            padding="30px",
            box_shadow="xl",
            width="500px"
        )
    )