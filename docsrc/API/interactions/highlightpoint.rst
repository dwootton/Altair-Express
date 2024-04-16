.. _highlight-point:

============
Highlight Point
============

The highlight_point() function is a data filtering technique that allows you to filter your data visualization by selecting a specific point in the plot. 
This function dims non-selected points from the chart and highlights the selected point.
This is particularly useful when investigating specific outliers or looking at a specific record of data.

Note: if you're using this to select marks separated by another encoding like 'color', you'll need to use the :ref:`highlight-color` function.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.highlight_point() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')




