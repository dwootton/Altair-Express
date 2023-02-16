.. _highlight-brush:

============
Highlight Brush
============

The highlight_brush() function allows you to interact with a data visualization by brushing a specific area of the chart.
This is particularly interested when datapoints of interest are closed together as all non-brushed data points become grayed out.
Through highlighting data within your brush, you can focus your analysis on the data that matters. 

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.highlight_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')
