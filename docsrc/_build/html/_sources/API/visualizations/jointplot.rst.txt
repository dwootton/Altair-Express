.. _jointplot:

============
Joint Plot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_brush() + alx.jointplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')

The jointplot() function is useful for understanding the distribution and relationship between two variables in a dataset.
Using a scatterplot plot with marginal histogram plots, Jointplots
assist in understanding how variables might interact. 


