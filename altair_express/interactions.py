"""Interactions module."""

import altair as alt
import pandas as pd
import numpy as np
from .utils import get_field_from_encoding, check_axis_meaningful, is_undefined, alt_get, extent_from_column
'''
Interactions have effects and triggers. 
"instruments" are the location-triggers (how to create) 
'''

def add_cursor_to_mark(chart,cursor_type):
    if alt_get(chart,'layer'):
       for layer in chart.layer:
           print('adding cursor to layer',layer.mark)
           if isinstance(chart.mark,str):
              mark_type = layer.mark
              layer.mark = alt.MarkDef(type=mark_type,cursor=cursor_type)
           else: 
              layer.mark.cursor = cursor_type
    else:
        print('adding cursor to layer',chart.mark)
        print(type(chart.mark))
        if isinstance(chart.mark,str):
            mark_type = chart.mark  
            chart.mark = alt.MarkDef(type=mark_type,cursor=cursor_type)
        else: 
          chart.mark.cursor = cursor_type
    return chart
    

def create_selection(chart,interaction):
    selection = None
    # only allow selection on an axis if it is meaningful (ie data encoded, not 'count')
    # check if any axis is aggregate
    
    if interaction['action']['trigger'] == "drag":
        encodings = ['x','y'] # by default
        encodings = [encoding for encoding in encodings if check_axis_meaningful(chart,encoding)]
        # TODO: fix bug if this is a calculated field
        
        selection = alt.selection_interval(encodings=encodings, name='drag-brush')

    if interaction['action']['trigger'] == "click":
        selection = alt.selection_point(name='click')
        
        if 'target' in interaction['action']:
            field = get_field_from_encoding(chart,interaction['action']['target'])
            selection=alt.selection_point(name='click', fields=[field])
        else: 
            x_is_meaningful = check_axis_meaningful(chart,'x')
            y_is_meaningful = check_axis_meaningful(chart,'y')
            if not x_is_meaningful and y_is_meaningful:
                # if x is aggregated (ie is a count), then add y field to selection 
                selection=alt.selection_point(name='click', encodings=['y'])
            elif  x_is_meaningful and not y_is_meaningful:
                # if both of them are 
                selection=alt.selection_point(name='click', encodings=['x'])
            elif not x_is_meaningful and not y_is_meaningful:
                selection=alt.selection_point(name='click', encodings=['x','y'])
        
        
    return selection 

def apply_effect(previous_chart,interaction,selection):
    chart = previous_chart.copy(deep=True)
    # alter the chart object to allow for interaction
    # apply the transform 
    
    if interaction['effect']['transform'] == "filter":
         chart = filter_chart(chart,interaction,selection)
                
        # if no encodings exist, 
    
    if interaction['effect']['transform'] == "highlight":
        chart = highlight_chart(chart,interaction,selection)
            
    if interaction['effect']['transform'] == "group":
        chart = group_chart(chart,interaction,selection)
        
    return chart



def group_chart(chart,interaction,selection):
    return chart
    
    
    
    
def filter_chart(chart,interaction,selection):
    filter_transform = alt.FilterTransform({"param": selection.name})
        # insert at begining to ensure all data gets filtered correctly
    if not is_undefined(chart.transform):
        chart.transform.insert(0,filter_transform)
    else:
        chart.transform = [filter_transform]
        
        # for each encoding in selection 
    encodings = selection.param.select.encodings
    if encodings: 
        for encoding in encodings:
            scale = chart['encoding'][encoding]['scale']

            extent = extent_from_column(chart.data,chart['encoding'][encoding]['field'])
            # TODO: copy the existing scale, just overwrite the domain
            scale = alt.Scale(domain=extent)
            chart['encoding'][encoding]['scale'] = scale
            
    return chart

def highlight_chart(chart,interaction,selection):
    print(selection)
    if True:
        highlight = alt.value('steelblue')
        
        # if the chart already has a color encoding, use that as a conditional
        if not is_undefined(chart.encoding) and not is_undefined(chart.encoding.color):
            highlight = get_field_from_encoding(chart,'color')  
            
        color = alt.condition(selection,highlight,alt.value('lightgray'))
            
            
        chart=chart.encode(color=color)
    return chart 

highlight = {"transform":"highlight"}
_filter = {"transform":"filter"} # _filter as to avoid overloading python's filter function

brush = {"trigger":"drag"}
point = {"trigger":"click"}
color = {"trigger":"click","target":"color"}


highlight_brush = {"effect":highlight,"action":brush} 
highlight_point = {"effect":highlight,"action":point}
highlight_color = {"effect":highlight,"action":color}

filter_brush = {"effect":_filter,"action":brush} 
filter_point = {"effect":_filter,"action":point}


# group_brush
# group_point

# tooltip_point # shows information about one specific value 
# tooltip_brush  # calculates summary statistics about data in selection


# TODO 1/6: Continue to build out these interactions




def add_cursor(chart,interaction):
    if interaction['action']['trigger'] == "drag":
        chart = add_cursor_to_mark(chart,'crosshair')
    if interaction['action']['trigger'] == "click":
        chart = add_cursor_to_mark(chart,'pointer')
    return chart
def add_interaction(chart, interaction):
    
    parameter = create_selection(chart,interaction)
    chart=chart.add_params(parameter)

    chart =  apply_effect(chart,interaction,parameter)

    chart = add_cursor(chart,interaction)
    return chart

