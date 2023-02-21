.. _panzoom:

============
Panzoom
============

The panzoom() function creates enables the panning and zooming functionality on a chart. 
These can be useful interactions for exploring and analyzing data, particularly if the chart is overplotted or you're interested in exploring different areas of a chart.

.. altair-plot::

    import altair_express as alx
    from vega_datasets import data

    alx.pan_zoom() + alx.scatterplot(data=data.cars(),x='Miles_per_Gallon',y='Horsepower')

