.. _joint-plot:

============
Joint Plot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_brush() + alx.jointplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')

Jointplots visualize distributional and correlation of two variables.
Using a bivariate scatterplot plot with marginal histogram univariate plots, Jointplots
assist in understanding how variables might interact. 


