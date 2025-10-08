import reflex as rx

async def get_user_id(state: rx.State) -> int:
    return await state.get_var_value("users_state.user_id")
