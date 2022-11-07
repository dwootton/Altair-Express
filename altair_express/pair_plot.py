import altair as alt
from .distributional import hist
from .relational import scatterplot
import numpy as np

#chart constructor that will add in interactions 
def pair_plot(data=None,variables=None):
  if data is None:
    raise ValueError('[pairgrid] data cannot be null')

  if variables is None:
    # get all numeric columns from the dataframe 
    variables = list(data.select_dtypes(include=[np.number]).columns.values)

  grid = []
  selection_name = "brush" 
  
  for row_index,row_variable in enumerate(variables):
    grid_row = []
    for column_index,column_variable in enumerate(variables):
      chart = None
      xAxis = None
      yAxis = None

      if row_index == len(variables)-1 :
         xAxis = alt.Axis()

      if column_index == 0:
         yAxis = alt.Axis()

      sel = alt.selection_interval(name='paintbrush',resolve="intersect",encodings=['x','y'])
      
      if row_variable == column_variable:
        
        # plot histogram
        color =alt.condition(
            sel,
            alt.value("steelblue"),
            alt.value("lightgray")
        )
        interactive = alt.selection_interval(name='paintbrush',resolve="intersect",encodings=['x'])
        # ,
        chart = hist(data,filters=[sel],interactive=interactive,x=column_variable,yAxis=yAxis,xAxis=xAxis).properties(height=100,width=100)
        if row_index == 0:
          chart.layer[0].encoding.y.title = row_variable
        if row_index == len(variables)-1:
          chart.layer[0].encoding.x.title = row_variable
        
      else:
        # plot scatterplot
        color =alt.condition(
            sel,
            alt.value("steelblue"),
            alt.value("lightgray")
            
        )
        chart = scatterplot(data,x=column_variable,y=row_variable,color=color,yAxis=yAxis,xAxis=xAxis).add_selection(sel).properties(height=100,width=100)
      grid_row.append(chart)

    grid.append(grid_row)

  chart = None
  for row_index in range(len(grid)):
    row = None
    for column_index in range(len(grid[row_index])):
       if row is None:
          row = grid[row_index][column_index]
       else: 
          row = alt.hconcat(row,grid[row_index][column_index],spacing=5)
      

    if chart is None:
      chart = row
    else: 
      chart = alt.vconcat(chart,row,spacing=5)
  return chart
