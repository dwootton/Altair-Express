import altair as alt
from .utils import data_type_converter, create_dataframe

def relplot(data=None, *, x=None, y=None,color=None,interactive=None,kind="scatter",width=200,height=200):

  if kind == "scatter":
    return scatterplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  elif kind == "line":
    return lineplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  else : 
    raise ValueError('[relplot] kind parameter should be one of "scatter" or "line"')

def lineplot(data=None, *, x=None, y=None,color=None,filters=None,interactive=None,width=200,height=200):
  if filters is None:
    filters = [] # as filters keeps last executions filters?
  # ensure that data 
  data, x, y = create_dataframe(data=data,x=x,y=y)
  x_type = data_type_converter(data.dtypes[x])
  y_type = data_type_converter(data.dtypes[y])

  line_color = 'steelblue'
  
  layers = {"fg":alt.Chart(data).mark_line().encode(
    alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False)),
    alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False)),
  ),
  "bg":alt.Chart(data).mark_line(color='lightgray').encode(
    alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False)),
    alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False)),
  )}
  


  if color:
    if color not in data.columns:
        layers['fg']=layers['fg'].mark_line(fill=line_color)
    else:
        unique = np.unique(data[color])
        layers['bg']=layers['bg'].encode(alt.Color(legend=None,field=color,scale=alt.Scale(domain=unique,range=['lightgray' for value in unique])))
        layers['fg']=layers['fg'].encode(alt.Color(field=color,scale=alt.Scale()))



  if interactive:
    # default to interval selection
    x_brush = alt.selection_interval(encodings=['x'],resolve="intersect",name='brush')
    if type(interactive) == type(alt.selection_interval()):
        x_brush = interactive  

    layers['fg']=layers['fg'].add_selection(x_brush)  
    
    filters.append(x_brush)
    
  if filters:
     for filter in filters:
        layers['fg'] = layers['fg'].transform_filter(filter)
  
  chart = layers['bg'] + layers['fg'] 

  chart=chart.resolve_scale(
      color='independent'
  )

  return chart.properties(width=width,height=height)

def scatterplot(data=None, *, x=None, y=None,xAxis=alt.Axis(),color=alt.Color(),yAxis=alt.Axis(),filters=None,fill="steelblue",interactive=None,width=200,height=200):
  if filters is None:
    filters = []
  data, x, y = create_dataframe(data=data,x=x,y=y)

  x_type = data_type_converter(data.dtypes[x])
  y_type = data_type_converter(data.dtypes[y])

  
  layers = {"fg":alt.Chart(data).mark_circle().encode(
      alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False),axis=xAxis),
      alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False),axis=yAxis),
  ),"bg":alt.Chart(data).mark_circle(color='lightgray').encode(
      alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False),axis=xAxis),
      alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False),axis=yAxis),
  )} 

  if color:
    if color not in data.columns:
        layers['fg']=layers['fg'].mark_circle(fill=color)
    else:
        layers['fg']=layers['fg'].encode(alt.Color(field=color))


  if interactive:
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