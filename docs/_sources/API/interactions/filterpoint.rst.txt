.. _filter-point:

============
Filter Point
============

The filter_point() function is a data filtering technique that allows you to filter your data visualization by selecting a specific point in the plot. 
This function removes all non-selected points from the chart (but keeps the axes consistent).
This is particularly useful when investigating specific outliers or looking at a specific record of data.
For multi-point selection, we recommend you use :ref:`highlight-point`. 


Note: if you're using this to select marks separated by another encoding like 'color', you'll need to use the :ref:`filter-color` function.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.filter_point() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_point() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')




