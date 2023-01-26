.. _highlight-brush:

============
Highlight Brush
============

*Highlight Brush is used to query a range from the data itself*

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.highlight_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')



