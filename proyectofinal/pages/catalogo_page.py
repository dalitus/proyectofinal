import reflex as rx
from proyectofinal.state.catalogo_state import CatalogoState
from proyectofinal.state.users_state import UsersState


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
        rx.button("Logearse", on_click=CatalogoState.ir_a_login),
        spacing="3",
        justify_content="flex-start",
        margin_bottom="20px"
    )

def producto_card(p: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.cond(
                p.get("imagen", "") != "",
                rx.image(
                    src=p["imagen"],
                    alt=p.get("nombre", ""),
                    width="150px",
                    height="150px",
                    border_radius="8px",
                    object_fit="cover",
                    style={
                        "transition": "transform 0.2s",
                        "_hover": {"transform": "scale(1.2)", "z_index": "10"}
                    }
                ),
                rx.image(
                    src="/static/default.jpg",
                    alt="Imagen no disponible",
                    width="150px",
                    height="150px",
                    border_radius="8px",
                    object_fit="cover"
                )
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
                rx.link(
                    rx.button("Ver Detalle", width="100%"),
                    href=f"/detalle_producto/{p['id_producto']}"
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

# -------------------
# PÁGINA PRINCIPAL
# -------------------

@rx.page(route="/catalogo", on_load=CatalogoState.cargar_productos)
def catalogo_page() -> rx.Component:
    return rx.hstack(
        rx.flex(
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
            style={"width": "75%", "padding": "20px"}
        ),
        rx.cond(
            UsersState.logeado,
            rx.card(
                rx.vstack(
                    rx.heading("👤 Perfil", size="4"),
                    rx.text(f"Nombre: {UsersState.perfil.get('nombre', '')}"),
                    rx.text(f"Email: {UsersState.perfil.get('email', '')}"),
                    rx.text(f"Teléfono: {UsersState.perfil.get('telefono', '')}"),
                    rx.button("Cerrar sesión", on_click=UsersState.logout)
                ),
                width="25%",
                padding="20px",
                box_shadow="md"
            ),
            rx.box(
                rx.text("No estás logeado"),
                width="25%",
                padding="20px"
            )
        )
    )