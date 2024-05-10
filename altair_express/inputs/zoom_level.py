from ..signals import Signal, OnEvent
from ..interactors import Generator

def zoom_level(minimum=1,maximum=100,step=1):
    listen = Signal(
        name="zoom",
        value=10,
        on=[OnEvent(
            events=[{"type":"wheel", "consume":True}],
            update=f"{step}*floor(min(max(zoom + (event.deltaY/2), {minimum}),{maximum})/{step})",
            force=True
        )]
    )

    return Generator(listener=listen, name="zoom", value="zoom", type="Numeric")