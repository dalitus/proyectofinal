from proyectofinal.repository.conect_db import get_session
from proyectofinal.model.gerente_model import Gerente

def select_gerente_by_email_y_contra(email: str, contrasenia: str):
    with get_session() as session:
        gerente = session.query(Gerente).filter(
            Gerente.email == email,
            Gerente.contrasenia == contrasenia
        ).first()
        return gerente
