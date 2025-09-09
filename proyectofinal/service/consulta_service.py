from proyectofinal.repository.consulta_repocitory import (
    crear_consulta_repo,
    listar_consultas_usuario_repo,  
    responder_consulta_repo,
)

from proyectofinal.repository.consulta_repocitory import (
    crear_consulta_repo,
    listar_consultas_usuario_repo,
    responder_consulta_repo,
)

from proyectofinal.repository.consulta_repocitory import listar_todas_consultas_repo

def crear_consulta(id_users: int, pregunta: str):
    if not id_users or not pregunta:
        raise ValueError("Todos los campos son obligatorios")
    return crear_consulta_repo(id_users, pregunta)

def listar_consultas_usuario(usuario_email: str):
    return listar_consultas_usuario_repo(usuario_email)

def responder_consulta(consulta_id: int, respuesta: str):
    consulta = responder_consulta_repo(consulta_id, respuesta)
    if not consulta:
        raise ValueError(f"No se encontró la consulta con ID {consulta_id}")
    return consulta