
import altair as alt
from .distributional import hist
from .relational import scatterplot
from .interactions import Interaction, apply_effect, process_effects

def jointplot(data=None,x=None, y=None,effects=None,width=200,height=200):
  """
    Return the most important thing about a person.
    Parameters
    ----------
    data
        A string indicating the name of the person.
  """
   
  top = hist(data=data,x=x,width=200,height=50,x_axis=None,y_axis=None)

  right = hist(data=data,y=y,width=50,height=200,x_axis=None,y_axis=None)
  mid = scatterplot(data=data,x=x,y=y, width = width,height=height)


  # question is there a way to 
  chart =  alt.vconcat(top, alt.hconcat(mid,right,spacing=-10), spacing=-10)

  if effects:
    chart = process_effects(chart,effects)

  return chart
