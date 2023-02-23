
import altair as alt
import pandas as pd
import numpy as np

from .interactions import Interaction, apply_effect, process_effects

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
  elif isinstance(data, pd.Series):
    data = pd.DataFrame({'x':data})
    x = 'x'
  
  return data,x,y

def hist(data=None,x=None,y=None,color=None, max_bins=10,width=200,height=50,effects=None,x_axis = alt.Axis(),y_axis = alt.Axis() ,x_scale = alt.Scale(), y_scale= alt.Scale()):
  # ensures that data is the data and x and y are column names
  data,x,y = create_hist_dataframe(data=data,x=x,y=y) 

  fill="steelblue"

  if color and color not in data.columns:
    fill = color
    color = None

  chart = alt.Chart(data)

  if x is not None:
    chart = chart.mark_bar(color=fill).encode(
            alt.X(f'{x}:Q', bin=alt.Bin(maxbins=max_bins),scale=x_scale, axis=x_axis),alt.Y('count()',axis=y_axis)
              ) 
  if y is not None:
    chart = chart.mark_bar(color=fill).encode(
            alt.Y(f'{y}:Q', bin=alt.Bin(maxbins=max_bins),scale=y_scale, axis=y_axis),alt.X('count()',axis=x_axis)
              )
  if color:
      chart = chart.encode(
        alt.Color(f'{color}:N'), opacity=(alt.value(0.5))
      )
  
    
  if effects:
    chart = process_effects(chart,effects)

  return chart.properties(
          width=width,
          height=height
      )

def stripplot(data=None,x=None,row=None,color=None, configure_facet=True, size=None,facet_params={},width=200,height=50,effects=None,y_axis =alt.Axis(values=[0], ticks=True, grid=False, labels=False),x_axis=alt.Axis()):
 
    # dynamically set size of marks based on number of data points
    if not size and len(data) > 1000:
      size = 8
    elif not size and len(data) > 100:
      size = 40
    elif not size:
      size = 90
    

    chart = alt.Chart(data,width=width,
          height=height).mark_circle(size=size).encode(
      y=alt.Y(
          'jitter:Q',
          title=None,
          axis=y_axis,
          #scale=alt.Scale(),
      ),
      x=alt.X(x,axis=x_axis),
          ).transform_calculate(
            # Generate Gaussian jitter with a Box-Muller transform
            jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
        )                  
    if color:
      chart = chart.encode(color=alt.Color(color))

    if row:
        chart = chart.facet(row=row,**facet_params)
   
    if effects:
      chart = process_effects(chart,effects)

    if configure_facet:
      chart = chart.configure_facet(
          spacing=0
      ).configure_view(
          stroke=None
      )
    return chart

def violin_plot(data=None,y=None,groupby=None, yAxis=None,xAxis=alt.Axis(labels=False, values=[0],grid=False, ticks=True),interactive=False,filters=None):
  if filters is None:
    filters = []

  facet_vars = [None]
  if groupby:
    facet_vars=pd.unique(data[groupby])


  charts =[]

  for index,variable in enumerate(facet_vars):
    # filter to unique value
    chart = alt.Chart(data=data)

    # filter to only one variable
    if variable is not None:
      chart=chart.transform_filter(
          alt.FieldEqualPredicate(field=groupby, equal=variable)
      )

    if yAxis is None:
      if index == 0:
        yAxis = alt.Axis(grid=False, ticks=True)
    else:
      if index != 0:
        yAxis = None
          
    chart = chart.mark_area().transform_density(
        y,
        as_=[y, 'density'],
    ).transform_stack(
        stack= "density",
        groupby= [y],
      as_= ["x", "x2"],
      offset= "center"
    ).encode(
        y=alt.Y(f'{y}:Q',axis=yAxis),
        x=alt.X(
            field='x',
            impute=None,
            title=None,
            type ="quantitative",
            axis=xAxis,
        ),
            x2=alt.X2(field = "x2")

    )


  
    if filters:
      for filter in filters:
        chart = chart.transform_filter(filter)
    
    charts.append(chart.properties(width=100,title = alt.TitleParams(text = variable )))
  final_chart = alt.hconcat(charts=charts,spacing=0)
  
  return final_chart


def countplot(data=None,x=None,x_axis=alt.Axis(),y_axis=alt.Axis(),sort=None, limit=15, effects=None,width=250,height=150):
  
 

  if data is None:
    if x is None:
      raise ValueError('[countplot] no data or data series provided.')
    data = pd.DataFrame({})
    if isinstance(x, pd.Series):
      data['x'] = x
      x = 'x'

  if sort is None:
    # sort in a descending order, 
    # the sort must be specified with the columns because otherwise if interaction is present the categorical labels will change their counts. 
    sort = alt.Sort(data[x].value_counts().index.tolist())


  chart = alt.Chart(data).mark_bar().encode(
      alt.X(field=f'{x}',axis=x_axis,sort=sort), # remove the sort as that will keep it consistent with the background
      alt.Y(f'count({x}):Q',axis=y_axis)
  )
   
  if effects:
    chart = process_effects(chart,effects)

   
  return chart.properties(
          width=width,
          height=height
      )

def heatmap(data=None):
  if data is None:
    raise ValueError('[heatmap] no data or data series provided.')
  
  
  source = pd.DataFrame(data.unstack().reset_index().rename(columns={0:"value"}))


  x_variable = source.columns[0]
  y_variable = source.columns[1]

  
  chart = alt.Chart(source).mark_rect().encode(
    x=f'{x_variable}:O',
    y=f'{y_variable}:O',
    color='value:Q'
  )
  return chart