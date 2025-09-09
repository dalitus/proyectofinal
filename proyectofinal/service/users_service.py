from ..repository.users_repository import select_all, select_by_email, create_user, delete_user_by_email, validar_usuario
from ..model.users_model import Users


_usuario_logueado: Users | None = None


def select_all_users_service():
    users = select_all()
    print(users)
    return users


def select_by_email_service(email: str):
    if len(email) != 0:
        return select_by_email(email)
    else:
        return select_all()


def create_user_service(nombre: str, apellido: str, contrasena: str, email: str, telefono: str):
    user = select_by_email(email)
    if len(user) == 0:
        user_save = Users(
            nombre=nombre,
            apellido=apellido,
            contrasena=contrasena,
            email=email,
            telefono=telefono
        )
        return create_user(user_save)
    else:
        raise ValueError("El usuario ya existe")


def delete_user_service(email: str):
    return delete_user_by_email(email)


def validar_usuario_service(email: str, password: str):
    """Valida usuario y lo guarda en sesión"""
    global _usuario_logueado
    user = validar_usuario(email, password)
    if user:
        _usuario_logueado = user
        return user
    else:
        raise ValueError("Email o contraseña incorrectos")


def get_usuario_logueado() -> Users | None:
    """Devuelve el usuario logueado (o None si no hay sesión activa)"""
    return _usuario_logueado


def cerrar_sesion_service():
    """Cierra la sesión del usuario actual"""
    global _usuario_logueado
    _usuario_logueado = None
