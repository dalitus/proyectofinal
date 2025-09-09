import reflex as rx

# Estado de ubicación
class UbicacionState(rx.State):
    direccion: str = ""
    mensaje: str = ""

    # Actualizar dirección
    def actualizar_direccion(self, value: str):
        self.direccion = value

    # Guardar dirección
    def guardar_direccion(self):
        if self.direccion.strip() == "":
            self.mensaje = "Ingrese una dirección válida"
        else:
            self.mensaje = f"Dirección guardada: {self.direccion}"

# Página de ubicación
@rx.page(route="/ubicacion", title="Ubicación")
def ubicaccion_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Ubicación del Usuario", align="center"),
        rx.input(
            placeholder="Ingrese su dirección",
            on_change=UbicacionState.actualizar_direccion
        ),
        rx.button("Guardar", on_click=UbicacionState.guardar_direccion),
        rx.cond(
            UbicacionState.mensaje != "",
            rx.text(UbicacionState.mensaje, color="green")
        ),
        spacing="3",
        style={"width": "80vw", "margin": "auto"}
    )
