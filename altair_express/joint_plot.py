import altair as alt
from .distributional import hist
from .relational import scatterplot

def joint_plot(data=None,x=None, y=None,width=200,height=200):
  x_brush = alt.selection_interval(encodings=['x'],resolve="intersect",name="brush")
  y_brush = alt.selection_interval(encodings=['y'],resolve="intersect",name="brush")

  top = hist(data=data,x=x,width=200,height=50,xAxis=None,yAxis=None,interactive=x_brush)
  right = hist(data=data,y=y,width=50,height=200,xAxis=None,yAxis=None,interactive=y_brush)


  base = scatterplot(data,x=x,y=y,interactive=False)
  bg = base.encode(color=alt.ColorValue("lightgray")).add_selection(alt.selection_interval(encodings=['x','y'],resolve="global",name="brush"))
  fg = base.encode(color=alt.ColorValue("steelblue")).transform_filter(alt.selection_interval(name="brush"))

  mid = bg+fg

  # question is there a way to 
  return  alt.vconcat(top, alt.hconcat(mid,right,spacing=-10), spacing=-10).properties(width=width,height=height)


