import altair as alt
from ..utils import data_type_converter, create_dataframe
import numpy as np

from .interactions import Interaction, apply_effect, process_effects

def relplot(data=None, *, x=None, y=None,color=None,interactive=None,kind="scatter",width=200,height=200):

  if kind == "scatter":
    return scatterplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  elif kind == "line":
    return lineplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  else : 
    raise ValueError('[relplot] kind parameter should be one of "scatter" or "line"')

def lineplot(data=None, *, x=None, y=None,color=None,effects=None,width=200,height=200):
  if filters is None:
    filters = [] # as filters keeps last executions filters?
  # ensure that data 
  data, x, y = create_dataframe(data=data,x=x,y=y)
  #x_type = data_type_converter(data.dtypes[x])
  #y_type = data_type_converter(data.dtypes[y])

  fill = 'steelblue'
  
  if color and color not in data.columns:
     fill = color
  chart = alt.Chart(data).mark_line(fill=fill).encode(
    alt.X(field=x, scale=alt.Scale(zero=False)),
    alt.Y(field=y, scale=alt.Scale(zero=False)),
  )
  


  #if color:
  #  if color not in data.columns:
  #      layers['fg']=layers['fg'].mark_line(fill=line_color)
  #  else:
  #      unique = pd.unique(data[color])
  #      layers['bg']=layers['bg'].encode(alt.Color(legend=None,field=color,scale=alt.Scale(domain=unique,range=['lightgray' for value in unique])))
  #      layers['fg']=layers['fg'].encode(alt.Color(field=color,scale=alt.Scale()))



  
    
  if effects:
    chart = process_effects(chart,effects)
  
  chart = layers['bg'] + layers['fg'] 

  chart=chart.resolve_scale(
      color='independent'
  )

  return chart.properties(width=width,height=height)

def scatterplot(data=None, *, x=None, y=None,x_axis=alt.Axis(),color=None,y_axis=alt.Axis(),effects=None,width=200,height=200):
  if filters is None:
    filters = []
  data, x, y = create_dataframe(data=data,x=x,y=y)
  
  layers = {"fg":alt.Chart(data).mark_circle().encode(
      alt.X(field=x, scale=alt.Scale(zero=False),axis=x_axis),
      alt.Y(field=y, scale=alt.Scale(zero=False),axis=y_axis),
  ),"bg":alt.Chart(data).mark_circle(color='lightgray').encode(
      alt.X(field=x, scale=alt.Scale(zero=False),axis=x_axis),
      alt.Y(field=y, scale=alt.Scale(zero=False),axis=y_axis),
  )} 


  if color:
    if color not in data.columns:
        layers['fg']=layers['fg'].mark_circle(fill=color)
    else:
        layers['fg']=layers['fg'].encode(alt.Color(field=color))


  if effects:
      x_y_brush = alt.selection_interval(encodings=['x','y'],resolve="intersect",name='brush')
      if type(interactive) == type(alt.selection_interval()):
        x_y_brush = interactive     
      layers['bg'] =  layers['bg'].add_selection(x_y_brush)
      filters.append(x_y_brush)
  

  if filters:
    for filter in filters:
      layers['fg'] = layers['fg'].transform_filter(filter)

  chart = layers['bg'] + layers['fg']

  return chart.properties(width=width,height=height)