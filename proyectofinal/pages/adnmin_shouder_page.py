import reflex as rx
from proyectofinal.model.product_model import Producto
from ..service.producto_servicio import (
    obtener_productos,
    crear_producto,
    eliminar_producto,
    editar_producto
)

class AdminState(rx.State):
    productos: list[Producto] = []
    error_message: str = ""

    # Cargar productos
    def cargar_productos(self):
        self.productos = obtener_productos()

    # Crear producto
    def crear_producto(self, data: dict):
        try:
            crear_producto(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
                precio=float(data["precio"]),
                marca=data["marca"],
                categoria=data["categoria"],
                talle=data["talle"],
                imagen=data.get("imagen")
            )
            self.cargar_productos()
            self.error_message = ""
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error_message = f"Error al crear producto: {e}"
    
    # Eliminar producto
    def eliminar_producto(self, producto_id: int):
        try:
            if eliminar_producto(producto_id):
                self.cargar_productos()
                self.error_message = ""
            else:
                self.error_message = "Error al eliminar producto: Producto no encontrado"
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error_message = f"Error al eliminar producto: {e}"
    
    # Editar producto
    def editar_producto(self, producto_id: int, data: dict):
        try:
            if editar_producto(producto_id, data):
                self.cargar_productos()
                self.error_message = ""
            else:
                self.error_message = "Error al editar producto: Producto no encontrado"
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error_message = f"Error al editar producto: {e}"


# -------------------
# PÁGINA DASHBOARD
# -------------------
@rx.page(route='admin_dashboard', title='Admin Dashboard', on_load=AdminState.cargar_productos)
def admin_dashboard_page() -> rx.Component:
    return rx.flex(
        rx.heading("Panel de Administración de Productos", align="center"),
        rx.button(
            "📬 Ir a consultas de usuarios",
            on_click=lambda: rx.redirect("/consulta_admin"),
            color="blue",
            width="100%"
        ),

        crear_producto_dialog_component(),
        table_productos(),
        rx.cond(
            AdminState.error_message != "",
            rx.text(AdminState.error_message, color="red")
        ),
        direction="column",
        style={"width": "70vw", "margin": "auto"}
    )


# -------------------
# TABLA DE PRODUCTOS
# -------------------
def table_productos() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Precio"),
                rx.table.column_header_cell("Marca"),
                rx.table.column_header_cell("Acciones")
            )
        ),
        rx.table.body(
            rx.foreach(
                AdminState.productos,
                lambda p: rx.table.row(
                    rx.table.cell(p.id_producto),
                    rx.table.cell(p.nombre),
                    rx.table.cell(f"${p.precio}"),
                    rx.table.cell(p.marca),
                    rx.table.cell(
                        rx.hstack(
                            rx.button("Eliminar", color_scheme="red",
                                on_click=AdminState.eliminar_producto(p.id_producto)),
                        )
                    )
                    #rx.table.cell(
                      
                    #)
                )
            )
        )
    )


# -------------------
# MODAL CREAR PRODUCTO
# -------------------
def crear_producto_dialog_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Producto")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Producto"),
                crear_producto_form(),
                justify="center",
                align="center",
                direction="column"
            ),
            rx.flex(
                rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                spacing="3",
                margin_top="16px",
                justify="center"
            ),
            style={"width": "400px"}
        )
    )


def crear_producto_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Nombre", name="nombre"),
            rx.input(placeholder="Descripción", name="descripcion"),
            rx.input(placeholder="Precio", name="precio"),
            rx.input(placeholder="Marca", name="marca"),
            rx.input(placeholder="Categoría", name="categoria"),
            rx.input(placeholder="Talle", name="talle"),
            rx.input(placeholder="Imagen URL", name="imagen"),
            rx.dialog.close(rx.button("Guardar", type="submit"))
        ),
        on_submit=AdminState.crear_producto
    )

# -------------------
# MODAL EDITAR PRODUCTO (opcional)
def editar_producto_dialog_component(producto: Producto) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Editar")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Producto ID {producto.id_producto}"),
                editar_producto_form(producto),
                justify="center",
                align="center",
                direction="column"
            ),
            rx.flex(
                rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray")),
                spacing="3",
                margin_top="16px",
                justify="center"
            ),
            style={"width": "400px"}
        )
    )
def editar_producto_form(producto: Producto) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Nombre", name="nombre", value=producto.nombre),
            rx.input(placeholder="Descripción", name="descripcion", value=producto.descripcion),
            rx.input(placeholder="Precio", name="precio", value=str(producto.precio)),
            rx.input(placeholder="Marca", name="marca", value=producto.marca),
            rx.input(placeholder="Categoría", name="categoria", value=producto.categoria),
            rx.input(placeholder="Talle", name="talle", value=producto.talle),
            rx.input(placeholder="Imagen URL", name="imagen", value=producto.imagen),
            rx.dialog.close(rx.button("Guardar", type="submit"))
        ),
        on_submit=lambda data: AdminState.editar_producto(producto.id_producto, {
            "nombre": data["nombre"],
            "descripcion": data["descripcion"],
            "precio": float(data["precio"]),
            "marca": data["marca"],
            "categoria": data["categoria"],
            "talle": data["talle"],
            "imagen": data.get("imagen")
        })
    )


