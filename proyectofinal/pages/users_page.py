import reflex as rx

from proyectofinal.model.users_model import Users
from ..service.users_service import select_all_users_service, select_by_email_service, create_user_service, delete_user_service, validar_usuario_service 
from ..service.notifail import notifail_component
import asyncio

from proyectofinal.service.gerente_service import validar_admin_service
from proyectofinal.pages.carrito_page import CarritoState
from proyectofinal.pages.catalogo_page import CatalogoState

import asyncio

class UsersState(rx.State):
    users: list[Users] = []
    user_buscar: str = ""
    error_message: str = ""
    user_id: int | None = None

    CarritoState.user_id = user_id  # donde 'usuario.id' viene de la base de datos
    CarritoState.cargar_carrito()

    def login(self, usuario_id: int):
        # Setear el id del usuario logueado
        self.user_id = usuario_id

        # Actualizar el carrito
        CarritoState.user_id = usuario_id
        CarritoState.cargar_carrito()

    def get_all_users(self):
        self.users = select_all_users_service()

    def get_user_by_email(self):
        self.users = select_by_email_service(self.user_buscar)

    async def clear_error_message(self):
        # Espera 2 segundos y limpia el mensaje de error
        await asyncio.sleep(2)
        self.error_message = ""

    def create_user(self, data: dict):
        try:
            create_user_service(
                nombre=data["nombre"],
                apellido=data["apellido"],
                contrasena=data["contrasena"],
                email=data["email"],
                telefono=data["telefono"]
            )
            self.users = select_all_users_service()
            self.error_message = ""
        except ValueError as e:
            self.error_message = str(e)
        except Exception as e:
            import traceback
            traceback.print_exc()  # ⬅ imprime la traza completa en consola
            self.error_message = f"Error al crear usuario: {e}"

    def buscar_on_change(self, value: str):
        self.user_buscar = value

    
    def delete_user(self, email: str):
        delete_user_service(email)
        self.users = select_all_users_service()

    error_message: str = ""

    def validar_usuario(self, data: dict):
        email = data["email"]
        password = data["password"]

        # 1. Intentar validar como administrador
        admin = validar_admin_service(email=email, contrasenia=password)
        if admin:
            self.user_id = admin.id_gerente
            return rx.redirect("/admin_dashboard")

        # 2. Intentar validar como usuario normal
        user = validar_usuario_service(email=email, password=password)
        if user:
            # Guardamos el user_id en todos los estados que lo necesiten
            self.user_id = user.id_users
            CatalogoState.user_id = user.id_users
            CarritoState.user_id = user.id_users
            return rx.redirect("/catalogo")

        # 3. Si no coincide, mostramos error
        self.error_message = "Credenciales inválidas. Intenta nuevamente."
        return notifail_component("Error", self.error_message)

    


@rx.page(route='users', title='Users', on_load=UsersState.get_all_users)
def users_page() -> rx.Component:
    return rx.flex(
        rx.heading("usuarios", align="center"),
        rx.hstack(
            buscar_user_component(),
            crate_user_dialogo_component(),
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
                rx.table.column_header_cell("nombre"),
                rx.table.column_header_cell("apellido"),
                rx.table.column_header_cell("email"),
                rx.table.column_header_cell("telefono"),
                rx.table.column_header_cell("acciones"),
            )
        ),
        # Aquí usamos rx.table.body en lugar de rx.tbody
        rx.table.body(
            rx.foreach(list_user, row_table)
        )
    )

def row_table(user: dict) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user["nombre"]),
        rx.table.cell(user["apellido"]),
        rx.table.cell(user["email"]),
        rx.table.cell((user["telefono"])),
        rx.table.cell(rx.hstack(
            rx.button("Eliminar", on_click=lambda: UsersState.delete_user(user["email"]))
        ))
    )

def buscar_user_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Buscar por email", on_change=UsersState.buscar_on_change),
        rx.button("buscar usuario", on_click=UsersState.get_user_by_email)
    )


def create_user_from() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="nombre", name="nombre"),
            rx.input(placeholder="apellido", name="apellido"),
            rx.input(placeholder="email", name="email"),
            rx.input(placeholder="telefono", name="telefono"),
            rx.input(placeholder="contraseña", name="contrasena", type="password"),
            rx.dialog.close(rx.button("guardar", type="submit")),
        ),
        on_submit=UsersState.create_user,
    )




def crate_user_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Usuario")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Usuario"),
                create_user_from(),
                justify="center",
                align="center", 
                direction="column",  
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("cancelar", variant="soft", color_scheme="gray")
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

