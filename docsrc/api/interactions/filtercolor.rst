.. _highlight-color:

============
Highlight Color
============

The highlight_color() function selects the marks that correspond to a specific color in a chart. 
This function grays out all non-selected colors from the chart.


.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_color() + alx.lineplot(data=data.stocks(),x='date',y='price',color='symbol')

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_color() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon',color='Origin')




