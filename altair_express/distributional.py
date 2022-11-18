import altair as alt
import pandas as pd
import numpy as np


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

      brush = alt.selection_interval(encodings=['x'],resolve="union",name='brush')
      
      if isinstance(interactive,alt.Selection):
        brush = interactive     
      
      layers['fg'] =  layers['fg'].add_selection(brush)
      filters.append(brush)


  elif x is  None and y is not None:
    layers['fg']= alt.Chart(data).mark_bar(color=fill).encode(
            alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
              ) 
    layers['bg'] = alt.Chart(data).mark_bar(color='lightgray').encode(
        alt.Y(f'{y}:Q', bin=True, axis=yAxis),alt.X('count()',axis=xAxis)
      )
    
    if interactive:

      brush = alt.selection_interval(encodings=['y'],resolve="union",name='brush')
      
      if isinstance(interactive,alt.Selection):
        brush = interactive     

      
      layers['fg'] =  layers['fg'].add_selection(brush)
      filters.append(brush)
  

  if filters:
     for filter in filters:
        layers['fg'] = layers['fg'].transform_filter(filter)

  chart = layers['bg'] + layers['fg'] 
  
  return chart.properties(
          width=width,
          height=height
      )



def violin_plots(data=None,y=None,groupby=None, yAxis=None,xAxis=alt.Axis(labels=False, values=[0],grid=False, ticks=True)):
  facet_vars = [None]
  if groupby:
    facet_vars=np.unique(data[groupby])

  brush = alt.selection_interval(
    name='brush',
    encodings=['y'],
    empty="all"
  )

  charts =[]

  for index,variable in enumerate(facet_vars):
    # filter to unique value
    base = alt.Chart(data=data)

    # filter to only one variable
    if variable is not None:
      base=base.transform_filter(
          alt.FieldEqualPredicate(field=groupby, equal=variable)
      )

    if yAxis is None:
      if index == 0:
        yAxis = alt.Axis(grid=False, ticks=True)
    else:
      if index != 0:
        yAxis = None
          


    base = base.transform_density(
        y,
        as_=[y, 'density'],
        extent=[5, 55],
    ).transform_stack(
        stack= "density",
        groupby= [y],
      as_= ["x", "x2"],
      offset= "center"
    )

    layers = {'fg':None,'bg':None}
    # for each value in origin, 
      # create layered plot
    # concat plots together

    layers['bg'] = base.mark_area(color="lightgray",
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



    layers['fg'] = base.mark_area(orient='horizontal', align="center",
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
    ).add_selection(
        brush
    ).transform_filter(
        brush
    )
                    
    chrt = layers['bg'] + layers['fg']
    charts.append(chrt.properties(width=100,title = alt.TitleParams(text = variable )))

  final_chart = None
  for chart in charts:
    if final_chart is None:
      final_chart = chart
    else:
      final_chart = alt.hconcat(final_chart,chart,spacing=0)
  return final_chart


def countplot(data=None,x=None,xAxis=alt.Axis(),yAxis=alt.Axis(), interactive=False, filters=[],width=250,height=150, max_bars = None):
  if data is None:
    if x is None:
      raise ValueError('[countplot] no data or data series provided.')
    data = pd.DataFrame({})
    if isinstance(x, pd.Series):
      data['x'] = x
      x = 'x'

  layers = {"fg":alt.Chart(data).mark_bar(color="steelblue")
    .encode(
      alt.X(f'{x}:N',axis=xAxis), # remove the sort as that will keep it consistent with the background
            alt.Y(f'count({x}):Q',axis=yAxis)
  ),"bg":alt.Chart(data).mark_bar(color="lightgray")
    .encode(
      alt.X(f'{x}:N',sort='-y',axis=xAxis), 
      alt.Y(f'count({x}):Q',axis=yAxis)
  )}

  if interactive:
      x_brush = alt.selection_multi(name='brush',encodings=['x'],resolve='union')
      if isinstance(interactive,alt.Selection):
        x_brush = interactive     
      
      layers['bg'] =  layers['bg'].add_selection(x_brush)
      filters.append(x_brush)
   
  if filters:
     for filter in filters:
        layers['fg'] = layers['fg'].transform_filter(filter)

  chart = layers['bg'] + layers['fg'] 
  return chart.properties(
          width=width,
          height=height
      )