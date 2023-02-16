.. _scatterplot:

============
Scatterplot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.highlight_brush() + alx.scatterplot(df,x='Horsepower',y='Miles_per_Gallon')

The scatterplot() function is useful for exploring the relationship between two continuous variables. 
This visualization allows you to see the distribution of the data points and the relationship between the variables, 
making it easy to identify patterns and correlations in the data.

Parameters
**********************
data : pandas dataframe or pandas series
    The data to visualize as a pandas dataframe. If a series is provided, the series is used as the variable to be encoded in a histogram.
x : string
    The column name of the data to be on the x-axis.
y : string
    The column name of the data to be on the y-axis
x_axis : alt.Axis() Object or None
    The column name of the data to be on the x-axis.
y_axis : alt.Axis() Object or None
    The column name of the data to be on the y-axis
color : string 
    A valid CSS color to make the chart or a column name in the dataframe to color the bars by.
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
    df = data.cars()

    alx.highlight_brush() + alx.scatterplot(df,x='Horsepower',y='Miles_per_Gallon')

    
Split by color  
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.cars()

    alx.highlight_color() + alx.scatterplot(df,x='Horsepower',y='Miles_per_Gallon', color='Origin')

