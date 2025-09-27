from sqlmodel import Session
from proyectofinal.repository.conect_db import engine
from proyectofinal.model.ubicacion_model import UbicacionLocal

def guardar_ubicacion(lat: float, lng: float):
    with Session(engine) as session:
        ubicacion = session.get(UbicacionLocal, 1)
        if not ubicacion:
            ubicacion = UbicacionLocal(id=1, lat=lat, lng=lng)
        else:
            ubicacion.lat = lat
            ubicacion.lng = lng
        session.add(ubicacion)
        session.commit()

def obtener_ubicacion() -> UbicacionLocal:
    with Session(engine) as session:
        return session.get(UbicacionLocal, 1)