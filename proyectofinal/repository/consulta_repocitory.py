from sqlmodel import Session, select
from proyectofinal.model.consulta_model import Consulta
from proyectofinal.repository.conect_db import engine

# Crear consulta
def crear_consulta_repo(id_users: int, pregunta: str):
    consulta = Consulta(id_users=id_users, pregunta=pregunta, respuesta=None)
    with Session(engine) as session:
        session.add(consulta)
        session.commit()
        session.refresh(consulta)
    return consulta

# Listar consultas por usuario
def listar_consultas_usuario_repo(id_users: int):
    with Session(engine) as session:
        statement = select(Consulta).where(Consulta.id_users == id_users)
        results = session.exec(statement)
        return results.all()

# Responder consulta
def responder_consulta_repo(consulta_id: int, respuesta: str):
    with Session(engine) as session:
        consulta = session.get(Consulta, consulta_id)
        if consulta:
            consulta.respuesta = respuesta
            session.add(consulta)
            session.commit()
            session.refresh(consulta)
            return consulta
    return None

# Alias para el servicio
def listar_consultas_usuario(id_users: int):
    return listar_consultas_usuario_repo(id_users)


def listar_todas_consultas_repo():
    with Session(engine) as session:
        statement = select(Consulta)
        results = session.exec(statement)
        return results.all()