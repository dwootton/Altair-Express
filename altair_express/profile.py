
import altair as alt

from .utils import is_undefined
from .distributional import hist, countplot
from pandas.api.types import is_numeric_dtype
import pandas as pd
import numpy as np
from altair_express.interactions import process_effects

def profile(data=None,vars=None,effects=None,category_limit=15):
  if vars is None:
    vars = data.columns
  
  # sort so they're in line with the table marks
  if type(vars) is list:
    vars.sort()
  
  
  charts = []

  column_width = 90

  chart_padding = 15
  chart_width = column_width-chart_padding
  charts=[]

  for index, variable in enumerate(vars):
   
      if(is_numeric_dtype(data[variable])):
        charts.append(hist(data = data,x = variable,width=chart_width,y_axis=None))

      else:
        # append blank till count plot are ready
        uniques = pd.unique(data[variable])
        if len(uniques) > category_limit:
          chart = (alt.Chart(pd.DataFrame({'col':['value']})).mark_text(text=f'{variable}',dy=54,fill="black",fontWeight="bold") +
                       alt.Chart(pd.DataFrame({'col':['value']})).mark_text(text=f'{len(uniques)} categories'))
          charts.append(chart.properties(width=column_width,height=50))
        else:
          charts.append(countplot(data=data,x=variable,width=column_width,height=50,y_axis=None))
        

  chart = alt.hconcat(*charts, spacing=chart_padding)

  if effects:
    chart = process_effects(chart,effects)

  if is_undefined(chart.data):
    chart.data = data

  return chart
