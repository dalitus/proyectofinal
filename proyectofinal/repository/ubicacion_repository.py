from proyectofinal.model.ubicacion_model import Ubicacion
from proyectofinal.repository.conect_db import get_session

# Obtener la ubicación actual

def get_ubicacion() -> Ubicacion:
    with get_session() as session:
        ubic = session.get(Ubicacion, 1)
        if ubic is None:
            ubic = Ubicacion(id_ubicacion=1, lat=-34.6037, lng=-58.3816)
            session.add(ubic)
            session.commit()
        return ubic

# Actualizar la ubicación

def set_ubicacion(lat: float, lng: float):
    with get_session() as session:
        ubic = session.get(Ubicacion, 1)
        if ubic is None:
            ubic = Ubicacion(id_ubicacion=1, lat=lat, lng=lng)
            session.add(ubic)
        else:
            ubic.lat = lat
            ubic.lng = lng
        session.commit()
        return ubic
