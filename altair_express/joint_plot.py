import altair as alt
from .distributional import hist
from .relational import scatterplot

def joint_plot(data=None,x=None, y=None,width=200,height=200):
  x_brush = alt.selection_interval(encodings=['x'],resolve="intersect",name="brush")
  y_brush = alt.selection_interval(encodings=['y'],resolve="intersect",name="brush")

  top = hist(data=data,x=x,width=200,height=50,xAxis=None,yAxis=None,interactive=x_brush)
  right = hist(data=data,y=y,width=50,height=200,xAxis=None,yAxis=None,interactive=y_brush)

  mid = scatterplot(data,x=x,y=y,filters=[x_brush,y_brush],interactive=False)
  # question is there a way to 
  return alt.vconcat(top, alt.hconcat(mid,right,spacing=-10), spacing=-10).properties(width=width,height=height)


