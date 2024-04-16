.. _filter-brush:

============
Filter Brush
============

The filter_brush() function allows you to interact with a data visualization by brushing or selecting a specific area of the chart.
This is particularly interested when datapoints of interest share a range of values as all non-brushed data points from the chart, while keeping the axes consistent. 
Through filtering out data not within your brush, you can focus your analysis on the data that matters. 

This interaction technique is separate from other techniques like :ref:`highlight-brush` in that it removes all non-brushed data from the chart. 

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_brush() + alx.scatterplot(data=data.cars(),x='Horsepower',y='Miles_per_Gallon')

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data


    alx.filter_brush() + alx.countplot(data=data.cars(),x='Origin')

