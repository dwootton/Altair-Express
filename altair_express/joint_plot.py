import altair as alt
from .distributional import hist
from .relational import scatterplot

def joint_plot(data=None,x=None, y=None,width=200,height=200):
  x_brush = alt.selection_interval(encodings=['x'],resolve="union",name="brush")
  y_brush = alt.selection_interval(encodings=['y'],resolve="union",name="brush")

  top = hist(data=data,x=x,width=200,height=50,xAxis=None,yAxis=None,interactive=x_brush)
  right = hist(data=data,y=y,width=50,height=200,xAxis=None,yAxis=None,interactive=y_brush)


  base = scatterplot(data,x='Horsepower',y='Miles_per_Gallon',interactive=False)
  bg = base.encode(color=alt.ColorValue("lightgray")).add_selection(alt.selection_interval(encodings=['x','y'],resolve="global",name="brush"))
  fg = base.encode(color=alt.ColorValue("steelblue")).transform_filter(alt.selection_interval(name="brush"))

  mid = bg+fg #add_selection(y_brush).add_selection(x_brush).encode(color=alt.condition(x_brush & y_brush ,alt.value('steelblue'),alt.value('lightgray')))

  # question is there a way to 
  return  alt.vconcat(top, alt.hconcat(mid,right,spacing=-10), spacing=-10)

