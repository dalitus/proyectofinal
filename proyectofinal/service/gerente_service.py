from proyectofinal.model.gerente_model import Gerente
from proyectofinal.repository.conect_db import get_session

def validar_admin_service(email: str, contrasenia: str) -> Gerente | None:
    with get_session() as db:
        return db.query(Gerente).filter(
            Gerente.email == email,
            Gerente.contrasenia == contrasenia
        ).first()
