import reflex as rx
from proyectofinal.model.users_model import Users
from proyectofinal.service.users_service import (
    select_all_users_service,
    select_by_email_service,
    select_by_id_service,
    create_user_service,
    delete_user_service,
    validar_usuario_service
)

from proyectofinal.service.gerente_service import validar_admin_service
from proyectofinal.service.notifail import notifail_component
from proyectofinal.state.catalogo_state import CatalogoState

class UsersState(rx.State):
    users: list[Users] = []
    user_buscar: str = ""
    error_message: str = ""
    user_id: int | None = None
    perfil: dict = {}
    logeado: bool = False

    @rx.event
    def login(self, usuario_id: int):
        self.user_id = usuario_id
        self.perfil = select_by_id_service(usuario_id)
        self.logeado = True
        CatalogoState.user_id = usuario_id
        CatalogoState.cargar_productos()

    @rx.event
    def logout(self):
        self.user_id = None
        self.perfil = {}
        self.logeado = False
        return rx.redirect("/users")

    @rx.event
    def validar_usuario(self, data: dict):
        email = data["email"]
        password = data["password"]

        admin = validar_admin_service(email=email, contrasenia=password)
        if admin:
            self.user_id = admin.id_gerente
            return rx.redirect("/admin_dashboard")

        user = validar_usuario_service(email=email, password=password)
        if user:
            self.login(user.id_users)
            return rx.redirect("/catalogo")

        self.error_message = "Credenciales inválidas. Intenta nuevamente."
        return notifail_component("Error", self.error_message)

    @rx.event
    def buscar_on_change(self, value: str):
        self.user_buscar = value

    @rx.event
    def get_user_by_email(self):
        self.users = select_by_email_service(self.user_buscar)

    @rx.event
    def get_all_users(self):
        self.users = select_all_users_service()

    @rx.event
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
            traceback.print_exc()
            self.error_message = f"Error al crear usuario: {e}"

    @rx.event
    def delete_user(self, email: str):
        delete_user_service(email)
        self.users = select_all_users_service()


