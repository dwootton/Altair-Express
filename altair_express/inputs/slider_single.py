import altair as alt
from ..interactors import Generator

def single_slider(minimum =1, maximum=100, initial_value=50, step=1):
    slider = alt.binding_range(min=minimum, max=maximum, step=step, )
    cutoff = alt.param(bind=slider, value=initial_value, name="slider")
    return Generator(listener=cutoff, name="slider", value=50, type="Numeric")