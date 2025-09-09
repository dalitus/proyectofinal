from sqlmodel import select
from proyectofinal.model.product_model import Producto
from proyectofinal.repository.conect_db import get_session

# Obtener producto por ID
def get_producto_by_id(producto_id: int) -> Producto | None:
    with get_session() as session:
        return session.get(Producto, producto_id)

# Obtener todos los productos
def get_all_productos() -> list[Producto]:
    with get_session() as session:
        return session.exec(select(Producto)).all()

# Crear producto
def create_producto(producto: Producto) -> Producto:
    with get_session() as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)  # para obtener ID generado
        return producto

# Actualizar producto
def update_producto(producto_id: int, data: dict) -> Producto | None:
    with get_session() as session:
        db_producto = session.get(Producto, producto_id)
        if db_producto:
            for key, value in data.items():
                setattr(db_producto, key, value)
            session.commit()
            session.refresh(db_producto)
            return db_producto
        return None

# Eliminar producto
def delete_producto(producto_id: int) -> bool:
    with get_session() as session:
        db_producto = session.get(Producto, producto_id)
        if db_producto:
            session.delete(db_producto)
            session.commit()
            return True
        return False

# Búsqueda con múltiples filtros
def buscar_productos(filtro: dict) -> list[Producto]:
    """
    Recibe un diccionario de filtros, ej:
    buscar_productos({"nombre": "notebook", "marca": "dell"})
    """
    with get_session() as session:
        query = select(Producto)
        for key, value in filtro.items():
            if hasattr(Producto, key):
                query = query.where(getattr(Producto, key).ilike(f"%{value}%"))
        return session.exec(query).all()

# Búsqueda por nombre
def buscar_productos_por_nombre(nombre: str) -> list[Producto]:
    with get_session() as session:
        return session.exec(
            select(Producto).where(Producto.nombre.ilike(f"%{nombre}%"))
        ).all()

# Búsqueda por marca
def buscar_productos_por_marca(marca: str) -> list[Producto]:
    with get_session() as session:
        return session.exec(
            select(Producto).where(Producto.marca.ilike(f"%{marca}%"))
        ).all()

# Búsqueda por categoría
def buscar_productos_por_categoria(categoria: str) -> list[Producto]:
    with get_session() as session:
        return session.exec(
            select(Producto).where(Producto.categoria.ilike(f"%{categoria}%"))
        ).all()
