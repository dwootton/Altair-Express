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
This visualization allows you to see the distribution of the data points and the relationship between the variables, making it easy to identify patterns and correlations in the data.