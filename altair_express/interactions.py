"""Interactions module."""

import altair as alt
import pandas as pd
import numpy as np
from .utils import add_encoding,check_axis_binned, get_field_from_encoding, check_axis_meaningful, is_undefined, alt_get, extent_from_column
'''
Interactions have effects and triggers. 
"instruments" are the location-triggers (how to create) 
'''


def add_cursor_to_mark(unit_chart,cursor_type):
    if isinstance(unit_chart.mark,str):
        mark_type = unit_chart.mark
        unit_chart.mark = alt.MarkDef(type=mark_type,cursor=cursor_type)
    else: 
        unit_chart.mark.cursor = cursor_type
    return unit_chart

def recursively_add_to_mark(chart,cursor_type):
    if hasattr(chart,'mark'):
        chart = add_cursor_to_mark(chart,cursor_type)
        return chart

    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        # TODO: fix this following line. Right now, it enters into if for any layer, concat.
        # instead, it should see if any exists, and if it does, it should use that as the item to search
        if alt_get(chart,attribute):
          for unit_spec in chart[attribute]:
              unit_spec = recursively_add_to_mark(unit_spec,cursor_type)
 
    return chart
    
def check_if_line(chart):
    if isinstance(chart.mark,str):
        return chart.mark == 'line' or chart.mark == 'area'  
    else: 
        return chart.mark.type == 'line' or chart.mark.type == 'area'
    

def create_selection(chart,interaction):
    selection = None
    # only allow selection on an axis if it is meaningful (ie data encoded, not 'count')
    # check if any axis is aggregate
    
    if interaction.action['trigger'] == "drag":
        encodings =  ['x','y'] # by default
        encodings = [encoding for encoding in encodings if check_axis_meaningful(chart,encoding)]

        # if it is a line chart without additional encodings options, use x
        has_options = getattr(interaction,'options',None) != None
        if check_if_line(chart) and (not has_options or (has_options and 'encodings' not in interaction.options)):
            encodings = ['x']

        if has_options and 'encodings' in interaction.options:
            encodings = interaction.options['encodings']


        selection = alt.selection_interval(encodings=encodings, name='drag')
        print(selection)
    if interaction.action['trigger'] == "click":
        selection = alt.selection_point(name='click')
        
        if 'target' in interaction.action:
            field = get_field_from_encoding(chart,interaction.action['target'])
            selection=alt.selection_point(name='click', fields=[field],**interaction.options)
        else: 
            x_is_meaningful = check_axis_meaningful(chart,'x')
            y_is_meaningful = check_axis_meaningful(chart,'y')
            if not x_is_meaningful and y_is_meaningful:
                # if x is aggregated (ie is a count), then add y field to selection 
                selection=alt.selection_point(name='click', encodings=['y'],**interaction.options)
            elif  x_is_meaningful and not y_is_meaningful:
                # if both of them are 
                selection=alt.selection_point(name='click', encodings=['x'],**interaction.options)
            elif not x_is_meaningful and not y_is_meaningful:
                selection=alt.selection_point(name='click', encodings=['x','y'],**interaction.options)
        
    
    return selection 

def apply_effect(previous_chart,interaction,selection):
    chart = previous_chart.copy(deep=True)
    # alter the chart object to allow for interaction
    # apply the transform 
    
    if interaction.effect['transform'] == "filter":
         chart = filter_chart(chart,interaction,selection)
                
        # if no encodings exist, 
    
    if interaction.effect['transform'] == "highlight":
        chart = highlight_chart(chart,interaction,selection)
    
    if interaction.effect['transform'] == "group":
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
    # if any of the axes are aggregated
    x_binned = check_axis_binned(chart,'x')
    y_binned = check_axis_binned(chart,'y')
    is_line = check_if_line(chart)

    if  is_line:
        # for line charts, create a new layer with a color scale that maps to light gray
        color = get_field_from_encoding(chart,'color')      

        transform = None

        if getattr(chart,'transform',None):
            transform = getattr(chart,'transform',None) 
            chart.transform = alt.Undefined

        chart = chart + chart 

        if color == None:
          
            chart.layer[0]=chart.layer[0].encode(color=alt.value('lightgray'))
            chart.layer[1]=chart.layer[1].encode(color=alt.value('steelblue'))
        else: 
            unique = np.unique(chart.data[color])
            chart.layer[0]=chart.layer[0].encode(alt.Color(legend=None,field=color,scale=alt.Scale(domain=unique,range=['lightgray' for value in unique])))
            chart.layer[1]=chart.layer[1].encode(alt.Color(field=color,scale=alt.Scale()))

        if transform:
          chart.transform = transform

        chart=chart.resolve_scale(
            color='independent'
        )

        filter_transform = alt.FilterTransform({"param": selection.name})
        if type(chart.layer[1].transform) is not alt.utils.schemapi.UndefinedType:
            chart.layer[1].transform.insert(0,filter_transform)
        else:
            chart.layer[1].transform = [filter_transform]
        print('passed transform')


    elif not x_binned and not y_binned :
            # if either encoding is meaningful and the underlying field is binned

        
        # if the chart already has a color encoding, use that as a conditional
        highlight = get_field_from_encoding(chart,'color')  or  alt.value('steelblue')
        #if 'encoding' in chart and not is_undefined(chart.encoding) and not is_undefined(chart.encoding.color):
        #    highlight = get_field_from_encoding(chart,'color')  
            
        color = alt.condition(selection,highlight,alt.value('lightgray'))
     
        chart = add_encoding(chart,color)
        
    else:
      # used for any elements where height, width, etc are controlled by filter 
        color_encoding = chart.encoding.color

        chart.encoding.color = alt.value('lightgray')
        chart = chart + chart 
        chart.layer[1].encoding.color = color_encoding

        filter_transform = alt.FilterTransform({"param": selection.name})
        if type(chart.layer[1].transform) is not alt.utils.schemapi.UndefinedType:
            chart.layer[1].transform.insert(0,filter_transform)
        else:
            chart.layer[1].transform = [filter_transform]
    return chart 



class Interaction:
    def __init__(self, effect, action,options=None):
        self.effect = effect
        self.action = action
        self.options = options


    def __add__(self, other):
        #chart 
        return add_interaction(other,self)
    def __radd__(self, other):
        return self.__add__(other)

    def set_selection(self,selection):
        self.selection = selection
    def get_selection(self):
        return self.selection

highlight = {"transform":"highlight"}
_filter = {"transform":"filter"} # _filter as to avoid overloading python's filter function

brush = {"trigger":"drag"}
point = {"trigger":"click"}
color = {"trigger":"click","target":"color"}

def highlight_brush(options=None):
    return Interaction(effect=highlight,action=brush,options=options)

def highlight_point():
    return Interaction(effect=highlight,action=point)
def highlight_color():
    return Interaction(effect=highlight,action=color)
def filter_brush():
    return Interaction(effect=_filter,action=brush)
def filter_point():
    return Interaction(effect=_filter,action=point)


# group_brush
# group_point

# tooltip_point # shows information about one specific value 
# tooltip_brush  # calculates summary statistics about data in selection


def process_effects(chart,effects):
    if 'filter' in effects:
      chart = process_filters(chart,effects['filter'])
    elif 'highlight' in effects:
      chart = process_highlights(chart,effects['highlight'])
    return chart

def process_highlights(chart,highlights):
  # if filter is not an array, make it an array
  if not isinstance(highlights, list):
      highlights = [highlights]
  for highlight in highlights:
      if isinstance(highlight, Interaction):
          parameter = highlight.get_selection()
          chart = apply_effect(chart,highlight,parameter)
  return chart

def process_filters(chart,filters):
  if not isinstance(filters, list):
      filters = [filters]

  for filter in filters:
      # if filter is Interaction instance 
      if isinstance(filter, Interaction):
          parameter = filter.get_selection()
          chart = chart.transform_filter(parameter)
      else: 
          chart = chart.transform_filter(filter)
  return chart

def add_cursor(chart,interaction):
    if interaction.action['trigger'] == "drag":
        chart = recursively_add_to_mark(chart,'crosshair')
    if interaction.action['trigger'] == "click":
        chart = recursively_add_to_mark(chart,'pointer')
    return chart

def add_interaction(chart, interaction):
    
    parameter = create_selection(chart,interaction)
    interaction.set_selection(parameter)
    chart=chart.add_params(parameter)

    chart =  apply_effect(chart,interaction,parameter)
    chart = add_cursor(chart,interaction)

    return chart

