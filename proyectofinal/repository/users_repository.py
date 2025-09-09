from proyectofinal.model.users_model import Users
from proyectofinal.repository.conect_db import get_session
from sqlmodel import select
from sqlalchemy import and_

# Obtener todos los usuarios
def select_all():
    with get_session() as session:
        query = select(Users)
        return session.exec(query).all()

# Buscar por email
def select_by_email(email: str):
    with get_session() as session:
        query = select(Users).where(Users.email == email)
        return session.exec(query).all()

# Crear nuevo usuario
def create_user(user: Users):
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# Eliminar por email
def delete_user_by_email(email: str):
    with get_session() as session:
        query = select(Users).where(Users.email == email)
        user = session.exec(query).one()
        session.delete(user)
        session.commit()

# Validar login
def validar_usuario(email: str, contrasena: str):
    with get_session() as session:
        query = select(Users).where(and_(Users.email == email, Users.contrasena == contrasena))
        return session.exec(query).one_or_none()
