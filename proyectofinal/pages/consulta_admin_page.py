import reflex as rx
from proyectofinal.service.consulta_service import responder_consulta, listar_todas_consultas_repo

class ConsultaAdminState(rx.State):
    consultas: list[dict] = []
    respuesta: str = ""
    consulta_seleccionada: int | None = None

    def cargar_consultas(self):
        self.consultas = [c.dict() for c in listar_todas_consultas_repo()]

    def seleccionar_consulta(self, consulta_id: int):
        self.consulta_seleccionada = consulta_id
        self.respuesta = ""

    def enviar_respuesta(self):
        if self.consulta_seleccionada and self.respuesta.strip():
            responder_consulta(self.consulta_seleccionada, self.respuesta)
            self.consulta_seleccionada = None
            self.respuesta = ""
            self.cargar_consultas()

def consulta_admin_page():
    return rx.vstack(
        rx.heading(" Consultas de usuarios"),
        rx.foreach(
            ConsultaAdminState.consultas,
            lambda c: rx.box(
                rx.text(f" Usuario ID: {c['id_users']}"),
                rx.text(f" Pregunta: {c['pregunta']}"),
                rx.text(f" Respuesta: {c['respuesta'] or 'Sin responder'}"),
                rx.button("Responder", on_click=lambda: ConsultaAdminState.seleccionar_consulta(c["id_consulta"])),
                rx.divider(),
            )
        ),
        rx.cond(
            ConsultaAdminState.consulta_seleccionada is not None,
            rx.vstack(
                rx.text_area(
                    placeholder="Escribí tu respuesta...",
                    value=ConsultaAdminState.respuesta,
                    on_change=lambda e: ConsultaAdminState.set_respuesta(e),
                    width="100%",
                ),
                rx.button("Enviar respuesta", on_click=ConsultaAdminState.enviar_respuesta),
            )
        )
    )

def mostrar_consultas_admin_component():
    return rx.foreach(
        ConsultaAdminState.consultas,
        lambda c: rx.box(
            rx.text(f" Usuario ID: {c['id_users']}"),
            rx.text(f" Pregunta: {c['pregunta']}"),
            rx.cond(
                c["respuesta"] != "", 
                rx.text(f" Respuesta: {c['respuesta']}"),
                rx.text(" Respuesta: Sin responder")
            ),
            rx.button("Responder", on_click=lambda: ConsultaAdminState.seleccionar_consulta(c["id_consulta"])),
            rx.divider(),
        )
    )


@rx.page(route="/consulta_admin", on_load=ConsultaAdminState.cargar_consultas)
def consulta_admin_page():
    return rx.vstack(
        rx.heading(" Consultas de usuarios"),
        mostrar_consultas_admin_component(),
        rx.cond(
            ConsultaAdminState.consulta_seleccionada is not None,
            rx.vstack(
                rx.text_area(
                    placeholder="Escribí tu respuesta...",
                    value=ConsultaAdminState.respuesta,
                    on_change=lambda e: ConsultaAdminState.set_respuesta(e),
                    width="100%",
                ),
                rx.button("Enviar respuesta", on_click=ConsultaAdminState.enviar_respuesta),
            )
        )
    )