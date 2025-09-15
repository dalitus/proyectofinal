from sqlmodel import select, or_
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
        session.refresh(producto)
        return producto

# Actualizar producto
def update_producto(producto_id: int, data: dict) -> Producto | None:
    with get_session() as session:
        db_producto = session.get(Producto, producto_id)
        if db_producto:
            for key, value in data.items():
                if hasattr(db_producto, key):
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

# Búsqueda general por texto (solo en campos de texto)
def buscar_productos_por_texto(texto: str) -> list[Producto]:
    with get_session() as session:
        query = select(Producto).where(
            or_(
                Producto.nombre.ilike(f"%{texto}%"),
                Producto.descripcion.ilike(f"%{texto}%"),
                Producto.marca.ilike(f"%{texto}%"),
                Producto.categoria.ilike(f"%{texto}%"),
                Producto.talle.ilike(f"%{texto}%")
            )
        )
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


