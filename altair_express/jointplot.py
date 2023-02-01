
import altair as alt
from .distributional import hist
from .relational import scatterplot

def jointplot(data=None,x=None, y=None):
  
  top = hist(data=data,x=x,width=200,height=50,xAxis=None,yAxis=None)
  right = hist(data=data,y=y,width=50,height=200,xAxis=None,yAxis=None)

  mid = scatterplot(data=data,x=x,y=y)


  # question is there a way to 
  return alt.vconcat(top, alt.hconcat(mid,right,spacing=-10), spacing=-10)
