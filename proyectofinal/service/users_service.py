from ..repository.users_repository import select_all, select_by_email, create_user, delete_user_by_email, validar_usuario
from ..model.users_model import Users

from proyectofinal.repository.users_repository import get_user_by_id

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


def create_user_service(nombre: str, apellido: str, contrasena: str, email: str, telefono: str, es_admin: bool = False):
    user = select_by_email(email)
    if len(user) == 0:
        user_save = Users(
            nombre=nombre,
            apellido=apellido,
            contrasena=contrasena,
            email=email,
            telefono=telefono,
            es_admin=es_admin,
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


def crear_admin_inicial(nombre: str, apellido: str, contrasena: str, email: str, telefono: str):
    existente = select_by_email(email)
    if len(existente) == 0:
        return create_user_service(nombre, apellido, contrasena, email, telefono, es_admin=True)
    # Si ya existe, asegura flag admin
    user = existente[0]
    if not user.es_admin:
        user.es_admin = True
        from proyectofinal.repository.conect_db import get_session
        with get_session() as s:
            s.add(user)
            s.commit()
            s.refresh(user)
    return user

def select_by_id_service(user_id: int) -> dict:
    user: Users | None = get_user_by_id(user_id)
    if user:
        return {
            "id_users": user.id_users,  # ← corregido
            "nombre": user.nombre,
            "apellido": user.apellido,
            "email": user.email,
            "telefono": user.telefono
        }
    return {}