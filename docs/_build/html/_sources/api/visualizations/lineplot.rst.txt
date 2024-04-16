.. _lineplot:

============
Lineplot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.stocks()

    alx.lineplot(data=df,x='date',y='price',color='symbol')

The lineplot() function is used to display the relationship between two variables over a continuous interval (often time).
This function creates a line plot where the x-axis represents the interval or time and the y-axis represents the value of the variable.
Lineplots work best for detecting change over time.


Parameters
**********************
data : pandas dataframe.
    The data to visualize as a pandas dataframe. 
x : string
    The column name of the data to be on the x-axis.
y : string
    The column name of the data to be on the y-axis
x_axis : alt.Axis() Object or None
    The column name of the data to be on the x-axis.
y_axis : alt.Axis() Object or None
    The column name of the data to be on the y-axis
color : string 
    The column name in the dataframe to color the bars by or a valid CSS color to make the line of the chart.
width : int
    The width of the chart in pixels.
height : int
    The height of the chart in pixels.
effects : :ref:`effects-object`
    The effects of interactions to be applied to the chart.

Examples
**********************

Interactive Brush
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.stocks()

    alx.highlight_brush() + alx.lineplot(data=df,x='date',y='price',color='symbol')

