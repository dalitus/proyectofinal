import reflex as rx
from proyectofinal.state.users_state import UsersState
from proyectofinal.service.notifail import notifail_component
from proyectofinal.model.users_model import Users

@rx.page(route="users", title="Users", on_load=UsersState.get_all_users)
def users_page() -> rx.Component:
    return rx.flex(
        rx.heading("Usuarios", align="center"),
        rx.hstack(
            buscar_user_component(),
            create_user_dialogo_component(),
            validar_usuario_button(),
            style={"textAlign": "center"},
        ),
        table_users(UsersState.users),
        rx.cond(
            UsersState.error_message != "",
            notifail_component(
                mensaje=UsersState.error_message,
                icon_notify="shield_alert",
                color="red"
            )
        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"},
    )

def table_users(list_user: list[Users]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Apellido"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Teléfono"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(list_user, row_table)
        )
    )

def row_table(user: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user["nombre"]),
        rx.table.cell(user["apellido"]),
        rx.table.cell(user["email"]),
        rx.table.cell(user["telefono"]),
        rx.table.cell(
            rx.hstack(
                delete_user_button(user["email"])
            )
        )
    )

def buscar_user_component() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Buscar por email",
            on_change=UsersState.buscar_on_change
        ),
        rx.button("Buscar usuario", on_click=UsersState.get_user_by_email)
    )

def create_user_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Apellido", name="apellido"),
            rx.input(placeholder="Email", name="email"),
            rx.input(placeholder="Teléfono", name="telefono"),
            rx.input(placeholder="Contraseña", name="contrasena", type="password"),
            rx.dialog.close(rx.button("Guardar", type="submit")),
        ),
        on_submit=UsersState.create_user,
    )

def create_user_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Usuario")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Usuario"),
                create_user_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                spacing="3",
                margin_top="16px",
                justify="center",
            ),
            style={"width": "400px"}
        ),
    )

def delete_user_button(email: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash-2"))),
        rx.dialog.content(
            rx.dialog.title("Confirmación"),
            rx.dialog.description(f"¿Estás seguro de que deseas eliminar el usuario con email: {email}?"),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=lambda: UsersState.delete_user(email))
                ),
                spacing="3",
                margin_top="16px",
                justify="center",
            ),
            style={"width": "350px"},
        )
    )

def validar_usuario_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Iniciar Sesión")),
        rx.dialog.content(
            rx.form(
                rx.vstack(
                    rx.dialog.title("Iniciar Sesión"),
                    rx.input(placeholder="Email", name="email"),
                    rx.input(placeholder="Contraseña", name="password", type="password"),
                    rx.dialog.close(rx.button("Iniciar Sesión", type="submit")),
                ),
                on_submit=UsersState.validar_usuario
            ),
            style={"width": "400px"}
        ),
    )

