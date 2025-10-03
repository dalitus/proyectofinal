import reflex as rx
from proyectofinal.service.catalogo_service import (
    obtener_catalogo,
    buscar_en_catalogo
)
from proyectofinal.service.carrito_service import agregar_item_al_carrito

class CatalogoState(rx.State):
    productos: list[dict] = []
    buscar_texto: str = ""
    error_message: str = ""
    success_message: str = ""
    user_id: int = 0

    @rx.event
    def cargar_productos(self):
        self.productos = obtener_catalogo()
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def actualizar_buscar_texto(self, value: str):
        self.buscar_texto = value

    @rx.event
    def buscar(self):
        resultados = buscar_en_catalogo(self.buscar_texto)
        if resultados:
            self.productos = resultados
            self.error_message = ""
        else:
            self.productos = []
            self.error_message = "No se encontraron productos."

    @rx.event
    def agregar_carrito_con_id(self, producto_id: int):
        if not self.user_id:
            self.error_message = "Debes iniciar sesión para agregar al carrito."
            self.success_message = ""
            return
        agregar_item_al_carrito(self.user_id, producto_id)
        self.success_message = "Producto agregado al carrito ✅"
        self.error_message = ""

    @rx.event
    def ir_a_carrito(self):
        return rx.redirect("/carrito")

    @rx.event
    def ir_a_ubicacion(self):
        return rx.redirect("/ubicacion")

    @rx.event
    def ir_a_consulta(self):
        return rx.redirect("/consulta_usuario")

    @rx.event
    def ir_a_login(self):
        return rx.redirect("/users")