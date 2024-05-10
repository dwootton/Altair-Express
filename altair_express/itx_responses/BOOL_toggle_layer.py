
from ..interactors import Response

def toggle_layer(chart,store_name):
    return chart.transform_filter(store_name)

def toggle_on():
    return Response(lambda chart,store_name, ps: toggle_layer(chart,store_name.name))