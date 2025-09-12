import reflex as rx
from proyectofinal.service.catalogo_service import obtener_catalogo, buscar_en_catalogo
from proyectofinal.service.carrito_service import agregar_al_carrito

class CatalogoState(rx.State):
    productos: list[dict] = []
    buscar_texto: str = ""
    error_message: str = ""
    success_message: str = ""
    user_id: int = 0

    @rx.event
    def cargar_productos(self):
        self.productos = obtener_catalogo()
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def actualizar_buscar_texto(self, value: str):
        self.buscar_texto = value

    @rx.event
    def buscar(self):
        resultados = buscar_en_catalogo(self.buscar_texto)
        if resultados:
            self.productos = resultados
            self.error_message = ""
        else:
            self.productos = []
            self.error_message = "No se encontraron productos."

    @rx.event
    def agregar_carrito_con_id(self, producto_id: int):
        if not self.user_id:
            self.error_message = "Debes iniciar sesión para agregar al carrito."
            self.success_message = ""
            return
        agregar_al_carrito(self.user_id, producto_id)
        self.success_message = "Producto agregado al carrito ✅"
        self.error_message = ""

    @rx.event
    def set_user(self, user_id: int):
        self.user_id = user_id

    @rx.event
    def ir_a_carrito(self):
        return rx.redirect("/carrito")

    @rx.event
    def ir_a_ubicacion(self):
        return rx.redirect("/ubicacion")

    @rx.event
    def ir_a_consulta(self):
        return rx.redirect("/consulta_usuario")
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
        rx.button("Ver Carrito", on_click=CatalogoState.ir_a_carrito),
        rx.button("Ubicarme", on_click=CatalogoState.ir_a_ubicacion),
        rx.button("Hacer Consulta", on_click=CatalogoState.ir_a_consulta),
        spacing="3",
        justify_content="flex-start",
        margin_bottom="20px"
    )

def producto_card(p: dict) -> rx.Component:
    return rx.box(
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
            rx.vstack(
                rx.button(
                    "Agregar al Carrito",
                    on_click=CatalogoState.agregar_carrito_con_id(p["id_producto"]),
                    width="100%"
                ),
                rx.button(
                    "Ver Detalle",
                    on_click=rx.redirect(f"/detalle_producto?producto_id={p['id_producto']}"),
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

def mostrar_productos() -> rx.Component:
    return rx.hstack(
        rx.foreach(
            CatalogoState.productos.to(list[dict]),
            producto_card
        ),
        flex_wrap="wrap",
        justify_content="center"
    )

@rx.page(route="/catalogo", on_load=CatalogoState.cargar_productos)
def catalogo_page() -> rx.Component:
    return rx.flex(
        rx.heading("Catálogo de Productos", align="center"),
        buscar_y_botones_component(),
        rx.cond(
            CatalogoState.error_message != "",
            rx.text(CatalogoState.error_message, color="red", margin_bottom="10px"),
            rx.box()
        ),
        rx.cond(
            CatalogoState.success_message != "",
            rx.text(CatalogoState.success_message, color="green", margin_bottom="10px"),
            rx.box()
        ),
        mostrar_productos(),
        direction="column",
        style={"width": "80vw", "margin": "auto"}
    )