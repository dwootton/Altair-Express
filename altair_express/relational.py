from ..utils import data_type_converter, create_dataframe

def relplot(data=None, *, x=None, y=None,color=None,interactive=None,kind="scatter",width=200,height=200):

  if kind == "scatter":
    return scatterplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  elif kind == "line":
    return lineplot(data=data,x=x,y=y,color=color,interactive=interactive,width=width,height=height)
  else : 
    raise ValueError('[relplot] kind parameter should be one of "scatter" or "line"')

def lineplot(data=None, *, x=None, y=None,color=None,interactive=None,width=200,height=200):
  # ensure that data 
  data, x, y = create_dataframe(data=data,x=x,y=y)
  x_type = data_type_converter(data.dtypes[x])
  y_type = data_type_converter(data.dtypes[y])
  chart = alt.Chart(data).mark_line().encode(
    alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False)),
    alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False)),
  ).properties(width=width,height=height)

  return chart

def scatterplot(data=None, *, x=None, y=None,xAxis=alt.Axis(),color=alt.Color(),yAxis=alt.Axis(),fill="steelblue",interactive=None,width=200,height=200):
  data, x, y = create_dataframe(data=data,x=x,y=y)

  x_type = data_type_converter(data.dtypes[x])
  y_type = data_type_converter(data.dtypes[y])
  
  chart =  alt.Chart(data).mark_circle().encode(
    alt.X(shorthand=f'{x}:{x_type}', scale=alt.Scale(zero=False),axis=xAxis),
      alt.Y(shorthand=f'{y}:{y_type}', scale=alt.Scale(zero=False),axis=yAxis),
    color=color
  ).properties(width=width,height=height)

  return chart
