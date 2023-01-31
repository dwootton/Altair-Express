"""Main module."""


import altair as alt
import pandas as pd
import numpy as np






# Hist
def create_hist_dataframe(data=None, *, x=None, y=None):
  # create data if x and y are pandas series
  if data is None:
    data = pd.DataFrame({})
    # case that x series is provided 
    if isinstance(x, pd.Series):
      data['x'] = x
      x = 'x'

    # case that y series is provided 
    if isinstance(y, pd.Series):
      data['y'] = y
      y = 'y'
  
  return data,x,y

def hist(data=None,x=None,y=None, width=200,height=50,filters=[],color=None,fill="steelblue",xAxis = alt.Axis(),yAxis=alt.Axis(),interactive=False):
  # ensures that data is the data and x and y are column names
  data,x,y = create_hist_dataframe(data=data,x=x,y=y) 
  chart = None

  layers = {"fg":None,"bg":None}

  if x is not None and y is None:
    layers['fg']= alt.Chart(data).mark_bar(color=fill).encode(
            alt.X(f'{x}:Q', bin=True, axis=xAxis),alt.Y('count()',axis=yAxis)
              ) 
    layers['bg'] = alt.Chart(data).mark_bar(color='lightgray').encode(
        alt.X(f'{x}:Q', bin=True, axis=xAxis),alt.Y('count()',axis=yAxis)
      )
    
    if interactive:

      x_brush = alt.selection_interval(encodings=['x'],resolve="union",name='x_brush')
      
      if type(interactive) == type(alt.selection_interval()):
        x_brush = interactive     
      
      layers['fg'] =  layers['fg'].add_selection(x_brush)
      filters.append(x_brush)


  elif x is  None and y is not None:
    layers['fg']= alt.Chart(data).mark_bar(color=fill).encode(
            alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
              ) 
    layers['bg'] = alt.Chart(data).mark_bar(color='lightgray').encode(
        alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
      )
    
    if interactive:

      y_brush = alt.selection_interval(encodings=['y'],resolve="union",name='y_brush')
      
      if type(interactive) == type(alt.selection_interval()):
        y_brush = interactive     

      
      layers['fg'] =  layers['fg'].add_selection(y_brush)
      filters.append(y_brush)

    
  # elif x is None and y is not None:

  #   chart =  alt.Chart(data).mark_bar(color=fill).encode(
  #     alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
  #       )
  #   if interactive:
  #     y_brush = alt.selection_interval(encodings=['y'],resolve="global",name='y_brush')
  #     if type(interactive) == type(alt.selection_interval()):
  #       y_brush = interactive 
  #     chart = chart.mark_bar(color='lightgray')
  #     chart = chart + alt.Chart(data).mark_bar(color=fill).encode(
  #         alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
  #     ).add_selection(y_brush).transform_filter(y_brush)
  

  if filters:
     for filter in filters:
        layers['fg'] = layers['fg'].transform_filter(filter)

  chart = layers['bg'] + layers['fg'] 
  
  return chart.properties(
          width=width,
          height=height
      )


