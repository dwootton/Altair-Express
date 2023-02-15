.. _filter-color:

============
Filter Color
============

The filter_color() function selects the marks that correspond to a specific color in a chart. 
This function removes all non-selected points from the chart.


.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.filter_color() + alx.lineplot(data=data.stocks(),x='date',y='price',color='symbol)

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.filter_color() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon',color='Origin')




