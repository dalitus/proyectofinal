import reflex as rx
from proyectofinal.pages.users_page import users_page
from proyectofinal.pages.catalogo_page import catalogo_page
from proyectofinal.pages.andmin_page import admin_login_page
from proyectofinal.pages.adnmin_shouder_page import admin_dashboard_page
from proyectofinal.pages.ubicaccion_page import ubicaccion_page
from proyectofinal.pages.carrito_page import carrito_page
from proyectofinal.pages.producto_detalle_page import detalle_producto_page

from proyectofinal.pages.consulta_usuario_page import consulta_usuario_page
from proyectofinal.pages.consulta_admin_page import consulta_admin_page

class UsersState(rx.State):
    pass

app = rx.App()
 
app.add_page(users_page, route="/", title="Usuarios")
app.add_page(catalogo_page, route="/catalogo", title="Catálogo")
app.add_page(admin_login_page, route="/admin_login", title="Login Admin")
app.add_page(admin_dashboard_page, route="/admin_dashboard", title="Panel Admin")
app.add_page(ubicaccion_page, route="/ubicacion", title="Ubicación")
app.add_page(carrito_page, route="/carrito", title="Carrito de Compra")
app.add_page(detalle_producto_page, route="/detalle_producto", title="Detalle Producto")

app.add_page(consulta_usuario_page, route="/consulta_usuario", title="Consulta Usuario")  
app.add_page(consulta_admin_page, route="/consulta_admin", title="Consulta Admin")
