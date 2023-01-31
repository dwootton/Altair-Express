
import altair as alt

from altair_express.interactions import process_effects
from .utils import data_type_converter, create_dataframe
import numpy as np
from .distributional import heatmap

def relplot(data=None, *, x=None, y=None,color=None,interactive=None,kind="scatter",width=200,height=200):

  if kind == "scatter":
    return scatterplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  elif kind == "line":
    return lineplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  else : 
    raise ValueError('[relplot] kind parameter should be one of "scatter" or "line"')

def generate_shorthand(input_field,data):
  # if input_field contains ":Q"  or ":N" then return input_field
  if input_field[-2:] == ":Q" or input_field[-2:] == ":N" or input_field[-2:] == ":O":
    return input_field # already as shorthand

  data_type = data_type_converter(data.dtypes[input_field])
  return f'{input_field}:{data_type}'


def process_chart_config(chart,x_axis,y_axis):
 
  if x_axis is None or y_axis is None:
       chart = chart.properties(title=config["title"])
   
  return chart

def lineplot(data=None, x=None, y=None,yAxis=alt.Axis(),xAxis=alt.Axis(),color=None,effects=None,width=200,height=200):
  data, x, y = create_dataframe(data=data,x=x,y=y)

  x_shorthand = generate_shorthand(x,data)
  y_shorthand = generate_shorthand(y,data)

  line_color = 'steelblue'
  
  chart = alt.Chart(data).mark_line().encode(
    alt.X(shorthand=x_shorthand, scale=alt.Scale(zero=False),axis=xAxis),
    alt.Y(shorthand=y_shorthand, scale=alt.Scale(zero=False),axis=yAxis),
  )

  if color:
    if color not in data.columns:
        chart= chart.mark_line(fill=line_color)
    else:
        chart=chart.encode(alt.Color(field=color,scale=alt.Scale()))

  if effects:
    chart = process_effects(chart,effects)

  return chart.properties(width=width,height=height)

def kdeplot(data=None,x=None,color=None,effects=None,width=200,height=200):
  x_shorthand = generate_shorthand(x,data)

  line_color = 'steelblue'
  transform_params ={
    "density":x,
    "as_":[x,'density'],
    "groupby":[color],
  }
  not_none_params = {k:v for k, v in transform_params.items() if v is not None and (not isinstance(v,list) or len(v)>0 and v[0] is not None)}

  chart = alt.Chart(data).mark_line().transform_density(**not_none_params).encode(
    alt.X(shorthand=x_shorthand, scale=alt.Scale(zero=False)),
    alt.Y(shorthand='density:Q'),
  )

  if color:
    if color not in data.columns:
        chart= chart.mark_line(fill=line_color)
    else:
        chart=chart.encode(alt.Color(field=color,scale=alt.Scale()))

  if effects:
    chart = process_effects(chart,effects)

  return chart

def scatterplot(data=None, *, x=None, y=None,xAxis=alt.Axis(),color=None,yAxis=alt.Axis(),effects=None,fill="steelblue",width=200,height=200):

  data, x, y = create_dataframe(data=data,x=x,y=y)

  x_type = data_type_converter(data.dtypes[x])
  y_type = data_type_converter(data.dtypes[y])

  
  chart = alt.Chart(data).mark_circle().encode(
      alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False),axis=xAxis),
      alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False),axis=yAxis),
  )

  if color:
    if color not in data.columns:
        chart=chart.mark_circle(fill=color)
    else:
        chart=chart.encode(alt.Color(field=color))

  if effects:
    chart = process_effects(chart,effects)
  


  return chart.properties(width=width,height=height)


def corr_map(data=None, vars=None):
  if vars is None:
    vars = data.columns

  correlation = data.corr()
  return heatmap(correlation)