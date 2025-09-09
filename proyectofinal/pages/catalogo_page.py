import reflex as rx
from proyectofinal.repository.producto_repocitory import get_all_productos
from proyectofinal.service.carrito_service import agregar_al_carrito

# -------------------
# STATE DEL CATALOGO
# -------------------
class CatalogoState(rx.State):
    productos: list[dict] = []
    buscar_texto: str = ""
    error_message: str = ""
    user_id: int = 0

    def set_user(self, user_id: int):
        self.user_id = user_id

    def agregar_carrito(self, producto_id: int):
        if not self.user_id:
            print("No hay usuario logueado")
            return
        agregar_al_carrito(self.user_id, producto_id)

    def cargar_productos(self):
        self.productos = [p.__dict__ for p in get_all_productos()]
        self.error_message = ""

    def actualizar_buscar_texto(self, value: str):
        self.buscar_texto = value

    def buscar(self):
        resultados = [
            p for p in get_all_productos()
            if self.buscar_texto.lower() in p.nombre.lower()
            or self.buscar_texto.lower() in p.marca.lower()
            or self.buscar_texto.lower() in str(p.precio)
        ]
        if resultados:
            self.productos = [p.__dict__ for p in resultados]
            self.error_message = ""
        else:
            self.productos = []
            self.error_message = "No se encontraron productos."

# -------------------
# COMPONENTES
# -------------------
def buscar_y_botones_component() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Buscar por nombre, marca o precio",
            on_change=CatalogoState.actualizar_buscar_texto,
            width="300px"
        ),
        rx.button("Buscar", on_click=CatalogoState.buscar),
        rx.button("Ver Carrito", on_click=lambda: rx.redirect("/carrito")),
        rx.button("Ubicarme", on_click=lambda: rx.redirect("/ubicacion")),
        rx.button("Hacer Consulta", on_click=lambda: rx.redirect("/consulta_usuario")),  # 🔹 Nuevo botón
        spacing="3",
        justify_content="flex-start",
        margin_bottom="20px"
    )

def mostrar_productos() -> rx.Component:
    return rx.hstack(
        rx.foreach(
            CatalogoState.productos.to(list[dict]),
            lambda p: rx.box(
                rx.vstack(
                    rx.image(
                        src=p.get("imagen", ""),
                        alt=p.get("nombre", ""),
                        width="150px",
                        height="150px"
                    ),
                    rx.text(p.get("nombre", ""), font_size="lg", font_weight="bold"),
                    rx.text(f"Precio: ${p.get('precio', '')}", font_size="md"),
                    rx.text(f"Marca: {p.get('marca', '')}", font_size="sm"),
                    # --- Botones uno debajo del otro ---
                    rx.vstack(
                        rx.button(
                            "Agregar al Carrito",
                            on_click=lambda p_id=p["id_producto"]: CatalogoState.agregar_carrito(p_id),
                            width="100%"
                        ),
                        rx.button(
                            "Ver Detalle",
                            on_click=lambda p_id=p["id_producto"]: rx.redirect(f"/detalle_producto?producto_id={p_id}"),
                            width="100%"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    spacing="2",
                    align_items="center"
                ),
                border="1px solid #ccc",
                border_radius="10px",
                padding="15px",
                margin="10px",
                width="220px",
                text_align="center",
                box_shadow="0px 2px 5px rgba(0,0,0,0.1)"
            )
        ),
        flex_wrap="wrap",
        justify_content="center"
    )

# -------------------
# PAGE
# -------------------
@rx.page(route="/catalogo", on_load=CatalogoState.cargar_productos)
def catalogo_page() -> rx.Component:
    return rx.flex(
        rx.heading("Catálogo de Productos", align="center"),
        buscar_y_botones_component(),
        mostrar_productos(),
        direction="column",
        style={"width": "80vw", "margin": "auto"}
    )



