import reflex as rx
from proyectofinal.repository.producto_repocitory import get_all_productos

class DetalleProductoState(rx.State):
    producto: dict = {}

    @rx.event
    def cargar_producto_con_id(self, producto_id: int):
        print("→ ID recibido:", producto_id)
        productos = get_all_productos()
        for p in productos:
            if p.id_producto == producto_id:
                self.producto = {
                    "id": p.id_producto,
                    "nombre": p.nombre,
                    "descripcion": p.descripcion,
                    "precio": float(p.precio),
                    "marca": p.marca,
                    "categoria": p.categoria,
                    "talle": p.talle,
                    "imagen": p.imagen or "",
                }
                print("→ Producto encontrado:", self.producto)
                break

            
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
                rx.button("← Volver al Catálogo", on_click=rx.redirect("/catalogo"))
            ),
            padding="30px",
            box_shadow="xl",
            width="500px"
        )
    )