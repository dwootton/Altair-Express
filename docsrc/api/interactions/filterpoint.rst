.. _filter-point:

============
Filter Point
============

*Filter Point is used to query specific elements of the data.* It is 
particularly used for cases like outlier selection.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_point() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')




