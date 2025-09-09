import reflex as rx
from proyectofinal.service.consulta_service import crear_consulta, listar_consultas_usuario


class ConsultaUsuarioState(rx.State):
    pregunta: str = ""
    id_users: int = 1  # ← Esto deberías obtenerlo dinámicamente si tenés login

    consultas: list[dict] = []

    def enviar_consulta(self):
        if self.pregunta.strip():
            crear_consulta(self.id_users, self.pregunta)
            self.pregunta = ""
            self.cargar_consultas()

    def cargar_consultas(self):
        consultas_obj = listar_consultas_usuario(self.id_users)
        self.consultas = [c.dict() for c in consultas_obj]


    def actualizar_asunto(self, value: str):
        self.asunto = value
    
    def actualizar_mensaje(self, value: str):
        self.mensaje = value



def mostrar_consultas_component() -> rx.Component:
    return rx.vstack(
        rx.foreach(
            ConsultaUsuarioState.consultas.to(list[dict]),
            lambda c: rx.box(
                rx.text(f"Asunto: {c['asunto']}"),
                rx.text(f"Mensaje: {c['mensaje']}"),
                rx.text(f"Respuesta: {c['respuesta'] | 'Sin respuesta'}"),
                border="1px solid gray",
                padding="5px",
                margin="5px",
                border_radius="5px",
            )
        ),
        spacing="3",
    )


@rx.page(route="/consulta_usuario", on_load=ConsultaUsuarioState.cargar_consultas)
def consulta_usuario_page():
    return rx.vstack(
        rx.heading("Enviar consulta"),
        rx.text_area(
                placeholder="Escribí tu consulta...",
                value=ConsultaUsuarioState.pregunta,
                on_change=lambda e: ConsultaUsuarioState.set_pregunta(e),
                width="100%",
            ),
        rx.button("Enviar", on_click=ConsultaUsuarioState.enviar_consulta),
        rx.divider(),
        rx.heading("Tus consultas"),
        rx.foreach(
            ConsultaUsuarioState.consultas,
            lambda c: rx.box(
                rx.text(f" {c.pregunta}"),
                rx.text(f" Respuesta: {c.respuesta | 'Pendiente'}"),
                rx.divider(),
            )
        )
    )
