.. _lineplot:

============
Lineplot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data
    df = data.stocks()

    alx.highlight_brush() + alx.lineplot(data=df,x='date',y='price',color='symbol')

The lineplot() function is used to display the relationship between two variables over a continuous interval (often time).
This function creates a line plot where the x-axis represents the interval or time and the y-axis represents the value of the variable.
Lineplots work best for detecting change over time.
