.. _barplot:

============
Stripplot
============

.. altair-plot::
    import altair_express as alx
    import pandas as pd

    df = data.seattle_temps().sample(5000)

    df['month'] = pd.DatetimeIndex(df['date']).month_name()
    df['month_index'] = pd.DatetimeIndex(df['date']).month


    chart = alx.stripplot(df,x='temp',color='temp', row='month_index')
    
    chart.configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )

   

A strip plot is a function that shows the numeric distribution of data over categories.
It draws a faceted scatter plot where each row is a value in categorical and one variable is numeric.
Within a data series, the y axis is jittered so it is easier to understand a distribution of data.

Parameters
**********************
data : pandas dataframe or pandas series
    The data to visualize as a pandas dataframe. If a series is provided, the series is used as the variable to be encoded in a histogram.
x : string
    The quantitative column name of the series for the x axis.
row : string
    The column name of the series for the y axis.
color : string 
    A valid CSS color to make the chart or a column name in the dataframe to color the plots by.
row : string
    The column name to be used as the row facet to produced grouped 
width : int
    The width of the chart in pixels.
height : int
    The height of the chart in pixels.
effects : :ref:`effects-object`
    The effects of interactions to be applied to the chart.


Examples
**********************

Quantitative Brush
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::
    import altair_express as alx
    import pandas as pd

    df = data.seattle_temps().sample(5000)

    df['month'] = pd.DatetimeIndex(df['date']).month_name()
    df['month_index'] = pd.DatetimeIndex(df['date']).month


    chart = alx.stripplot(df,x='temp',color='temp', row='month_index')
    
    alx.highlight_brush()+chart.configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )

Selecting Specific Values
^^^^^^^^^^^^^^^^^^^^^^
.. altair-plot::
    alx.highlight_color()+alx.stripplot(df.sample(5000),width=400,x='temp',color='month', row='month_index').configure_facet(
    spacing=0
).configure_view(
    stroke=None
)

