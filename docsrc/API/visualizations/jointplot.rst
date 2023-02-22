.. _jointplot:

============
Joint Plot
============
.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.jointplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')

The jointplot() function is useful for understanding the distribution and relationship between two variables in a dataset.
Using a scatterplot plot with marginal histogram plots, Jointplots
assist in understanding how variables might interact. 


Parameters
**********************
data : pandas dataframe
    The data to visualize as a pandas dataframe. 
x : string
    The column name of the categorical series used for the x axis.
y : string
    The column name of the categorical series used for the y axis.
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

    alx.highlight_brush() + alx.jointplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')
