import reflex as rx

def notifail_component(mensaje: str, icon_notify: str, color: str) -> rx.Component:
    return rx.callout(
        mensaje,
        icon=icon_notify,
        style={
            "position": "fixed",
            "top": "0px",
            "right": "0px",
            "margin": "10px",
        },
        color_scheme=color,
    )

staile_notifail= {
    "position": "fixed",
    "top": "0px",
    "right": "0px",
    "margin": "10px 10px",
}
