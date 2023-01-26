.. _filter-brush:

============
Filter Brush
============

*Filter Brush is used to query a range from the data itself*

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

