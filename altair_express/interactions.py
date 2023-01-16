"""Interactions module."""

import altair as alt
import pandas as pd
import numpy as np
from .utils import add_encoding,check_axis_binned, get_field_from_encoding, check_axis_meaningful, is_undefined, alt_get, extent_from_column
'''
Interactions have effects and triggers. 
"instruments" are the location-triggers (how to create) 
'''



def add_cursor_to_mark(chart,cursor_type):
    attributes_for_recursion = ['layer','hconcat','vconcat']
    for attribute in attributes_for_recursion:
        
        # TODO: fix this following line. Right now, it enters into if for any layer, concat.
        # instead, it should see if any exists, and if it does, it should use that as the item to search
        if alt_get(chart,attribute):
          for unit_spec in chart[attribute]:
            if isinstance(unit_spec.mark,str):
                mark_type = unit_spec.mark
                unit_spec.mark = alt.MarkDef(type=mark_type,cursor=cursor_type)
            else: 
                unit_spec.mark.cursor = cursor_type
        else:          
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
    
    if interaction.action['trigger'] == "drag":
        encodings = ['x','y'] # by default
        encodings = [encoding for encoding in encodings if check_axis_meaningful(chart,encoding)]
        # TODO: fix bug if this is a calculated field
        
        selection = alt.selection_interval(encodings=encodings, name='drag')

    if interaction.action['trigger'] == "click":
        selection = alt.selection_point(name='click')
        
        if 'target' in interaction.action:
            field = get_field_from_encoding(chart,interaction.action['target'])
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
    # if either encoding is meaningful and the underlying field is binned
    if not x_binned and not y_binned:
        #highlight =
        
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
    def __init__(self, effect, action):
        self.effect = effect
        self.action = action

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

def highlight_brush():
    return Interaction(effect=highlight,action=brush)
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
        chart = add_cursor_to_mark(chart,'crosshair')
    if interaction.action['trigger'] == "click":
        chart = add_cursor_to_mark(chart,'pointer')
    return chart

def add_interaction(chart, interaction):
    
    parameter = create_selection(chart,interaction)
    interaction.set_selection(parameter)
    chart=chart.add_params(parameter)

    chart =  apply_effect(chart,interaction,parameter)

    chart = add_cursor(chart,interaction)
    return chart

