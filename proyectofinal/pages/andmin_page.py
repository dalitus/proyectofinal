import reflex as rx
from proyectofinal.service.gerente_service import validar_admin_service


class AdminLoginState(rx.State):
    error_message: str = ""

    def validar_admin(self, data: dict):
        try:
            admin = validar_admin_service(
                email=data["email"],
                contrasenia=data["contrasenia"]
            )
            print("Admin logueado:", admin.nombre)
            return rx.redirect("/admin_dashboard")
        except ValueError as e:
            self.error_message = str(e)

@rx.page(route="/admin_login", title="Login Admin")
def admin_login_page():
    return rx.center(
        rx.vstack(
            rx.heading("Login Admin"),
            rx.form(
                rx.vstack(
                    rx.input(placeholder="Email", name="email"),
                    rx.input(placeholder="Contraseña", name="contrasenia", type_="password"),
                    rx.button("Iniciar sesión", type_="submit"),
                    rx.text(AdminLoginState.error_message, color="red"),
                ),
                on_submit=AdminLoginState.validar_admin,
                reset_on_submit=True,
            ),
        ),
        height="100vh"
    )
