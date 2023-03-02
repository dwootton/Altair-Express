
import altair as alt
from .distributional import hist
from .relational import scatterplot
import numpy as np

def pairplot(data=None,variables=None):
  if data is None:
    raise ValueError('[pairgrid] data cannot be null')

  if variables is None:
    # get all numeric columns from the dataframe 
    variables = list(data.select_dtypes(include=[np.number]).columns.values)

  grid = []
  
  for row_index,row_variable in enumerate(variables):
    grid_row = []
    for column_index,column_variable in enumerate(variables):
      chart = None
      
      y_axis = None
      x_axis = None

      if row_index == len(variables)-1 :
         x_axis = alt.Axis()

      if column_index == 0:
         y_axis = alt.Axis()

      
      if row_variable == column_variable:
       
        # ,
        chart = hist(data,x=column_variable,y_axis=y_axis,x_axis=x_axis).properties(height=100,width=100)
        if row_index == 0:
          chart.encoding.y.title = row_variable
        if row_index == len(variables)-1:
          chart.encoding.x.title = row_variable
        
      else:
       
        chart = scatterplot(data,x=column_variable,y=row_variable,y_axis=y_axis,x_axis=x_axis).properties(height=100,width=100)
      grid_row.append(chart)

    grid.append(grid_row)

  chart = None
  rows =[]

  for row_index in range(len(grid)):
      rows.append(alt.hconcat(*grid[row_index],spacing=5))

  chart = alt.vconcat(*rows,spacing=5)
    
  return chart