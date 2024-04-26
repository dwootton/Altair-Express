import altair as alt

from ..utils import is_undefined
from ..interactors import Response

valid_encodings = [
    'angle', 'color', 'detail', 'facet', 'fill', 'fillOpacity', 'href', 
    'key', 'latitude', 'latitude2', 'longitude', 'longitude2', 'opacity', 
    'order', 'radius', 'radius2', 'row', 'shape', 'size', 'stroke', 
    'strokeDash', 'strokeOpacity', 'strokeWidth', 'text', 'theta', 'theta2', 
    'tooltip', 'url', 'x', 'x2', 'xError', 'xError2', 'xOffset', 'y', 'y2', 
    'yError', 'yError2', 'yOffset'
]
def get_encodings(encodings):
    end = [item for item in valid_encodings if not is_undefined(encodings[item])]
    return end



def bin_max(chart,store_name):
    for encoding_type in get_encodings(chart['encoding']):
        encode_value = chart.encoding[encoding_type].__dict__['_kwds']
        
        if encode_value['bin'] and not is_undefined(encode_value['bin']):
            encode = chart.encoding[encoding_type]
            # if encode is just "true" create a bin object, else, just update bin object

            if isinstance(encode, object):
                chart.encoding[encoding_type].bin = {"maxbins":{"signal":store_name}}
            elif encode is True:
                chart.encoding[encoding_type].bin = {"maxbins":{"signal":store_name}}

    return chart
    
